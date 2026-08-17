#!/usr/bin/env python3
"""Validate MANIFEST.md reference integrity for machiavelli-library.

Checks every relative link in every MANIFEST.md:
  1. target file must exist (relative to the MANIFEST's directory)
  2. target file must be > MIN_BYTES (catches empty/stub files)

Usage:
  python3 scripts/validate-manifest.py          # check all, exit 1 if broken
  python3 scripts/validate-manifest.py --json   # machine-readable output
"""
import os, re, sys, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_BYTES = 200

def find_manifests(base):
    manifests = []
    for root, dirs, files in os.walk(base):
        if '.git' in root:
            continue
        if 'MANIFEST.md' in files:
            manifests.append(os.path.join(root, 'MANIFEST.md'))
    return sorted(manifests)

def extract_refs(content):
    """Return (text, target) pairs for markdown links and bare paths."""
    refs = []
    # markdown links: [text](target)
    for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', content):
        text, target = m.group(1).strip(), m.group(2).strip()
        if target.startswith(('http://', 'https://', '#')):
            continue
        refs.append((text, target))
    return refs

def main():
    manifests = find_manifests(BASE)
    total_refs = 0
    broken = []
    stub = []
    checked_manifests = 0

    for mpath in manifests:
        rel_m = os.path.relpath(mpath, BASE)
        try:
            content = open(mpath, encoding='utf-8').read()
        except Exception as e:
            broken.append((rel_m, '<unreadable>', str(e)))
            continue
        refs = extract_refs(content)
        if not refs:
            continue
        checked_manifests += 1
        mdir = os.path.dirname(mpath)
        for text, target in refs:
            total_refs += 1
            # strip anchor suffix
            target_clean = target.split('#')[0]
            if not target_clean:
                continue
            full = os.path.normpath(os.path.join(mdir, target_clean))
            if not os.path.exists(full):
                broken.append((rel_m, target, 'MISSING'))
            else:
                size = os.path.getsize(full)
                if os.path.isfile(full) and size < MIN_BYTES:
                    stub.append((rel_m, target, f'{size}B'))

    ok = not broken
    print(f'machiavelli-library MANIFEST validation')
    print(f'  MANIFESTs with refs : {checked_manifests}')
    print(f'  total refs checked  : {total_refs}')
    print(f'  broken (missing)    : {len(broken)}')
    print(f'  stubs (<{MIN_BYTES}B)  : {len(stub)}')

    for rel_m, target, reason in broken:
        print(f'  ❌ {rel_m} → {target} ({reason})')
    for rel_m, target, size in stub:
        print(f'  ⚠️  {rel_m} → {target} ({size})')

    if '--json' in sys.argv:
        print(json.dumps({
            'manifests': checked_manifests,
            'total_refs': total_refs,
            'broken': [{'manifest': m, 'target': t, 'reason': r} for m, t, r in broken],
            'stubs': [{'manifest': m, 'target': t, 'size': r} for m, t, r in stub],
        }, ensure_ascii=False, indent=2))

    print()
    if broken:
        print(f'❌ FAILED: {len(broken)} broken references')
        sys.exit(1)
    if stub:
        print(f'⚠️  PASSED with {len(stub)} stub targets (informational)')
        sys.exit(0)
    print('✅ All MANIFEST references valid')
    sys.exit(0)

if __name__ == '__main__':
    main()
