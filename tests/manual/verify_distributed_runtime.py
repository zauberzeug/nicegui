"""Empirical verification of the three critical findings from the multi-reviewer pass.

Run with the venv that has nicegui + eclipse-zenoh installed:
  ./.venv/bin/python /tmp/verify_reviews.py
"""
from __future__ import annotations

import asyncio
import json
import sys
import threading
from pathlib import Path

import zenoh

from nicegui.distributed import DistributedSession

# Make the patched nicegui importable from the working tree
sys.path.insert(0, str(Path(__file__).resolve().parent))


LOOPBACK = 'tcp/127.0.0.1:17448'


# ------------------------------------------------------------------------
# CLAIM 1 (Copilot C1): Zenoh callbacks run on a non-asyncio thread.
# If true, scheduling onto core.loop via plain loop.create_task is unsafe.
# ------------------------------------------------------------------------
def claim1_zenoh_thread_check():
    print('\n=== CLAIM 1: Zenoh callback thread / asyncio safety ===')
    print('  fix: DistributedSession.subscribe marshals via core.loop.call_soon_threadsafe')
    from nicegui import core

    async def run_probe():
        loop_thread = threading.current_thread()
        loop = asyncio.get_running_loop()
        core.loop = loop  # simulate nicegui startup

        DistributedSession._instance = None
        sess = DistributedSession.__new__(DistributedSession)
        listener_cfg = zenoh.Config.from_json5(json.dumps({'listen': {'endpoints': [LOOPBACK]}}))
        sess.session = zenoh.open(listener_cfg)
        sess.instance_id = 'PROBE_A'
        sess.namespace = 'probe'
        sess.publishers = {}
        sess.subscribers = {}

        observed = {}

        def user_callback(data):
            observed['cb_thread'] = threading.current_thread()
            observed['cb_thread_name'] = threading.current_thread().name
            try:
                observed['cb_loop'] = asyncio.get_running_loop()
            except RuntimeError as e:
                observed['cb_loop_err'] = str(e)
            observed['data'] = data

        sess.subscribe('probe', user_callback)

        sender_cfg = zenoh.Config.from_json5(json.dumps({'connect': {'endpoints': [LOOPBACK]}}))
        s_send = zenoh.open(sender_cfg)
        s_send.declare_publisher(sess.wire_topic('probe')).put(
            json.dumps({'instance_id': 'PROBE_B', 'data': {'hello': 1}}).encode()
        )

        for _ in range(50):
            if observed:
                break
            await asyncio.sleep(0.1)

        sess.shutdown()
        s_send.close()

        print(f'  loop thread name:     {loop_thread.name}')
        print(f'  callback thread name: {observed.get("cb_thread_name")!r}')
        print(f'  callback == loop:     {observed.get("cb_thread") is loop_thread}')
        print(f'  get_running_loop:     {observed.get("cb_loop", "FAILED: " + observed.get("cb_loop_err", "?"))}')
        return observed.get('cb_thread') is loop_thread and 'cb_loop' in observed

    on_loop_thread = asyncio.run(run_probe())
    verdict = 'NO BUG' if on_loop_thread else 'BUG CONFIRMED'
    print(f'  >>> {verdict} <<<')
    return not on_loop_thread


# ------------------------------------------------------------------------
# CLAIM 2 (Claude C1): ui.run(distributed=...) under user simulation
# silently skips the DistributedSession.initialize() call.
# ------------------------------------------------------------------------
def claim2_user_sim_check():
    print('\n=== CLAIM 2: distributed= silent no-op under user simulation ===')
    print('  fix: under user simulation we now raise RuntimeError loudly instead of silently no-op')
    from nicegui import helpers
    from nicegui import ui_run as ui_run_mod

    # Force the user-sim branch
    original = helpers.is_user_simulation
    helpers.is_user_simulation = lambda: True
    DistributedSession._instance = None
    raised = None
    try:
        ui_run_mod.run(distributed=True, reload=False, show=False)
    except RuntimeError as e:
        raised = e
    except SystemExit:
        pass
    finally:
        helpers.is_user_simulation = original

    session = DistributedSession.get()
    print(f'  ui.run raised: {raised!r}')
    print(f'  DistributedSession.get(): {session!r}')
    # Bug WAS: silently ignored. Fix: raise loudly. Either fail-loud OR honoured init is "NO BUG".
    silently_ignored = (raised is None) and (session is None)
    verdict = 'BUG CONFIRMED' if silently_ignored else 'NO BUG'
    print(f'  >>> {verdict} <<<')
    return silently_ignored


