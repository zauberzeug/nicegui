---
name: release-notes
description: Write NiceGUI release notes for a milestone to release.md and a Reddit post to reddit.md. Use when asked to draft release notes or a release announcement for a given milestone/version (e.g. "write release notes for 3.14").
---

Write release notes for the milestone passed as an argument (e.g. `3.14`) to `release.md` and a Reddit post to `reddit.md`.

## How to gather data

**Start with the helper script** [`release-notes.sh`](release-notes.sh) (in this skill's directory), which collects the deterministic data so nothing is forgotten:

- `release-notes.sh dossier "<milestone>"` → one JSON dossier: every milestone issue/PR with labels, author, committers, reviewers, commenters, and extracted cross-reference `#`s; each cross-reference resolved to issue/PR/**discussion** with its author (discussions are the easiest contributor to miss); plus the sponsors dump sorted by monthly amount.
- `release-notes.sh verify "<milestone>" release.md` → milestone tickets missing from the draft (and `#`s in the draft that aren't milestone tickets — expected for cross-refs).
- `release-notes.sh check-docs <slug> [slug...]` → HTTP status per docs page, to verify links before using them.

The dossier gives you the raw facts; you still apply judgment for grouping tickets into stories, writing descriptions, and deciding which commenters are substantive. The manual `gh` recipes below remain valid as a fallback or for spot-checks.

1. Use `gh` to list all issues and PRs in the milestone with their labels, linked PRs, authors, and participants.
2. For each issue/PR, inspect the timeline and comments to identify contributors (see contributor rules below).
3. For each merged PR, also fetch its reviewers and committers explicitly — `gh pr view <n> --json reviews,commits` — and fold them into the contributor list. Comment scraping alone misses reviewers who only left a formal review. (Do not credit the merger; see Contributors.)
4. Resolve cross-referenced numbers that are **discussions**, not issues/PRs. `gh issue view <n>` / `gh pr view <n>` fail on a discussion number; query it via GraphQL instead, e.g. `gh api graphql -f query='{repository(owner:"zauberzeug",name:"nicegui"){discussion(number:N){title author{login}}}}'`, and credit the discussion author.
5. Check if any PRs reference a GHSA (GitHub Security Advisory) — these go into a separate Security section.

## Structure

Follow the exact structure used in prior releases at https://github.com/zauberzeug/nicegui/releases.

### Section mapping (by label)

| Label            | Section heading               |
| ---------------- | ----------------------------- |
| (GHSA-based PRs) | Security                      |
| `feature`        | New features and enhancements |
| `bug`            | Bugfixes                      |
| `documentation`  | Documentation                 |
| `testing`        | Testing                       |
| `dependencies`   | Dependencies                  |
| `infrastructure` | Infrastructure                |

If a label doesn't map to any section above, use your best judgment to place it or create an appropriate section following the established pattern.

Security section (if any) always comes first. Then the remaining sections in the order listed above.
Security items start with a "⚠️" prefix (e.g. `⚠️ Prevent memory exhaustion via media streaming routes`).

### Sponsors footer

Both `release.md` and `reddit.md` should end with a sponsors footer.

Fetch active sponsors via the GitHub GraphQL API:

```
gh api graphql -f query='{ organization(login: "zauberzeug") { sponsorshipsAsMaintainer(first: 100, activeOnly: true) { nodes { sponsorEntity { ... on User { login name } ... on Organization { login name } } tier { monthlyPriceInDollars isOneTime } } } } }'
```

Mention sponsors by name (linked to their GitHub profile) if they meet either threshold:

- Monthly sponsor: $150/month or more
- One-time sponsor: $50 or more

The threshold is a starting point, not the final word: the named set is curated and may carry forward a long-standing sponsor that now sits below the threshold (e.g. a recurring sponsor named in the previous release). So **always surface the computed candidate set and confirm the final "top sponsors" line with the user before writing the footer** — list each candidate with its monthly/one-time amount, and cross-check against the previous release's footer at https://github.com/zauberzeug/nicegui/releases so a previously-named sponsor isn't silently dropped.

Use the existing footer format:

```
---

#### Special thanks to our top sponsors [Name1](https://github.com/login1) and [Name2](https://github.com/login2) ✨

and all our other [sponsors](https://github.com/sponsors/zauberzeug) and [contributors](https://github.com/zauberzeug/nicegui/graphs/contributors) for supporting this project!

🙏 _Want to support this project? Check out our [GitHub Sponsors page](https://github.com/sponsors/zauberzeug) to help us keep building amazing features!_
```

If no sponsors meet the threshold, omit the "Special thanks" line and just keep the general sponsors/contributors line.

### Documentation links

When an item mentions a UI element or concept that has a documentation page, link it.
For example: [`ui.parallax`](https://nicegui.io/documentation/parallax), [`ui.scene`](https://nicegui.io/documentation/scene).

**Important:** Do not guess URLs. Verify each link exists by fetching it (the `check-docs` helper does this in bulk).
The typical pattern is `https://nicegui.io/documentation/<element_name_without_ui_prefix>`,
but sections like `section_configuration_deployment` or `section_security` also exist.
If a page doesn't exist yet (e.g. new elements added in this release), ask the user whether to include the link anyway (it will go live after deployment).

### Item format

Each line follows this pattern:

```
- Short description of the change (#issue, #pr by @author1, @author2, @contributor3)
```

- One item per story (a story is usually an issue with a PR that fixes it, but may include follow-up fixes)

- Check PR descriptions for references to feature requests, discussions, or other issues that led to the change — include those ticket numbers too

- Group related tickets into a single item — all ticket numbers for the milestone should appear somewhere

- Ticket numbers go in parentheses: `(#123, #456 by @user1, @user2)`

- If a PR has a breaking change, add a `**Breaking change:**` block below the item, like this:

  ```
  - Short description of the change (#issue, #pr by @author1, @author2)

      **Breaking change:** Explanation of what changed and how to migrate.
      For example, if an API was removed, show the old usage and the new replacement.
  ```

### Contributors

For each item, mention all involved contributors in the `by @...` list:

- Issue author
- **The author of any feature request / discussion that led to the change** (often referenced in the PR description), plus anyone who contributed substantively to that discussion — not only the issue/PR participants
- Users with relevant contributions to discussions (substantive comments, reproductions, debugging - not just "me too" comments)
- **Reviewers** who provided relevant feedback — include both review submissions (`gh pr view <n> --json reviews`) **and** inline review comments, not just top-level issue/PR comments. A formal review with no top-level comment is easy to miss with comment scraping alone.
- Committers (anyone who pushed commits to the PR), ignoring AI/bot co-author logins such as `claude`

Do **not** credit the merger as such — merging a PR is not, on its own, a contribution worth listing.

**Make sure no contributor is forgotten** — when a borderline commenter is genuinely engaged (offered to help, attempted a fix, added environment detail), lean toward including them rather than filtering them out. Only ignore:

- Simple "me too" comments with no added information
- Review approvals without valuable comments or own commits

## Verification

After writing `release.md`, verify completeness — `release-notes.sh verify "<milestone>" release.md` does steps 1-3:

1. Use `gh` to list all issue and PR numbers in the milestone.
2. Extract all `#nnn` ticket numbers from the generated `release.md`.
3. Compare the two sets. Report any milestone tickets missing from the release notes.
4. If there are missing tickets, investigate them and either add them to the appropriate section or explain why they were excluded (e.g. duplicates, reverted, not actually resolved).

## Reddit post

After `release.md` is complete, create `reddit.md` based on it.

Keep most of the Markdown unchanged, including:

- "⚠️" for security issues
- The sponsors footer

Apply these changes:

- Add a title line at the top starting with "NiceGUI x.y.z with ..." mentioning the most important changes
- Remove the parenthesized ticket numbers and contributors (the `(#123, #456 by @user1, @user2)` parts)
- Keep the documentation links from `release.md`
