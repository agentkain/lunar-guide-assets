# Claude Ads — vendored skills

Paid-media skills used for Lunar Guide ad strategy, audits, and creative briefs.

## Provenance

| | |
|---|---|
| Upstream | https://github.com/AgriciDaniel/claude-ads |
| Version | v2.0.1 |
| Commit | `669c7608ecb50dd95c941a71fa3ca0a1c0e40512` |
| License | MIT — see `ADS_LICENSE` |
| Vendored | 2026-08-18 |

## Layout

    .claude/skills/ads/SKILL.md          main operating contract, entry point
    .claude/skills/ads/references/       38 platform + methodology references
    .claude/skills/ads-<name>/           33 workflow and platform skills
    .claude/agents/                      25 audit and creative worker agents
    .claude/ads-control-plane/           manifests and schemas the skills cite

Start with the `ads` skill; it routes to the rest. Platform skills
(`ads-meta`, `ads-google`, …) and workflow skills (`ads-plan`, `ads-budget`,
`ads-creative`, …) can also be invoked directly.

Cross-reference paths in the skill text were rewritten from the upstream repo
layout to this one. Upstream `ads/references/x.md` is
`.claude/skills/ads/references/x.md` here, and `control-plane/` is
`.claude/ads-control-plane/`. Re-apply those rewrites when updating.

## What was left out

The upstream Python execution layer is **not** vendored: `claude_ads_core/`,
`scripts/`, `tests/`, `evals/`, and the install scripts. Everything the model
reads and reasons over is here; nothing that needs `pip install` is.

As a result these degrade to model-driven work rather than deterministic tooling:

- `/ads status` and `/ads next` — no `python -m claude_ads_core` backend
- `/ads validate` — schemas are present, but no validator runs them
- `/ads report` PDF rendering — needs `weasyprint` / `matplotlib`
- `ads-generate` image fallback — needs `scripts/generate_image.py`

Also skipped: `control-plane/dependency-inventory.json` (1.5 MB) and other
release-engineering ledgers no skill references.

## Updating

Re-clone upstream, copy `ads/`, `skills/`, `agents/` and the cited
`control-plane/` files into this layout, then re-run the path rewrites above and
confirm every referenced file resolves.
