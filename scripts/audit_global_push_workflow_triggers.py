#!/usr/bin/env python3
from pathlib import Path
import re

WORKFLOWS = Path('.github/workflows')


def block_after(lines, start, indent):
    out = []
    for i in range(start + 1, len(lines)):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith('#'):
            out.append(raw)
            continue
        cur = len(raw) - len(raw.lstrip(' '))
        if cur <= indent:
            break
        out.append(raw)
    return out


def classify(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    global_push = False
    scoped_push = False
    forms = []

    for i, raw in enumerate(lines):
        stripped = raw.strip()
        if re.fullmatch(r'on:\s*push\s*', stripped):
            global_push = True
            forms.append(('inline', i + 1))
        if stripped.startswith('on:') and '[' in stripped and 'push' in stripped:
            global_push = True
            forms.append(('inline-list', i + 1))

        m = re.match(r'^(\s*)push:\s*(?:#.*)?$', raw)
        if not m:
            continue
        indent = len(m.group(1))
        child = block_after(lines, i, indent)
        child_text = '\n'.join(child)
        has_scope = any(
            re.search(rf'^\s*{key}:', x)
            for x in child
            for key in ('branches', 'branches-ignore', 'paths', 'paths-ignore', 'tags', 'tags-ignore')
        )
        if has_scope:
            scoped_push = True
            forms.append(('scoped-block', i + 1))
        else:
            global_push = True
            forms.append(('global-block', i + 1))

    return global_push, scoped_push, forms


def main():
    offenders = []
    scoped = []
    no_push = []

    for path in sorted(list(WORKFLOWS.glob('*.yml')) + list(WORKFLOWS.glob('*.yaml'))):
        global_push, scoped_push, forms = classify(path)
        if global_push:
            offenders.append((str(path), forms))
        elif scoped_push:
            scoped.append(str(path))
        else:
            no_push.append(str(path))

    print('workflow_files', len(offenders) + len(scoped) + len(no_push))
    print('global_push_workflows', len(offenders))
    print('scoped_push_workflows', len(scoped))
    print('no_push_workflows', len(no_push))
    for path, forms in offenders:
        print('GLOBAL_PUSH', path, forms)
    for path in scoped:
        print('SCOPED_PUSH', path)

    print('PASS AUDIT_GLOBAL_PUSH_WORKFLOW_TRIGGERS')
    print('scope=diagnostic only; no workflow trigger is changed by this script')


if __name__ == '__main__':
    main()
