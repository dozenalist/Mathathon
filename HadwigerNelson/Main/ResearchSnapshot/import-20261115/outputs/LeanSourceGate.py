"""Conservative review gate, not an execution sandbox or proof validator."""
import re


def code_only(text):
    out = list(text)
    i = 0
    while i < len(text):
        start = i
        if text.startswith('--', i):
            end = text.find('\n', i)
            i = len(text) if end < 0 else end
        elif text.startswith('/-', i):
            depth = 1
            i += 2
            while i < len(text) and depth:
                if text.startswith('/-', i):
                    depth += 1
                    i += 2
                elif text.startswith('-/', i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            if depth:
                raise ValueError('Unclosed Lean comment requires review')
        elif text[i] == '"':
            previous = ''.join(out[:i]).rstrip()
            if previous and (previous[-1].isalnum() or previous[-1] in '!_#'):
                raise ValueError('Prefixed/interpolated string requires review')
            i += 1
            while i < len(text) and text[i] != '"':
                if text[i] == '\\':
                    i += 2
                else:
                    i += 1
            if i >= len(text):
                raise ValueError('Unclosed Lean string requires review')
            i += 1
        elif text[i] in '«»':
            raise ValueError('Escaped identifier requires review')
        else:
            i += 1
            continue
        for k in range(start, i):
            if out[k] not in '\r\n':
                out[k] = ' '
    return ''.join(out)


def validate_source(text):
    code = code_only(text)
    if re.search(r'\b(sorry|admit|axiom|unsafe|initialize|builtin_initialize|elab|macro|run_tac|run_meta|run_elab|IO|System|extern|native_decide)\b', code):
        raise ValueError('Source requires manual review: axiom, placeholder or executable metaprogram')
    if re.search(r'\bimport\s+Lean\b', code):
        raise ValueError('Lean metaprogramming import requires review')
    for line in code.splitlines():
        if '#' in line and (line.count('#') != 1 or not re.match(r'^\s*#(?:check\s|print\s+axioms\s)', line)):
            raise ValueError('Command requires manual review')

