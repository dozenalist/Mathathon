"""Serial local Lean queue. Frozen sources/pins, bounded children, no automatic retries."""
import argparse
from datetime import datetime, timezone
import hashlib
import os
import re
import subprocess
import time
from automation_io import ROOT, HIDDEN, ExclusiveLock, inside, read_json, write_json, utc, memory
from LeanSourceGate import validate_source

QUEUE = ROOT / 'work/lean-queue'
CONTROL = ROOT / 'work/automation-supervisor'

def admit_proposals(queue):
    directory=CONTROL/'lean-proposals'
    for path in sorted(directory.glob('*.json')) if directory.exists() else []:
        proposal=read_json(path)
        if proposal.get('status')!='proposed':continue
        try:
            artifact=inside(CONTROL/'inbox',proposal['artifact'])
            text=artifact.read_text(encoding='utf-8')
            if artifact.suffix!='.lean' or len(text)>50000:
                raise ValueError('Only bounded Lean source is admitted')
            validate_source(text)
            template=next(j for j in queue['jobs'] if j['id']==proposal['template_job'] and j['status']=='passed')
            job_id=proposal['id']
            if any(j['id']==job_id for j in queue['jobs']):
                proposal['status']='already_queued';write_json(path,proposal);continue
            location=inside(QUEUE,'claude-admissions/'+job_id)
            location.mkdir(parents=True,exist_ok=True)
            # Pin exactly the bytes written; Windows text mode would translate LF to CRLF.
            (location/'Candidate.lean').write_bytes(text.encode('utf-8'))
            job={k:template[k] for k in ('leanExe','expectedVersion','expectedCommit','mathlibRoot','requiredMathlib','leanPath') if k in template}
            job.update(id=job_id,status='queued',source=str((location/'Candidate.lean').relative_to(QUEUE)),
                       output=str((location/'Candidate.olean').relative_to(QUEUE)),workingDirectory=str(location.relative_to(QUEUE)),
                       expectedSourceSha256=hashlib.sha256(text.encode()).hexdigest(),timeoutSeconds=480,
                       purpose=proposal.get('purpose','Claude-reviewed pure Lean check'),dependsOn=template['id'],reviewedBy='Claude supervisor plus conservative source gate')
            queue['jobs'].append(job);proposal['status']='queued'
        except Exception as exc:
            proposal.update(status='needs_review',error=str(exc))
        write_json(path,proposal)

def check_output(args, **kwargs):
    return subprocess.check_output(args, text=True, encoding='utf-8', errors='replace', timeout=30, creationflags=HIDDEN, **kwargs).strip()

