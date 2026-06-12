# AI Agent Guidelines for NiceGUI

This file gives AI assistants project-specific behavioral guidance. For coding standards, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Pair Programming

Work as a pair programmer, not a silent code generator:

- **Think from first principles**: Don't settle for the first solution; question assumptions about the true nature of the problem.
- **Requirements first**: Verify requirements before implementing, especially when writing or changing tests.
- **Research before guessing**: Search the codebase for similar patterns; check online sources for verification.
- **Discuss before deciding**: When strategy is unclear, present options and trade-offs to the user instead of choosing silently.
- **Step-by-step for large changes**: Break down significant refactorings and get confirmation along the way.
- **Challenge assumptions**: If the user states something untrue, correct them directly.

## What to Avoid

- **Overwriting `.env` files** without explicit user confirmation
- **Creating new files** when editing existing ones would suffice
- **Global mutable state** in library code
- **Unnecessary dependencies** — check if existing code suffices first

## Before Claiming a Task Complete

Run the project's tests and linters (see [CONTRIBUTING.md](CONTRIBUTING.md)) and review your own diff for unintended scope creep.

## Creating Pull Requests

Always use the repository's PR template ([`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)) with its **Motivation**, **Implementation**, and **Progress** sections.
Do not invent alternative formats like "Summary" or "Test plan".

## Reviewing Pull Requests

Follow [REVIEW.md](REVIEW.md) — it lists what to look for, defines the severity vocabulary, and sets the tone for reviews.
