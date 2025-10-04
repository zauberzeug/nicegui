#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent

LICENSE_LINKS = {
    'MIT': 'https://opensource.org/licenses/MIT',
    'Apache-2.0': 'https://opensource.org/licenses/Apache-2.0',
    'BSD-2-Clause': 'https://opensource.org/licenses/BSD-2-Clause',
    'BSD 3-Clause': 'https://opensource.org/licenses/BSD-3-Clause',
    'ISC': 'https://opensource.org/licenses/ISC',
}

with (ROOT / 'DEPENDENCIES.md').open('w') as output_file:
    output_file.write('# Included Web Dependencies\n\n')

    for p in [ROOT / 'package.json', *sorted(ROOT.glob('nicegui/elements/*/package.json'))]:
        package_lock = json.loads(p.with_stem('package-lock').read_text(encoding='utf-8'))
        for name, version in json.loads(p.read_text(encoding='utf-8')).get('dependencies', {}).items():
            assert isinstance(name, str)
            try:
                license_string = package_lock['packages'][f'node_modules/{name}']['license']
            except KeyError:
                with (p.with_name('node_modules') / name / 'LICENSE').open('r') as license_file:
                    license_string = license_file.readline().strip().removesuffix(' License')
            output_file.write(f'- {name}: {version} ([{license_string}]({LICENSE_LINKS[license_string]}))\n')
