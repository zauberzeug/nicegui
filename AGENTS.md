# AI Agent Guidelines for NiceGUI

> **For**: AI assistants (Cursor, GitHub Copilot, Codex, etc.) working on NiceGUI codebase
> **About**: The project, examples and architecture is described in [README.md](README.md) > **Standards**: All coding standards are in [CONTRIBUTING.md](CONTRIBUTING.md) – follow those rules

## Core Principles

### Think from First Principles

Don't settle for the first solution.
Question assumptions and think deeply about the true nature of the problem before implementing.

### Pair Programming Approach

We work together as pair programmers, switching seamlessly between driver and navigator:

- **Requirements first**: Verify requirements are correct before implementing, especially when writing/changing tests
- **Discuss strategy**: Present options and trade-offs when uncertain about approach
- **Step-by-step for large changes**: Break down significant refactorings and get confirmation at each step
- **Challenge assumptions**: If the user makes wrong assumptions or states untrue facts, correct them directly

### Simplicity First

- Prefer simple, straightforward solutions
- Avoid over-engineering
- Remove obsolete code rather than working around it
- Code should be self-explanatory

## Code Organization

- **High-level code first**: Put interesting logic at the top of files
- **Helpers below usage**: Functions called from high-level code should be close to, but below, their usage
- **Keep files focused**: Aim for under 200-300 lines per file; suggest refactorings when larger

## Async/Event Loop

- **Never block the event loop**: All async handlers must stay non-blocking
- **Never use `asyncio.create_task()`** – The garbage collector might remove unfinished tasks
- Use appropriate methods based on operation type:
  - `run.cpu_bound()` for CPU-intensive operations
  - `run.io_bound()` for blocking I/O operations
  - `background_tasks.create()` for background tasks that need proper lifecycle management
- Clean up background tasks on teardown
- Handle resource cleanup properly in async contexts

## API Stability

- `nicegui.*` is **public API** – breaking changes need deprecation paths
- New parameters must have sensible defaults for backward compatibility
- Validate user inputs at API boundaries for critical operations

## Common Patterns

### Element Creation

Look at similar elements in `nicegui/elements/` for patterns on initialization, props handling, and event binding.

## What to Avoid

- **Global mutable state** in library code
- **Blocking I/O** in async handlers or WebSocket paths
- **Broad exception catching** without proper error context
- **Debug prints** in library code (use proper logging)
- **Unnecessary dependencies** – check if existing code suffices
- **Duplicate logic** – consolidate when introducing new patterns
- **Overwriting .env files** without explicit user confirmation
- **Creating new files** when editing existing ones would suffice

## Path-Specific Context

- `nicegui/` – Core library (public API), highest stability requirements
- `examples/` – Standalone demos, must be minimal and runnable
- `website/` – Documentation site, keep in sync with code behavior
- `tests/` – Test suite, prefer pytest patterns
- `main.py` – Runs the nicegui.io website locally

## Quick Verification

Before claiming a task complete, verify:

1. No blocking operations in async code?
2. Public API backward compatible?
3. Tests passing? (see CONTRIBUTING.md)
4. Linters passing? (see CONTRIBUTING.md)
5. Debug code removed?

## When Uncertain

- **Check online sources** for inspiration or verification rather than guessing
- **Search the codebase** for similar patterns before inventing new ones
- **Ask the user** by presenting options and trade-offs if strategy is unclear
- **Start broad, then narrow**: Explore with semantic search, then drill into specific files

---

## Code Review Guidelines

**Purpose**: Maximize signal/noise, protect API stability, and offload maintainers.
Act as a _single, concise reviewer_.
Prefer one structured top-level comment with suggested diffs over many line-by-line nits.

**Standards Reference**: Before starting a review, internalize all coding standards, style guidelines, and contribution workflows defined in CONTRIBUTING.md and the principles above.

### Scope & Tone

- Audience: PR authors and maintainers of `zauberzeug/nicegui`
- Voice: concise, technical, actionable. No style opinions when linters/formatters are green
- Output format: one summary + grouped findings (**BLOCKER**, **MAJOR**, **CLEANUP**) + **suggested diff** blocks where possible

