---
name: fix-dependabot-alert
description: Fix one or more Dependabot security alerts by updating the affected packages, rebuilding bundles and vendored files, and preparing a commit. Use when asked to fix Dependabot alerts (e.g. "fix Dependabot alert 252", "fix all new Dependabot alerts").
---

Fix the Dependabot alerts whose numbers are passed as arguments.
If no numbers are given or the user asks for "all new" alerts, fetch all open ones:

```
gh api 'repos/zauberzeug/nicegui/dependabot/alerts?state=open'
```

## Python alerts (`uv.lock`)

Alerts on `uv.lock` are fixed by a pin in `pyproject.toml`, not by only re-locking:
add `"<pkg>>=<patched>",  # https://github.com/zauberzeug/nicegui/security/dependabot/<number>` to the section that pulls the package in
(`dependencies` for runtime deps, the `dev` group for test-only deps; append `, for <parent>` if it is transitive — `uv tree --invert --package <pkg>` shows the parents),
then run `uv lock` and check that the patched version satisfies `requires-python`.
Commit `pyproject.toml` and `uv.lock` together; `DEPENDENCIES.md` only covers npm packages and stays unchanged.

## Prebuilt bundles (plotly, json_editor, mermaid)

Three elements ship code that upstream built with dependencies compiled in:

- plotly imports `plotly.js/dist/plotly.min.js`, which contains all of plotly's dependencies (e.g. `maplibre-gl`, `probe-image-size`).
- json_editor imports `vanilla-jsoneditor`, which contains svelte and its UI dependencies (e.g. `svelte-select`, `@floating-ui/dom`); its other dependencies are bundled from our lockfile.
- mermaid depends on `@mermaid-js/parser`, which contains `langium`, `chevrotain`, `vscode-jsonrpc` and its own copy of `lodash-es`; mermaid's other dependencies are bundled from our lockfile.

Alerts on these compiled-in dependencies can not be fixed in the lockfile:
`npm update` or an override closes the alert, but `dist/` still ships the vulnerable code.
Leave such an alert open and tell the user;
it is fixed by upgrading the parent package once a release contains the patched version (grep the upstream file to check).
All other dependencies are built from package sources, so their lockfiles decide what ships.
The `@iconify/utils` override in mermaid is deliberate: 3.1 generates short icon ids such as `c1` that collide with NiceGUI's element ids, so do not bump it to fix an alert without checking the ids.

## Steps (npm alerts)

01. **Fetch each alert** to identify the package, manifest path, and first patched version:

    ```
    gh api repos/zauberzeug/nicegui/dependabot/alerts/<number>
    ```

02. **Try the minimal fix first** — `npm update <pkg>` inside the manifest's directory.
    If the existing semver range in the parent's `package.json` already allows the patched version, this is enough and `package.json` stays untouched.

03. **Escalate to an npm override** if the patched version is outside the declared range (common for transitive deps).
    Add the package to the `overrides` section of the manifest's `package.json` with a range that includes the patched version, then run `npm install`.

04. **Rebuild if the element has a `dist/`** — run `npm run clean && npm run build` in the manifest's directory, so that chunks with old content hashes do not stay behind.
    Don't hand-revert the `dist/` changes; let pre-commit hooks normalize any whitespace-only noise (the end-of-file-fixer will handle source-map trailing newlines).

05. **Rebuild vendored core libraries if the root manifest changed** — run `npm run build` in the repository root; it runs `extract_core_libraries.py` to refresh `nicegui/static/`.
    Whitespace-only churn in unrelated static files is normalized away by the pre-commit hooks.

06. **Scan other lockfiles** in the repo for the same vulnerable package — sometimes Dependabot is slow to raise the next alert:

    ```
    find . -name 'package-lock.json' -not -path '*/node_modules/*' -not -path '*/.venv/*'
    ```

    Check each one for the package and apply the same fix if needed.

07. **Check for other open alerts** that might as well be bundled into the same commit:

    ```
    gh api 'repos/zauberzeug/nicegui/dependabot/alerts?state=open'
    ```

08. **Regenerate `DEPENDENCIES.md`** — run `python3 summarize_dependencies.py`; it rewrites the file from the resolved lockfile versions and belongs in the same commit.

09. **Confirm with the user before committing.** Then commit with a message following the established style:

    - Single alert: `fix Dependabot alert 252`
    - Multiple: `fix Dependabot alerts 250 and 251` or `fix Dependabot alerts 246, 247, 248 and 249`

    Reference alert numbers as plain integers, **never** as `#252` — GitHub auto-links `#N` to issues/PRs, which points to the wrong ticket.

10. **Do not push** unless the user explicitly asks.
