# Code Review Guidelines for NiceGUI

This file augments any review prompt — the built-in `/review` command, Cursor commands, or an ad-hoc "review this" request.
It defines _what to look for_, _how far to trust the pull request_, and _how to label severity_, but leaves the layout to whatever invokes the review.
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
  - Missing test for a new feature or bug fix, with no reason given in the pull request
  - Tests coupled to implementation details — private attributes, call counts, patched internals, fake request objects — where the user-visible effect could be asserted instead
  - Test cost out of proportion to the risk: a `Screen` test where the `User` fixture would do, elaborate scaffolding for a marginal edge case (see [CONTRIBUTING.md](CONTRIBUTING.md#coding-conventions))
  - Untested edge cases: empty/None, large payloads, cancellation
  - Flaky, time-dependent, or network-dependent tests
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
  - Tests asserting CPython-only semantics — immediate weakref cleanup via refcounting, exact CPython error-message wording — need a PyPy `skipif` or a tolerant match (PyPy compatibility is tracked externally, not promised)
- **Readability**
  - Complex logic without comments explaining intent; magic numbers

## How far to trust the pull request

A pull request's measurements, mechanisms and root-cause stories are the author's hypotheses, not evidence.
Review what the code does, not what the description says it does.

- Re-derive load-bearing claims yourself: rebuild the artifact, run the reproduction, read the upstream source.
  A number, a benchmark or a "this is why it happens" that nobody re-checked is an open question, not a finding.
- When a fix depends on undocumented behavior of an upstream or vendored library, ask for a test against the real library, so an upstream change fails loudly instead of silently.
- A reported bug is a sample, not the population.
  Before merging, look for the same shape elsewhere in the codebase and say what you found.
- The same caution applies to your own findings.
  Before reporting existing behavior as a defect, check that nobody chose it: the source shows what the code does, not whether it was intended.
  Search the tracker for the symptom, and `git blame` the warning or guard being flagged — or `git log -S` it when the string is stable — to find the pull request that introduced it, because a deliberate trade-off and a defect look identical in the diff.

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
