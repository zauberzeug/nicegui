---
name: advisory-text
description: Write the publication text (title and description) of a NiceGUI security advisory and patch it into the advisory via the API. Use when asked to prepare an advisory for publication (e.g. "prepare GHSA-xxxx-xxxx-xxxx for publication", "write the advisory text").
---

Rewrite the advisory whose GHSA ID is passed as an argument for publication.
The submitted report is written for the maintainers (proof of concept, code quotes, internal class names);
the published text is read by application developers who want to know whether they are affected and what to do.
The submitted version stays in the advisory history, so nothing is lost by replacing it.

## Steps

1. **Read the advisory** and the fix (the merged PR or the commit on `main`):

   ```
   gh api repos/zauberzeug/nicegui/security-advisories/<ghsa-id>
   ```

2. **Read a published advisory** to match the voice, e.g. GHSA-p92q-2755-mhgh:

   ```
   gh api repos/zauberzeug/nicegui/security-advisories/GHSA-p92q-2755-mhgh --jq '{summary, description}'
   ```

3. **Title:** one short sentence stating the effect, not the mechanism.
   "Disabled or hidden `ui.upload` elements still accept uploads", not "upload route bypasses the `is_ignoring_events` check".

4. **Description** in four sections, prose only - no code dumps, no proof-of-concept steps, no internal class or function names:

   - `### Summary` - what NiceGUI does, what was missing, what a client could do.
   - `### Impact` - which applications are affected, who can exploit it (a logged-in user? anyone on the network?), what the damage depends on, and which applications are not affected.
   - `### Patches` - "Fixed in NiceGUI **x.y.z**", one sentence on what the fix does and its limits (link follow-up issues), "Upgrade to x.y.z or later."
   - `### Workarounds` - what to do without upgrading; often the recommended pattern anyway.

   The reporter is credited via the credits field, not in the text.

5. **Draft the text for the user to review**, then patch it with a JSON file written by a script (the description contains code spans and newlines):

   ```
   gh api -X PATCH repos/zauberzeug/nicegui/security-advisories/<ghsa-id> --input patch.json   # {"summary": "...", "description": "..."}
   ```

6. **Keep the advisory a draft** until the release named under Patches is on PyPI.
   Setting the patched version, requesting a CVE and publishing are separate, confirmed actions after the release.
