# Code Review Guidelines for NiceGUI

This file augments any review prompt — the built-in `/review` command, Cursor commands, or an ad-hoc "review this" request.
It defines _what to look for_ and _how to label severity_, but leaves the layout to whatever invokes the review.
For coding rules, see [CONTRIBUTING.md](CONTRIBUTING.md); for general agent guidance, see [AGENTS.md](AGENTS.md).

## What to look for

- **Security**
  - Leaked credentials, secrets, or API keys
  - Unsafe `eval`/`exec`, command injection, uncontrolled deserialization, path traversal, template injection
  - Unvalidated user input at API boundaries
- **Async & concurrency**
  - Blocking I/O inside `async def` (CPU-bound work, sync file I/O, blocking network calls)
  - Missing `await`, race conditions, deadlocks
  - `asyncio.create_task()` instead of `background_tasks.create()` — the GC may drop unfinished tasks
  - Non-thread-safe mutations from background tasks
- **Public API stability** (`nicegui.*`)
  - Breaking changes without an explicit deprecation path
  - New parameters without backward-compatible defaults
- **Performance**
  - O(n²) work on hot paths, synchronous I/O in request handlers, heavyweight objects per request
  - Tight-loop allocations; cache pure results; defer cold-path imports
- **Error handling**
  - Exceptions swallowed silently, broad `except:` clauses
  - Missing input validation at system boundaries
- **Resource hygiene**
  - Unclosed files, sockets, or tasks; missing context managers; memory leaks
- **Logging & observability**
  - Noisy logs, missing error context, debug prints in library code
- **Tests**
  - New features and bug fixes need tests (see CONTRIBUTING.md for `User` vs `Screen` fixture choice)
  - Edge cases: empty/None, large payloads, cancellation
  - Flakiness, time-dependence, hidden network deps
- **Docs & examples**
  - Code that diverges from documented behavior
  - Examples that no longer run
  - Missing docstrings on the public API surface
- **Formatting & placement**
  - Files unformatted (violates pre-commit)
  - Surprising file placement without rationale; architecture drift
- **PR description**
  - Missing or vague motivation per [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)
  - Unclear problem statement or impact
- **Cross-platform**
  - Windows path assumptions, locale/timezone hardcoding, reliance on system binaries without guards
- **Readability**
  - Complex logic without `# NOTE:` comments explaining intent; magic numbers

## Severity vocabulary

Present findings as a numbered list, with the severity label in parentheses after the title:

```
1. **Title of the finding** (major) — body explaining the issue and the suggested fix.
```

Labels:

- **blocking** — security holes, broken public API, broken tests, failing CI, examples that stop working, missing PR motivation. Worth requesting changes.
- **major** — error-handling gaps, unnecessary complexity, resource leaks, cross-platform pitfalls, surprising placement. Worth addressing pre-merge but not strictly blocking.
- **minor** — readability nits, missing docstrings, edge-case test gaps, micro-perf. Reviewer's leave-or-take.

When the severity is obvious from the finding, the label can be omitted.
For long reviews, findings can be grouped under severity sub-headings (`### Blocking`, `### Major`, `### Minor`) — restart numbering in each.

## Path-specific guidance

- `nicegui/` (library): treat as **public API**. Defaults on new args; validate inputs; add or extend tests
- `examples/`: keep minimal and runnable; no hidden dependencies; idiomatic NiceGUI
- `website/` and docs: verify snippets still run; avoid drift between docs and code
- `tests/`: prefer fast, deterministic tests; isolate network and time; fixtures over sleeps

## Tone & behavior

- Concise, technical, actionable. No style opinions when linters/formatters are green.
- Use GitHub suggestion blocks for trivial, safe diffs.
- If evidence is weak, ask a question instead of asserting.
- If the change is broad, propose a small follow-up PR rather than expanding this one.
- Drop `#L...` line anchors in file links — they don't render in PR comments. Put the line range in the link text or prose instead.
