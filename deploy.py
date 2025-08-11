#!/usr/bin/env python3
import json
import subprocess
from typing import List


def run(cmd: List[str], *, capture: bool = False) -> str:
    """Run a command and return the output."""
    if capture:
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    subprocess.run(cmd, check=True)
    return ''


try:
    tag = run(['git', 'describe', '--abbrev=0', '--tags', '--match', 'v*'], capture=True).strip()
    version = tag.lstrip('v') or '0.0.0'
except Exception:
    version = '0.0.0'

run(['fly', 'deploy', '--wait-timeout', '360', '--build-arg', f'VERSION={version}'])

instances = {
    'yul': 2,  # Montreal, Quebec (Canada)
    'iad': 4,  # Washington DC, Virginia (US)
    'sjc': 2,  # San Jose, California (US)
    'lax': 2,  # Los Angeles, California (US)
    'mia': 3,  # Miami, Florida (US)
    'sea': 2,  # Seattle, Washington (US)
    'fra': 5,  # Frankfurt, Germany
    'ams': 2,  # Amsterdam, Netherlands
    'mad': 1,  # Madrid, Spain
    'cdg': 2,  # Paris, France
    'lhr': 2,  # London, England (UK)
    'otp': 1,  # Bucharest, Romania
    'jnb': 1,  # Johannesburg, South Africa
    'bom': 1,  # Mumbai, India
    'nrt': 4,  # Tokyo, Japan
    'sin': 2,  # Singapore
    'hkg': 4,  # Hong Kong
    'syd': 1,  # Sydney, Australia
    'gru': 1,  # Sao Paulo, Brazil
}
for region, count in instances.items():
    run(['fly', 'scale', 'count', f'app={count}', '--region', region, '-y'])

# NOTE: pin first machine per region to avoid cold-start latency
machines_json = run(['fly', 'machines', 'list', '--json'], capture=True)
machines = json.loads(machines_json)
pinned_regions = set()
for m in machines:
    region = m.get('region', 'unknown')
    if region in pinned_regions:
        continue
    machine_id = m.get('id')
    if machine_id:
        run(['fly', 'machine', 'update', machine_id, '--autostop=false', '-y'])
        print(f'pinned {machine_id} in {region}')
        pinned_regions.add(region)
