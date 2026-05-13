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
    'bom': 1,  # Mumbai, India
    'nrt': 4,  # Tokyo, Japan
    'sin': 4,  # Singapore
    'syd': 1,  # Sydney, Australia
    'gru': 1,  # Sao Paulo, Brazil
}


def destroy_and_rescale(machine_id: str, region: str) -> None:
    """Destroy a machine and re-scale the region to replace it."""
    run(['fly', 'machine', 'destroy', machine_id, '--force'])
    run(['fly', 'scale', 'count', f'app={instances.get(region, 1)}', '--region', region, '-y'])


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
    run(['fly', 'scale', 'count', f'app={count}', '--region', region, '-y'])
    time.sleep(2)

# NOTE: wait for machines to become healthy before pinning
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

# NOTE: pin first machine per region to avoid cold-start latency
print('pinning machines...')
machines_json = run(['fly', 'machines', 'list', '--json'], capture=True)
machines = json.loads(machines_json)
pinned_regions: set[str] = set()
recovered_regions: list[str] = []
for m in machines:
    region = m.get('region', 'unknown')
    if region in pinned_regions or region in recovered_regions:
        continue
    machine_id = m.get('id')
    if not machine_id:
        continue
    if not is_healthy(m):
        if instances.get(region, 0) == 0:
            print(f'  {machine_id} in {region} is unhealthy but region is scaled to 0, destroying...')
            run(['fly', 'machine', 'destroy', machine_id, '--force'])
            continue
        print(f'  {machine_id} in {region} is unhealthy (state={m.get("state")}), destroying and re-provisioning...')
        try:
            destroy_and_rescale(machine_id, region)
        except subprocess.CalledProcessError:
            print(f'  could not recover {region}')
        recovered_regions.append(region)
        continue
    if is_pinned(m):
        print(f'  {machine_id} in {region} already pinned')
        pinned_regions.add(region)
        continue
    try:
        run(['fly', 'machine', 'update', machine_id, '--autostop=false', f'--wait-timeout={PIN_TIMEOUT}', '-y'])
        print(f'  pinned {machine_id} in {region}')
        pinned_regions.add(region)
    except subprocess.CalledProcessError:
        print(f'  {machine_id} in {region} failed to pin, destroying and re-provisioning...')
        try:
            destroy_and_rescale(machine_id, region)
        except subprocess.CalledProcessError:
            print(f'  could not recover {region}')
        recovered_regions.append(region)
    time.sleep(2)

if recovered_regions:
    print(f'\nre-pinning recovered regions ({", ".join(recovered_regions)})...')
    time.sleep(10)
    machines_json = run(['fly', 'machines', 'list', '--json'], capture=True)
    machines = json.loads(machines_json)
    for m in machines:
        region = m.get('region', 'unknown')
        if region not in recovered_regions or region in pinned_regions:
            continue
        machine_id = m.get('id')
        if not machine_id:
            continue
        if not is_healthy(m):
            print(f'  {machine_id} in {region} still unhealthy, needs manual intervention')
            continue
        try:
            run(['fly', 'machine', 'update', machine_id, '--autostop=false', f'--wait-timeout={PIN_TIMEOUT}', '-y'])
            print(f'  pinned {machine_id} in {region}')
            pinned_regions.add(region)
        except subprocess.CalledProcessError:
            print(f'  {machine_id} in {region} still failing, needs manual intervention')
        time.sleep(2)

still_failed = [r for r in recovered_regions if r not in pinned_regions]
if still_failed:
    print(f'\nWARNING: could not pin machines in: {", ".join(still_failed)}')
else:
    print('all machines pinned successfully')
