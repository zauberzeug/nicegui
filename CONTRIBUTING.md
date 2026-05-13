# Contributing to NiceGUI

We're thrilled that you're interested in contributing to NiceGUI!
Here are some guidelines that will help you get started.

We follow a [Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you agree to abide by its terms.

## About NiceGUI

NiceGUI is a Python library for building web-based user interfaces with minimal code.
It's designed to be simple, powerful, and fun to use.

### Project Structure

- `nicegui/` - Core library code (public API)
- `nicegui/elements/` - Built-in UI elements
- `nicegui/functions/` - Utility functions
- `examples/` - Standalone example applications
- `website/` - Documentation site (nicegui.io)
- `tests/` - Test suite
- `main.py` - Runs the documentation website locally

### Tech Stack

- **Python 3.10+** - Core language
- **FastAPI/Starlette** - Web framework
- **Vue 3** - Frontend framework
- **Quasar** - UI component framework
- **Tailwind CSS 4** - Styling
- **pytest** - Testing framework

## Ways to contribute

There are several ways to help out, depending on what you want to do:

- **Report a bug or request a feature** → see [Reporting issues](#reporting-issues)
- **Report a security vulnerability** → see [Reporting security vulnerabilities](#reporting-security-vulnerabilities)
- **Beta-test the development version** → see [Beta-testing](#beta-testing)
- **Contribute code or documentation** → see [Contributing code and documentation](#contributing-code-and-documentation)
- **Create video or tutorial content** → see [Video and tutorial content](#video-and-tutorial-content)

For non-trivial work, please discuss your approach with maintainers before implementing.
If you're unsure, present options and trade-offs first.
For larger changes, work step-by-step and confirm direction with maintainers along the way.

## Reporting issues

> [!IMPORTANT]
> If you've found a security vulnerability, do **not** open a public issue.
> See [Reporting security vulnerabilities](#reporting-security-vulnerabilities) instead.

If you encounter a bug or other issue with NiceGUI, please [open a new issue](https://github.com/zauberzeug/nicegui/issues/new/choose) using one of the templates.
Provide a clear and concise description of the problem, including any relevant error messages and code snippets.
If possible, include steps to reproduce the issue.

## Reporting security vulnerabilities

Security issues are handled through GitHub's private vulnerability reporting, not public issues, so we can discuss and patch in a secure workspace before disclosure.

See [SECURITY.md](SECURITY.md) for the full policy and the supported reporting channels.

## Beta-testing

If you have an existing NiceGUI project, you can help us catch regressions before they ship by running it against the development version:

```bash
pip install -U git+https://github.com/zauberzeug/nicegui.git@main
```

If anything breaks, behaves worse than the current release, or feels off, please [open an issue](https://github.com/zauberzeug/nicegui/issues/new/choose).

## Contributing code and documentation

We are excited that you want to contribute to NiceGUI.
We're always looking for bug fixes, performance improvements, new features, and documentation improvements.

### Set up your environment

First, fork the repository on GitHub and clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/nicegui.git
cd nicegui
```

Then pick a development setup that fits your workflow:

**Option 1: Dev Container** — the simplest way. Start our Dev Container in VS Code:

1. Ensure you have VS Code, Docker and the Dev Containers extension installed.
2. Open the project root directory in VS Code.
3. Press `F1`, type `Dev Containers: Open Folder in Container`, and hit enter (or use the bottom-left corner icon in VS Code to reopen in container).
4. Wait until the image has been built. (On first launch, watch the terminal for a GitHub authentication prompt.)
5. Happy coding.

**Option 2: Locally** — you need Python 3.10+ and [uv](https://docs.astral.sh/uv/) installed.

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install NiceGUI in editable mode with all dependencies:

```bash
uv sync
```

This installs the `nicegui` package in editable mode, so code changes are reflected immediately.
You can also use your local version of NiceGUI in other projects.
To run the tests you need some additional setup which is described in [tests/README.md](tests/README.md).

**Option 3: Plain Docker** — start the development container:

```bash
./docker.sh up app
```

By default, the development server listens to http://localhost:80/.

The configuration is written in the `docker-compose.yml` file and automatically loads the `main.py` which contains the website https://nicegui.io.
Every code change will result in reloading the content.
We use Python 3.10 as a base to ensure compatibility (see `development.dockerfile`).

To view the log output, use the command:

```bash
./docker.sh log
```

> [!TIP]
> Open `nicegui.code-workspace` in VSCode with the recommended extensions to format on save while you work.

### Coding conventions

The conventions below cover both general Python style and NiceGUI-specific patterns.

- **Principles**

  - Always prefer simple solutions
  - Avoid duplication — check the codebase for similar functionality before adding new patterns
  - Remove obsolete code rather than working around it
  - When fixing bugs, exhaust existing patterns before introducing new ones; if you must introduce a new one, remove the old approach so logic doesn't duplicate

- **Style**

  - Follow **PEP 8** with a 120 character line length
  - Use single quotes in Python, double quotes in JavaScript
  - Use f-strings wherever possible (mark performance-critical exceptions with `# NOTE:`)
  - Use `# NOTE:` prefix for important implementation details and non-obvious code
  - No mutable defaults (`[]`, `{}`) without `# noqa: B006` and a justification — prefer `None`
  - Put high-level/interesting code at the top of files; helper functions go below their usage
  - Each sentence in documentation goes on a new line ([why](https://nick.groenen.me/notes/one-sentence-per-line/))

- **Async and background tasks**

  - No blocking I/O in async code — sync I/O blocks the event loop and freezes every connected client
  - Use `background_tasks.create()`, never `asyncio.create_task()` — the garbage collector might drop unfinished tasks
  - Use `helpers.should_await()` to check if a result should be awaited
  - Use `helpers.expects_arguments()` to check if a handler expects arguments
  - Use `core.app.handle_exception()` for exceptions in background tasks

- **Error handling**

  - Use `with contextlib.suppress(...)` instead of try/except/pass for cleaner exception handling
  - Catch `ImportError` for optional dependencies, not `ModuleNotFoundError` — covers both missing and broken installations
  - Use assertions for internal invariants (e.g., `assert self.current_scene is not None`)
  - Raise descriptive exceptions (`ValueError`, `RuntimeError`) with helpful messages

- **Elements** (core library)

  - **Mixins**: Elements use mixin composition; inheritance order matters for Python's Method Resolution Order (MRO)
  - **Props vs. attributes**: Use `self._props` for data that syncs to Vue/frontend; use instance attributes for Python-only state
  - **Context managers**: Elements can be used as context managers (`with element:`) for slot/child management
  - **Component registration**: Use class parameters for components: `component='file.js'`, `esm={'package': 'dist'}`, `default_classes='css-class'`

- **Memory** (core library)

  - **Weakref pattern**: Use `self._element = weakref.ref(element)` to avoid circular references (which require more costly garbage collection).
    When dereferencing, always check for `None`: `element = self._element(); if element is not None: element.update()`
  - **WeakValueDictionary**: Use for caches that shouldn't prevent garbage collection by means of CPython's reference counting

- **Binding** (core library)

  - **BindableProperty**: Use with `cast(Self, sender)` in on-change handlers for type safety
  - **Triple underscore storage**: BindableProperty stores values in `___property_name` attributes
  - **Batch updates**: Use `suspend_updates()` context manager when changing properties in `update()` to avoid infinite cycles

- **Method chaining**: Methods that support chaining (fluent interface) return `Self` from `typing_extensions`, enabling the builder pattern.
  When chaining, use backslash line continuation:

  ```python
  ui.button('Click me') \
      .classes('bg-green') \
      .on('click', lambda: ui.notify('Hello'))
  ```

- **Dataclasses**: Prefer `@dataclass(kw_only=True, slots=True)`

- **Tests**: Include tests for new features and bug fixes. Prefer the `User` fixture (fast, runs in the same async context as NiceGUI, no browser); use the `Screen` fixture only when testing browser/JavaScript interactions.

### Before submitting a pull request

Run these from the project root:

1. **Format and lint** with pre-commit:

   ```bash
   uv run pre-commit run --all-files
   ```

   Hooks are installed by `uv sync` (run `uv run pre-commit install` once if they aren't).
   They run autopep8 (120 char line length), `ruff check . --fix`, trailing-whitespace removal, end-of-file fixing, and single-quote enforcement.

   > [!TIP]
   > If pre-commit fails with `RuntimeError: failed to find interpreter for Builtin discover of python_spec='python3.10'`, install Python 3.10 and make sure it's available in your `PATH`.

2. **Run tests** with pytest:

   ```bash
   uv run pytest
   ```

   Tests require python-selenium with ChromeDriver — see [tests/README.md](tests/README.md) for setup.

3. **Add documentation** for new features and behavior changes:

   - **Element demos** live in `website/documentation/content/<element>_documentation.py`.
     Use `@doc.demo(ui.some_new_element)` for the main description (the docstring is shown as description text, in restructured-text) and `@doc.demo('Title', 'Description')` for additional interactive demos.
     Reference the page from `website/documentation/content/section_*.py` via `@doc.intro(...)`.
     Update `website/documentation/content/overview.py` with a link to the new element.
   - **Standalone examples** live in `examples/`.
     Keep each focused on one concept and as minimal as possible.
     To properly render on the website, they need to contain a README.md with
     at least a title (level 1 heading),
     a one-sentence description and
     a screenshot of the running example (960x540 WEBP).

### Submitting a pull request

1. **Create a feature branch** (e.g., `git checkout -b fix-button-alignment` or `git checkout -b add-dark-mode`)
2. **Commit** your changes to your branch
3. **Push** your feature branch to your fork (e.g., `git push origin fix-button-alignment`)
4. Open a **pull request (PR)** from your feature branch with a detailed description of your changes
   (the PR button is shown on the GitHub website of your forked repository)

> [!IMPORTANT]
> Always work on a feature branch, never on `main`:
>
> 1. Working on `main` blocks you from contributing to multiple things simultaneously,
> 2. It highly increases the chance of an unclean commit history,
> 3. Your `main` branch should stay in sync with the upstream repository.

> [!NOTE]
> **AI co-authorship:** if you used an AI assistant to help write your PR, please check that the commit message includes a `Co-authored-by:` trailer.
> Some agents add it automatically; others don't, and some silently **remove** existing ones when amending or rebasing.
> If missing, add the appropriate line (PRs are welcome to add lines for other agents):
>
> ```
> Co-authored-by: copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>
> Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
> Co-authored-by: opencode <noreply@opencode.ai>
> ```

## Video and tutorial content

We welcome and support video and tutorial contributions to the NiceGUI community!
Creating and sharing tutorials or showcasing projects using NiceGUI can be an excellent way to help others learn and grow,
while also spreading the word about our library.

Please note that NiceGUI is pronounced like "nice guy," which might be helpful to know when creating any video content.

If you decide to create YouTube content around NiceGUI,
we kindly ask that you credit our repository, our YouTube channel, and any relevant videos or resources within the description.
By doing so, you'll be contributing to the growth of our community and helping us receive more amazing pull requests and feature suggestions.

We're thrilled to see your creations and look forward to watching your videos. Happy video-making!

## For maintainers

### Updating node dependencies

We use `package.json` files to pin the versions of node dependencies.
There is one in the root directory for core dependencies and additional ones in `nicegui/elements/.../` directories for individual UI elements.
They are usually updated during major releases.

To update or add a dependency:

1. Use `npm` or other tools to modify the `package.json` file.
2. Run `npm install` to install the new dependencies. Any conflicts will be caught at this point.
3. Run `npm run build` to copy the dependencies into the `nicegui/static/` directory or to bundle them in the `nicegui/elements/.../` directories.

### Updating other resources

The following scripts update various resources:

- `deploy.py` — deploys nicegui.io to Fly.io
- `extract_core_libraries.py` — extracts core JS/CSS libraries from `node_modules` into `nicegui/static/`
- `fetch_google_fonts.py` — fetches the Google Fonts
- `fetch_languages.py` — updates the list of supported languages in `language.py`
- `fetch_milestone.py` — prepares the release notes for a given milestone
- `fetch_sponsors.py` — updates the list of sponsors on the website and in `README.md`
- `summarize_dependencies.py` — updates `DEPENDENCIES.md`
- `set_scale.sh` — sets the Fly.io machine count per region for nicegui.io

## Thank you!

Thank you for your interest in contributing to NiceGUI!
We're looking forward to working with you!
