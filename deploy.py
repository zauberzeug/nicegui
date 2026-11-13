#!/usr/bin/env python3
import argparse
import json
import subprocess
import time

PIN_TIMEOUT = 120


def run(cmd: list[str], *, capture: bool = False) -> str:
    """Run a command and return the output."""
    if capture:
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    subprocess.run(cmd, check=True)
    return ''


def is_healthy(machine: dict) -> bool:
    """Check if a machine is started and passing all health checks."""
    if machine.get('state') != 'started':
        return False
    return all(c.get('status') == 'passing' for c in machine.get('checks', []))


def is_pinned(machine: dict) -> bool:
    """Check if a machine already has autostop disabled."""
    services = machine.get('config', {}).get('services', [])
    return bool(services and services[0].get('autostop') is False)


instances = {
    'yyz': 2,  # Toronto, Ontario (Canada)
    'iad': 3,  # Washington DC, Virginia (US)
    'sjc': 4,  # San Jose, California (US)
    'lax': 2,  # Los Angeles, California (US)
    'dfw': 2,  # Dallas, Texas (US)
    'mia': 0,  # Miami, Florida (US)
    'sea': 0,  # Seattle, Washington (US)
    'fra': 6,  # Frankfurt, Germany
    'ams': 2,  # Amsterdam, Netherlands
    'cdg': 3,  # Paris, France
    'lhr': 2,  # London, England (UK)
    'jnb': 1,  # Johannesburg, South Africa
    'bom': 0,  # Mumbai, India (deprecated by Fly, use sin instead)
    'nrt': 4,  # Tokyo, Japan
    'sin': 5,  # Singapore
    'syd': 1,  # Sydney, Australia
    'gru': 1,  # Sao Paulo, Brazil
}


parser = argparse.ArgumentParser(description='Deploy NiceGUI to Fly.io')
parser.add_argument('--scale-only', action='store_true', help='Skip deploy, only run scaling and pinning')
args = parser.parse_args()

if not args.scale_only:
    try:
        tag = run(['git', 'describe', '--abbrev=0', '--tags', '--match', 'v*'], capture=True).strip()
        version = tag.lstrip('v') or '0.0.0'
    except Exception:
        version = '0.0.0'
    run(['fly', 'deploy', '--wait-timeout', '600', '--lease-timeout', '30s', '--build-arg', f'VERSION={version}'])

print('scaling regions...')
for region, count in instances.items():
    try:
        run(['fly', 'scale', 'count', f'app={count}', '--region', region, '-y'])
    except subprocess.CalledProcessError:
        print(f'  could not scale {region}, continuing')
    time.sleep(2)

# wait for machines to become healthy before pinning
print('waiting for machines to become healthy...')
HEALTH_TIMEOUT = 60
HEALTH_INTERVAL = 5
expected_regions = {r for r, c in instances.items() if c > 0}
healthy_regions: set[str] = set()
for elapsed in range(0, HEALTH_TIMEOUT, HEALTH_INTERVAL):
    machines_json = run(['fly', 'machines', 'list', '--json'], capture=True)
    machines = json.loads(machines_json)
    healthy_regions = {m.get('region') for m in machines if is_healthy(m)}
    if expected_regions <= healthy_regions:
        print(f'  all regions healthy after {elapsed}s')
        break
    time.sleep(HEALTH_INTERVAL)
else:
    missing = expected_regions - healthy_regions
    print(f'  timed out waiting for: {", ".join(sorted(missing))}')

# pin one machine per region to avoid cold-start latency
print('pinning machines...')
machines = json.loads(run(['fly', 'machines', 'list', '--json'], capture=True))
by_region: dict[str, list[dict]] = {}
for m in machines:
    by_region.setdefault(m.get('region', 'unknown'), []).append(m)

failed_regions: list[str] = []
for region, count in instances.items():
    if count == 0:
        continue
    region_machines = by_region.get(region, [])
    for m in region_machines:
        if m.get('state') not in ('started', 'stopped'):
            print(f'  {m["id"]} in {region} is in state {m.get("state")}, needs manual intervention')
    pinned = next((m for m in region_machines if is_pinned(m)), None)
    if pinned:
        print(f'  {pinned["id"]} in {region} already pinned')
        continue
    # prefer healthy running machines, but a stopped machine is fine too: the update starts it
    candidates = sorted(region_machines, key=lambda m: (not is_healthy(m), m.get('state') != 'started'))
    for m in candidates:
        if m.get('state') not in ('started', 'stopped'):
            continue
        try:
            run(['fly', 'machine', 'update', m['id'], '--autostop=false', f'--wait-timeout={PIN_TIMEOUT}', '-y'])
            print(f'  pinned {m["id"]} in {region}')
            break
        except subprocess.CalledProcessError:
            print(f'  {m["id"]} in {region} failed to pin, trying next machine')
    else:
        failed_regions.append(region)
    time.sleep(2)

if failed_regions:
    print(f'\nWARNING: could not pin machines in: {", ".join(failed_regions)}')
else:
    print('all machines pinned successfully')
