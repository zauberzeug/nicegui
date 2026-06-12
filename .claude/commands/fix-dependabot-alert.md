Fix Dependabot alert $ARGUMENTS.

## Steps

1. **Fetch the alert** to identify the package, manifest path, and first patched version:

   ```
   gh api repos/zauberzeug/nicegui/dependabot/alerts/$ARGUMENTS
   ```

2. **Try the minimal fix first** — `npm update <pkg>` inside the manifest's directory. If the existing semver range in the parent's `package.json` already allows the patched version, this is enough and `package.json` stays untouched.

3. **Escalate to an npm override** if the patched version is outside the declared range (common for transitive deps). Add the package to the `overrides` section of the manifest's `package.json` with a range that includes the patched version, then run `npm install`.

4. **Rebuild if the element has a `dist/`** — run `npm run build` in the manifest's directory. Don't hand-revert the `dist/` changes; let pre-commit hooks normalize any whitespace-only noise (the end-of-file-fixer will handle source-map trailing newlines).

5. **Scan other lockfiles** in the repo for the same vulnerable package — sometimes Dependabot is slow to raise the next alert:

   ```
   find . -name 'package-lock.json' -not -path '*/node_modules/*' -not -path '*/.venv/*'
   ```

   Check each one for the package and apply the same fix if needed.

6. **Check for other open alerts** that might as well be bundled into the same commit:

   ```
   gh api 'repos/zauberzeug/nicegui/dependabot/alerts?state=open'
   ```

7. **Confirm with the user before committing.** Then commit with a message following the established style:

   - Single alert: `fix Dependabot alert 252`
   - Multiple: `fix Dependabot alerts 250 and 251` or `fix Dependabot alerts 246, 247, 248 and 249`

   Reference alert numbers as plain integers, **never** as `#252` — GitHub auto-links `#N` to issues/PRs, which points to the wrong ticket.

8. **Do not push** unless the user explicitly asks.