### Severity Mapping

#### BLOCKER (if violated ⇒ request changes)

1. **Security/Secrets**: leaked creds/keys, unsafe eval/exec, command injection, uncontrolled deserialization, path traversal, template injection
2. **Concurrency/Async correctness**: event loop blocking (long CPU/I/O in async handlers), missing awaits, race conditions, deadlocks, using `asyncio.create_task()` instead of `background_tasks.create()`, non-thread-safe mutations in background tasks
3. **Public API stability**: breaking changes in `nicegui.*` without explicit deprecation path. New params must be backward compatible with sensible defaults
4. **Performance regressions on hot paths**: O(n²) additions, synchronous I/O, unnecessary per-request heavyweight objects
5. **Docs/Examples mismatch**: code diverges from documented behavior, examples stop working
6. **Tests & CI**: missing or incomplete tests; ignoring configured linters/type checks (see [CONTRIBUTING.md](CONTRIBUTING.md) for test requirements)
7. **PR description quality**: missing/vague problem statement, motivation per PR template requirements
8. **Formatting & placement**: unformatted files (violates [CONTRIBUTING.md](CONTRIBUTING.md) pre-commit requirements), surprising file placement without rationale
9. **Explanation of the change**: missing/vague explanation of motivations behind the change, why it is needed, what is the impact

#### MAJOR (should be fixed before merge)

1. **Error-handling gaps**: exceptions swallowed, broad `except:`, unvalidated user input
2. **File/feature placement**: unexpected location or architecture drift; justify location or move accordingly
3. **Unnecessary complexity**: simpler design meets requirements (violates [CONTRIBUTING.md](CONTRIBUTING.md) "prefer simple solutions" principle)
4. **Resource hygiene**: unclosed files/sockets/tasks; memory leaks; missing context managers
5. **Logging/observability**: noisy logs, missing error context; debug prints in library code
6. **Cross-platform pitfalls**: Windows paths, locale/timezone assumptions, reliance on system binaries without guards

#### CLEANUP (suggest quick diffs)

1. **Readability**: complex logic without NOTE comments; magic numbers; missing docstrings on public API
2. **Test coverage**: edge cases untested (empty/None, large payloads, cancellation)
3. **Micro-perf**: avoid tiny allocations in tight loops; cache pure results; defer imports in cold paths

### Path-Specific Guidance

- `nicegui/` (library): treat as **public API**. Ensure new props/arguments have defaults; validate inputs; add/extend tests
- `examples/`: keep minimal and runnable; ensure no hidden dependencies; prefer idiomatic NiceGUI usage
- `website/` & docs: verify snippets still run; avoid drift between docs and code
- `tests/`: prefer fast, deterministic tests; isolate network and time; use fixtures over sleeps

### Review Structure

Structure your review comment like this:

**Summary**

What changed, risk hotspots, and migration impact in 2-4 bullets.

**BLOCKER**

Itemized violations of critical rules with short rationale and reproduction if relevant.

**MAJOR**

Concrete issues that should be fixed pre-merge.

**CLEANUP**

Low-noise, quick-win improvements.

**Suggested diffs**

Use GitHub's suggestion blocks (apply only if trivial and safe):

```diff
- data = Path('config.json').read_text()
+ with Path('config.json').open() as f:
+     data = f.read()
```

### Review Behavior

- Prefer **one** top-comment; avoid scatter
- If evidence is weak/speculative, ask a short question instead of asserting
- If change is broad: propose a tiny follow-up PR rather than expanding this one

### Review Checklist

Mental checklist before posting review:

1. Public API surface changed? Defaults/backward compatibility preserved?
2. Async paths non-blocking? Tasks cleaned up? Timeouts and cancellations handled?
3. Secrets and security basics ok? Inputs validated? No dangerous eval/exec?
4. Tests: added/updated? any flakiness? coverage for edge cases?
5. Docs/examples updated if behavior changed?

---

> This file complements [CONTRIBUTING.md](CONTRIBUTING.md).
> For style rules, formatting, and detailed contribution workflow, see CONTRIBUTING.md.
>
> Maintainers: update this file as conventions evolve.
