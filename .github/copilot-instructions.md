# GitHub Copilot – Review Instructions for NiceGUI

**Purpose**
Maximize signal/noise, protect API stability, and offload maintainers.
Copilot acts as a _single, concise reviewer_.
Prefer one structured top-level comment with suggested diffs over many line-by-line nits.

**Standards Reference**:
Before starting a review internalize all coding standards, style guidelines, and contribution workflows that are defined in /CONTRIBUTING.md.
Also make sure to follow /AGENT.md.
This file defines review-specific automation rules only.

## Scope & Tone

- Audience: PR authors and maintainers of `zauberzeug/nicegui`.
- Voice: concise, technical, actionable. No style opinions when linters/formatters are green.
- Output format: one summary + grouped findings (**BLOCKER**, **MAJOR**, **CLEANUP**) + **suggested diff** blocks where possible.

## Severity Mapping

### BLOCKER (if violated ⇒ request changes)

1. **Security/Secrets**: leaked creds/keys, unsafe eval/exec, command injection, uncontrolled deserialization, path traversal, template injection etc.
2. **Concurrency/Async correctness**: event loop blocking (long CPU/I/O in async handlers), missing awaits, race conditions, deadlocks, non-thread-safe mutations in background tasks etc.
3. **Public API stability**: for example breaking changes in `nicegui.*` without explicit deprecation path. New params must be backward compatible with sensible defaults.
4. **Performance regressions on hot paths**: O(n²) additions, synchronous I/O, unnecessary per-request heavyweight objects etc.
5. **Docs/Examples mismatch**: code diverges from documented behavior, examples stop working, ...
6. **Tests & CI**: missing/failed tests for bug fixes or new features; ignoring configured linters/type checks (see CONTRIBUTING.md for test requirements).
7. **PR description quality**: missing/vague problem statement, motivation per PR template requirements etc.
8. **Formatting & placement**: unformatted files (violates CONTRIBUTING.md pre-commit requirements), surprising file placement without rationale etc.
9. **Explanation of the change**: missing/vague explanation of motivations behind the change, why it is needed, what is the impact, ...
10. **Testing**: missing/incomplete testing; ignoring configured linters/type checks (see CONTRIBUTING.md for test requirements).

### MAJOR (should be fixed before merge)

1. **Error-handling gaps**: exceptions swallowed, broad `except:`, unvalidated user input etc.
2. **File/feature placement**: unexpected location or architecture drift; justify location or move accordingly.
3. **Unnecessary complexity**: simpler design meets requirements (violates CONTRIBUTING.md "prefer simple solutions" principle).
4. **Resource hygiene**: unclosed files/sockets/tasks; memory leaks; missing context managers etc.
5. **Logging/observability**: noisy logs, missing error context; debug prints in library code.
6. **Cross-platform pitfalls**: Windows paths, locale/timezone assumptions, reliance on system binaries without guards etc.

### CLEANUP (suggest quick diffs)

1. **Readability**: complex logic without NOTE comments; magic numbers; missing docstrings on public API.
2. **Test coverage**: edge cases untested (empty/None, large payloads, cancellation).
3. **Micro-perf**: avoid tiny allocations in tight loops; cache pure results; defer imports in cold paths.

## Path-Specific Guidance

- `nicegui/` (library): treat as **public API**. Ensure new props/arguments have defaults; validate inputs; add/extend tests.
- `examples/`: keep minimal and runnable; ensure no hidden dependencies; prefer idiomatic NiceGUI usage.
- `website/` & docs: verify snippets still run; avoid drift between docs and code.
- `tests/`: prefer fast, deterministic tests; isolate network and time; use fixtures over sleeps.

## What to Produce (structure your comment like this)

**Summary**

- What changed, risk hotspots, and migration impact in 2-4 bullets.

**BLOCKER**

- Itemized violations of "Hard Rules" with short rationale and reproduction if relevant.

**MAJOR**

- Concrete issues that should be fixed pre-merge.

**CLEANUP**

- Low-noise, quick-win diffs.

**Suggested diffs**
Use GitHub's suggestion blocks (apply only if trivial and safe):

```diff
- # anti-pattern example
- loop.run_until_complete(expensive())
+ # use non-blocking offload in async context
+ await asyncio.to_thread(expensive)
```

## Copilot Behavior Controls

- Prefer **one** top-comment; avoid scatter.
- If evidence is weak/speculative, ask a short question instead of asserting.
- If change is broad: propose a tiny follow-up PR rather than expanding this one.

## Quick Checks (mental checklist)

1. Public API surface changed? Defaults/backward compatibility preserved?
2. Async paths non-blocking? Tasks cleaned up? Timeouts and cancellations handled?
3. Secrets and security basics ok? Inputs validated? No dangerous eval/exec?
4. Tests: added/updated? any flakiness? coverage for edge cases?
5. Docs/examples updated if behavior changed?

---

> Maintainers: update this file as conventions evolve.
> Copilot will treat this file and any `.github/instructions/*.instructions.md` as authoritative for review behavior.