# ------------------------------------------------------------------------
# CLAIM 3 (Claude C2): DistributedEvent.emit() fires LOCAL callbacks
# before session.publish() validates the payload. So non-JSON args =
# local already ran when publish raises.
# ------------------------------------------------------------------------
def claim3_emit_ordering_check():
    print('\n=== CLAIM 3: emit() fires locally BEFORE publish raises ===')
    print('  fix: payload is JSON-validated UPFRONT; local callbacks should not fire on bad payload')
    from nicegui.distributed_event import DistributedEvent

    DistributedSession._instance = None
    cfg = zenoh.Config.from_json5(json.dumps({'connect': {'endpoints': [LOOPBACK]}}))
    s = zenoh.open(cfg)
    sess = DistributedSession.__new__(DistributedSession)
    sess.session = s
    sess.instance_id = 'CLAIM3'
    sess.namespace = 'shared'
    sess.publishers = {}
    sess.subscribers = {}
    DistributedSession._instance = sess

    fired = []
    event = DistributedEvent[object]()
    event.subscribe(lambda x: fired.append(('local-fired-with', type(x).__name__)))

    raised = None
    try:
        event.emit({'an', 'unhashable', 'set'})
    except (TypeError, ValueError) as e:
        raised = e

    print(f'  local callbacks fired: {fired}')
    print(f'  emit raised:           {raised!r}')

    s.close()
    DistributedSession._instance = None

    bug = bool(fired) and (raised is not None)
    verdict = 'BUG CONFIRMED' if bug else 'NO BUG'
    print(f'  asymmetric (local fired AND remote raised): {bug}')
    print(f'  >>> {verdict} <<<')
    return bug


# ------------------------------------------------------------------------
# CLAIM 4 (Claude Important): default "shared" namespace cross-talks
# between unrelated deployments when no storage_secret is set.
# ------------------------------------------------------------------------
def claim4_shared_namespace_check():
    print('\n=== CLAIM 4: "shared" namespace cross-talks across deployments ===')
    print('  fix: DistributedSession now refuses to construct without storage_secret')
    rejected = []
    for label, secret in [('None', None), ('""', '')]:
        try:
            DistributedSession(True, storage_secret=secret)
            rejected.append((label, False, None))
        except ValueError as e:
            rejected.append((label, True, str(e)[:80]))
    for label, ok, err in rejected:
        print(f'  DistributedSession(True, storage_secret={label}): refused={ok}; err={err!r}')
    all_rejected = all(ok for _, ok, _ in rejected)
    verdict = 'NO BUG' if all_rejected else 'BUG CONFIRMED'
    print(f'  >>> {verdict} <<<')
    return not all_rejected


# ------------------------------------------------------------------------
# CLAIM 5 (Copilot C5): shutdown() is never hooked into app lifecycle.
# ------------------------------------------------------------------------
def claim5_shutdown_hook_check():
    print('\n=== CLAIM 5: DistributedSession.shutdown is never registered ===')
    print('  fix: initialize() should call core.app.on_shutdown(self.shutdown)')
    from nicegui import core
    DistributedSession._instance = None

    captured = []
    original_on_shutdown = core.app.on_shutdown
    core.app.on_shutdown = lambda h: (captured.append(h), original_on_shutdown(h))[1]
    try:
        DistributedSession.initialize(True, storage_secret='probe-c5')
    finally:
        core.app.on_shutdown = original_on_shutdown

    session = DistributedSession.get()
    bound_to_session_shutdown = any(
        getattr(h, '__func__', h) is DistributedSession.shutdown
        or getattr(h, '__self__', None) is session
        for h in captured
    )
    print(f'  on_shutdown handlers captured: {len(captured)}')
    print(f'  any bound to session.shutdown: {bound_to_session_shutdown}')

    if session is not None:
        session.shutdown()
    DistributedSession._instance = None

    verdict = 'NO BUG' if bound_to_session_shutdown else 'BUG CONFIRMED'
    print(f'  >>> {verdict} <<<')
    return not bound_to_session_shutdown


if __name__ == '__main__':
    results = {
        'C1 (Copilot) Zenoh thread / asyncio': claim1_zenoh_thread_check(),
        'C2 (Claude) user-sim silent no-op':   claim2_user_sim_check(),
        'C3 (Claude) emit-then-publish race':  claim3_emit_ordering_check(),
        'C4 (Claude) "shared" namespace':       claim4_shared_namespace_check(),
        'C5 (Copilot) shutdown not hooked':    claim5_shutdown_hook_check(),
    }
    print('\n=== SUMMARY ===')
    for name, confirmed in results.items():
        print(f'  {"BUG" if confirmed else "OK "}: {name}')
