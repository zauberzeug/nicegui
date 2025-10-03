# AI Agent Guidelines for NiceGUI

> **For**: AI assistants (Cursor, GitHub Copilot, etc.) working on NiceGUI codebase
> **Standards**: All coding standards are in [CONTRIBUTING.md](CONTRIBUTING.md) – follow those rules
> **Review**: For PR reviews, see [.github/copilot-instructions.md](.github/copilot-instructions.md)
> **Purpose**: Provide context and patterns specific to NiceGUI architecture

## Project Context

NiceGUI is a Python framework for building web UIs with a **backend-first philosophy**.
Key architectural decisions:

- **Backend-first**: All UI logic lives in Python; the framework handles web details
- **Tech stack**: Python/FastAPI backend, Vue/Quasar frontend, socket.io for communication
- **Single worker**: Uses one uvicorn worker (no multi-process synchronization needed)
- **Real-time communication**: WebSocket connection established after initial page load, kept open for client-server communication
- **User interactions**: All UI events are sent to backend and invoke Python functions

## AI-Specific Working Principles

### Pair Programming Approach

- **Discuss before implementing**: If approach is unclear, present options and trade-offs
- **Step-by-step for large changes**: Get confirmation before drastic refactorings
- **Think from first principles**: Question assumptions to find the true nature of problems

### Code Organization

- **High-level code first**: Put interesting logic at the top of files
- **Helpers below usage**: Functions called from high-level code should be close to, but below, their usage

## Critical Architecture Patterns

### Async/Event Loop

- **Never block the event loop**: All async handlers must stay non-blocking
- Use `asyncio.to_thread()` or executors for CPU-bound operations
- Clean up tasks on teardown
- Handle WebSocket resource cleanup properly

### API Stability

- `nicegui.*` is **public API** – breaking changes need deprecation paths
- New parameters must have sensible defaults for backward compatibility
- Validate user inputs at API boundaries

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

> This file complements [CONTRIBUTING.md](CONTRIBUTING.md). For style rules, formatting, and detailed contribution workflow, see CONTRIBUTING.md.