def run_job(job):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', job['id']):
        raise ValueError('Invalid job id')
    source = inside(QUEUE, job['source'])
    output = inside(QUEUE, job.get('output', job['id'] + '.olean'))
    cwd = inside(QUEUE, job['workingDirectory']) if job.get('workingDirectory') else QUEUE
    if source.suffix != '.lean' or output.suffix != '.olean':
        raise ValueError('Invalid source/output extension')
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if job.get('expectedSourceSha256') and digest != job['expectedSourceSha256']:
        raise ValueError('Frozen source hash mismatch')
    version = check_output([job['leanExe'], '--version'])
    if job['expectedVersion'] not in version or job.get('expectedCommit', '') not in version:
        raise ValueError('Lean pin mismatch')
    if job.get('requiredMathlib'):
        revision = check_output(['git', '-C', job['mathlibRoot'], 'rev-parse', 'HEAD'])
        if revision != job['requiredMathlib']:
            raise ValueError('Mathlib pin mismatch')
    env = os.environ.copy()
    env.pop('LEAN_NUM_THREADS', None)
    env.pop('LEAN_PATH', None)
    if job.get('leanPath'):
        env['LEAN_PATH'] = job['leanPath']
    args = [job['leanExe']]
    # The tested default import completed; the old forced4GiB setup stalled.
    # Explicit overrides remain available per job, never global settings.
    if job.get('threads'):
        args += ['-j', str(int(job['threads']))]
    if job.get('compilerMemoryMiB'):
        args += ['-M', str(int(job['compilerMemoryMiB']))]
    if job.get('profile'):
        args.append('--profile')
    output.parent.mkdir(parents=True, exist_ok=True)
    args += ['-o', str(output), str(source)]
    log = QUEUE / (job['id'] + '.python.log')
    timeout = min(900, max(10, int(job.get('timeoutSeconds', 480))))
    job.update(status='running', startedUtc=utc(), sourceSha256=digest, actualVersion=version, runner='python', command=args)
    write_json(QUEUE / 'queue.json', active_queue)
    start = time.monotonic()
    child = None
    try:
        with log.open('w', encoding='utf-8') as stream:
            child = subprocess.Popen(args, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, creationflags=HIDDEN)
            job['processId'] = child.pid
            write_json(QUEUE / 'queue.json', active_queue)
            reason = None
            while child.poll() is None:
                metrics = memory(child.pid)
                elapsed = time.monotonic() - start
                job.update(elapsedSeconds=round(elapsed, 2), **metrics)
                job['peakWorkingSetMiB'] = max(job.get('peakWorkingSetMiB', 0), metrics.get('workingSetMiB', 0))
                job['peakPrivateMiB'] = max(job.get('peakPrivateMiB', 0), metrics.get('privateMiB', 0))
                try:
                    write_json(QUEUE / (job['id'] + '.progress.json'), job)
                except OSError:
                    pass  # Telemetry contention must never abort compilation.
                if elapsed > timeout:
                    reason = 'timeout'
                elif metrics.get('workingSetMiB', 0) > job.get('maxRssMiB', 8192) or metrics.get('privateMiB', 0) > job.get('maxPrivateMiB', 12288) or metrics['availableMiB'] < 2048:
                    reason = 'memory_guard'
                elif (CONTROL / 'STOP_LEAN').exists():
                    reason = 'stopped'
                if reason:
                    child.kill(); child.wait(timeout=10); break
                time.sleep(2)
            job['exitCode'] = child.wait()
            job['status'] = reason or ('passed' if child.returncode == 0 else 'failed')
        text = log.read_text(encoding='utf-8', errors='replace')
        if job['status'] == 'passed' and (not output.exists() or 'sorryAx' in text or "declaration uses 'sorry'" in text):
            job.update(status='failed_validation', error='Output missing or sorry detected')
    finally:
        if child is not None and child.poll() is None:
            child.kill(); child.wait(timeout=10)
        job['finishedUtc'] = utc()
        job['elapsedSeconds'] = round(time.monotonic() - start, 2)
        job['log'] = str(log)

def cycle():
    global active_queue
    with ExclusiveLock(QUEUE / 'queue.lock'):
        active_queue = read_json(QUEUE / 'queue.json')
        if active_queue['maxParallel'] != 1:
            raise ValueError('Only serial Lean execution is allowed')
        if any(j['status'] == 'running' for j in active_queue['jobs']):
            raise RuntimeError('Reconcile prior running job before restarting')
        admit_proposals(active_queue)
        write_json(QUEUE/'queue.json',active_queue)
        for job in active_queue['jobs']:
            if (CONTROL / 'STOP_LEAN').exists() or datetime.now(timezone.utc) >= DEADLINE:
                break
            if job['status'] != 'queued':
                continue
            dependency = job.get('dependsOn')
            if dependency and not any(j['id'] == dependency and j['status'] == 'passed' for j in active_queue['jobs']):
                job.update(status='blocked_dependency', error='Preceding job did not pass')
                write_json(QUEUE / 'queue.json', active_queue)
                continue
            write_json(CONTROL / 'lean-status.json', {'pid': os.getpid(), 'status':'running', 'job':job['id'], 'at':utc()})
            try:
                run_job(job)
            except Exception as exc:
                job.update(status='runner_error', error=str(exc), finishedUtc=utc())
            write_json(QUEUE / 'queue.json', active_queue)
            write_json(QUEUE / (job['id'] + '.progress.json'), job)
            print(job['id'] + ': ' + job['status'], flush=True)
            if job['status'] not in ('passed', 'blocked_dependency'):
                break
        write_json(CONTROL / 'lean-status.json', {'pid':os.getpid(), 'status':'idle', 'at':utc(), 'queued':sum(j['status']=='queued' for j in active_queue['jobs'])})

def main():
    global DEADLINE
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', action='store_true')
    parser.add_argument('--deadline', default='2026-11-15T17:35:13+00:00')
    options = parser.parse_args()
    DEADLINE = datetime.fromisoformat(options.deadline)
    CONTROL.mkdir(parents=True, exist_ok=True)
    with ExclusiveLock(CONTROL / 'lean-watch.lock'):
        while datetime.now(timezone.utc) < datetime.fromisoformat(options.deadline) and not (CONTROL/'STOP_LEAN').exists():
            try:
                cycle()
            except Exception as exc:
                write_json(CONTROL/'lean-status.json', {'status':'needs_review','error':str(exc),'at':utc(),'pid':os.getpid()})
            if not options.watch:
                break
            time.sleep(15)

if __name__ == '__main__':
    main()
