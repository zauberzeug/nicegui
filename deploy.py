#!/usr/bin/env python3
import json
import subprocess
import time


def run(cmd: list[str], *, capture: bool = False) -> str:
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

run(['fly', 'deploy', '--wait-timeout', '600', '--lease-timeout', '30s', '--build-arg', f'VERSION={version}'])

instances = {
    'yyz': 2,  # Toronto, Ontario (Canada)
    'iad': 3,  # Washington DC, Virginia (US)
    'sjc': 4,  # San Jose, California (US)
    'lax': 2,  # Los Angeles, California (US)
    'dfw': 2,  # Dallas, Texas (US)
    'mia': 0,   # Miami, Florida (US)
    'sea': 0,  # Seattle, Washington (US)
    'fra': 4,  # Frankfurt, Germany
    'ams': 2,  # Amsterdam, Netherlands
    'cdg': 3,  # Paris, France
    'lhr': 2,  # London, England (UK)
    'jnb': 1,  # Johannesburg, South Africa
    'bom': 1,  # Mumbai, India
    'nrt': 4,  # Tokyo, Japan
    'sin': 4,  # Singapore
    'syd': 1,  # Sydney, Australia
    'gru': 1,  # Sao Paulo, Brazil
}

print('scaling regions...')
for region, count in instances.items():
    run(['fly', 'scale', 'count', f'app={count}', '--region', region, '-y'])
    time.sleep(2)

# NOTE: pin first machine per region to avoid cold-start latency
print('pinning machines...')
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
        time.sleep(2)
