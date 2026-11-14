"""Inspect the authors' uncompressed tar archive with bounded HTTP ranges.

This optional network command downloads tar headers and small source/metadata
files, never an entire solver output. Raw upstream files stay in the ignored
_upstream_cache directory. It does not execute any downloaded Julia code.

Run explicitly: python fetch_upstream_metadata.py --fetch
Add --include-d4-slice to retrieve the first 10 primal SOS blocks (13 MB).
"""

import argparse
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_upstream_cache"
ARCHIVE_URL = "https://dspace.mit.edu/server/api/core/bitstreams/3ad1c7a0-ced0-45b8-8070-310dccc2190c/content"
ARCHIVE_SIZE = 1227925504
ARCHIVE_MD5 = "b00fa1aa734c483e69a202aac161377c"


class RangeReader:
    def __init__(self, budget=20000000):
        self.budget = budget
        self.downloaded = 0
        self.requests = 0

    def get(self, start, size):
        if size <= 0 or size > self.budget - self.downloaded:
            raise ValueError("HTTP byte budget exceeded before request")
        end = min(start + size, ARCHIVE_SIZE) - 1
        request = urllib.request.Request(ARCHIVE_URL, headers={"Range": f"bytes={start}-{end}"})
        with urllib.request.urlopen(request, timeout=30) as response:
            expected = f"bytes {start}-{end}/{ARCHIVE_SIZE}"
            if response.status != 206 or response.headers.get("Content-Range") != expected:
                raise ValueError("Server did not honor the exact byte range; refusing full download")
            data = response.read(end - start + 2)
        if len(data) != end - start + 1:
            raise ValueError("Range response has unexpected length")
        self.downloaded += len(data)
        self.requests += 1
        return data


def inspect_archive(reader):
    entries = []
    offset = 0
    while offset < ARCHIVE_SIZE:
        data = reader.get(offset, min(65536, ARCHIVE_SIZE - offset))
        next_offset = offset
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
            while True:
                try:
                    member = archive.next()
                except tarfile.ReadError:
                    break
                if member is None:
                    return entries
                start = offset + member.offset_data
                entry = dict(name=member.name, size=member.size, header_offset=offset + member.offset,
                             data_offset=start, type="file" if member.isfile() else "other")
                entries.append(entry)
                next_offset = start + ((member.size + 511) // 512) * 512
                relative_name = member.name.removeprefix("ThreePointSpherePacking/")
                wanted = (relative_name in ("README.txt", "Project.toml", "Manifest.toml")
                          or relative_name.startswith("src/") and relative_name.endswith(".jl")
                          and not Path(relative_name).name.startswith("._")
                          or relative_name in ("latticethreepointdata/indices-13.jls",
                                               "latticethreepointdata/pivots-4-13.jls"))
                if member.isfile() and wanted:
                    if member.offset_data + member.size <= len(data):
                        content = data[member.offset_data:member.offset_data + member.size]
                    else:
                        content = reader.get(start, member.size)
                    target = (CACHE / relative_name).resolve()
                    if not target.is_relative_to(CACHE.resolve()):
                        raise ValueError("Archive member escapes the designated cache directory")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                    entry["sha256"] = hashlib.sha256(content).hexdigest()
                if next_offset >= offset + len(data):
                    break
        if next_offset <= offset:
            raise ValueError("Tar header scan made no progress")
        offset = next_offset
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="explicitly enable bounded network reads")
    parser.add_argument("--include-d4-slice", action="store_true", help="also fetch the 13 MB first-shell inspection input")
    args = parser.parse_args()
    if not args.fetch:
        parser.error("Use --fetch to enable this optional network operation")
    CACHE.mkdir(parents=True, exist_ok=True)
    reader = RangeReader()
    entries = inspect_archive(reader)
    slice_info = None
    if args.include_d4_slice:
        start = 998708224 + 22974632
        size = 13000000
        data = reader.get(start, size)
        digest = hashlib.sha256(data).hexdigest()
        expected = "e5b40f2b0616852fe7fd6177dbd353b9b35bfbca93ff5f5e3f0a2a40de92e7d1"
        if digest != expected:
            raise ValueError("Published solver slice differs from the inspected version")
        (CACHE / "d4-yMat-first13MB.txt").write_bytes(data)
        slice_info = dict(start=start, size=size, sha256=digest)
    result = dict(source_url=ARCHIVE_URL, full_archive_size=ARCHIVE_SIZE,
                  full_archive_md5_from_repository=ARCHIVE_MD5,
                  full_archive_downloaded=False, full_archive_checksum_verified=False,
                  bytes_retrieved=reader.downloaded, http_range_requests=reader.requests,
                  optional_d4_slice=slice_info, entries=entries)
    (HERE / "upstream_archive_index.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Indexed {len(entries)} tar members using {reader.downloaded} bytes in {reader.requests} range requests.")
    for entry in entries:
        if entry["name"].startswith("ThreePointSpherePacking/latticethreepointdata/"):
            print(entry["name"], entry["size"], entry["data_offset"])


if __name__ == "__main__":
    main()
