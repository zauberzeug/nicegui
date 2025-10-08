#!/usr/bin/env python3
"""Collect screenshots for failed pytest tests.

Reads `reports/junit.xml` for `<failure>` or `<error>` entries and copies
matching files from `screenshots/` to `failed-screenshots/`.

It supports matching multiple files per test name using glob patterns.
"""
from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    junit = Path('reports/junit.xml')
    screenshots = Path('screenshots')
    out = Path('failed-screenshots')
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    if not junit.exists():
        print('No junit.xml found; nothing to collect')
        return 0

    tree = ET.parse(junit)
    root = tree.getroot()
    failed = set()
    for tc in root.iter('testcase'):
        for child in tc:
            if child.tag in ('failure', 'error'):
                name = tc.attrib.get('name')
                if name:
                    failed.add(name)
                break

    copied = 0
    for name in failed:
        src = screenshots / f'{name}.png'
        if src.exists():
            dest = out / src.name
            shutil.copyfile(src, dest)
            copied += 1

    print(f'Collected {copied} failed screenshots for {len(failed)} failing tests')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
