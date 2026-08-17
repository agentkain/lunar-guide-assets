# Lunar Organic Production — Reference

Read from `SKILL.md` when packaging, scheduling, or debugging a batch.

## Buffer channels (My Organization)

Confirm with `list_channels` before every campaign; IDs can change if accounts are reconnected.

| Channel | ID (as of AFFIRM Aug 2026 batch) |
|---------|----------------------------------|
| Instagram | `6a7a125fb2d9d57743502b43` |
| Facebook | `6a7a12e8b2d9d577435037aa` |
| Organization | `6a7a0f66c4d9821ad859a68f` |

Raw media base (stills on `main`):

```text
https://raw.githubusercontent.com/agentkain/lunar-guide-assets/main/
```

## Week folder rule

Monday of the post date (UTC) → `week-MM-DD`.

Examples from the AFFIRM Aug 23–Sep 5 batch:

| Post date | Folder |
|-----------|--------|
| 2026-08-23 (Sun) | `2026/08/week-08-17/` |
| 2026-08-24 … 08-30 | `2026/08/week-08-24/` |
| 2026-08-31 | `2026/08/week-08-31/` |
| 2026-09-01 … 09-05 | `2026/09/week-08-31/` |

Subdirs: `feed/`, `stories/`, `video/`, `captions/`.

## AFFIRM Remotion pipeline paths

```text
lunar-guide-assets/
  production/
    affirm-*.json                 # manifests, schedule, Buffer payloads, results
  pipeline/affirm-remotion/
    scripts/generate-backgrounds.py
    scripts/render.mjs
    scripts/prepare-buffer-posts.py
    public/backgrounds/           # gitignored working backgrounds
    src/still.tsx                 # type overlay template
  2026/…/week-…/feed|stories|captions/
```

API key: typically `GOOGLE_API_KEY` in `Lunar-Guide-Home-Page/.env.local` (never commit).

## Buffer payload row shape

```json
{
  "date": "YYYY-MM-DD",
  "creativeId": "LG-…",
  "channel": "instagram|facebook",
  "format": "feed|story",
  "channelId": "…",
  "dueAt": "YYYY-MM-DDTHH:MM:SS-06:00",
  "text": "caption or empty for story",
  "imageUrl": "https://raw.githubusercontent.com/…",
  "altText": "…",
  "metadata": {}
}
```

Results file:

```json
{
  "scheduledAt": "ISO",
  "organization": "My Organization",
  "totalPosts": 56,
  "successCount": 56,
  "failureCount": 0,
  "posts": [
    {
      "date": "…",
      "creativeId": "…",
      "channel": "…",
      "format": "…",
      "bufferPostId": "…",
      "dueAt": "…",
      "status": "scheduled|error",
      "error": null
    }
  ]
}
```

## create_post essentials

- `schedulingType`: `automatic`
- `mode`: `customScheduled` when using explicit `dueAt`
- Image asset: `{ "image": { "url": "…", "metadata": { "altText": "…" } } }`
- `dueAt` must be after `get_account.currentTime`

## QA probes

- Count `(channel, date, format)` uniqueness
- Sample HEAD/GET on raw image URLs after merge
- Spot-check 1–2 live Buffer posts for CTA text after edits
- Confirm results JSON has one unique `bufferPostId` per planned row

## Known gotchas

| Issue | Fix |
|-------|-----|
| Remotion `npx` fails on Windows | `process.execPath` + local `remotion-cli.js` |
| Backgrounds include frames/CTA | Stricter text-free prompt; regenerate with date filter |
| JSON string replace misses captions | File uses escaped `\n`; replace escaped form in JSON |
| QA on stale branch tip | Schedule from payloads that match approved CTA on disk/`main` |
| Buffer rate limit advisory | Pause; do not burn remaining daily quota on spot-checks |
| Drive / Google Doc OAuth `invalid_grant` | User re-runs OAuth setup; do not block Buffer hosting on Drive |

## Extending for a new idea

1. Copy an existing `production/*` manifest as a template; rename slug.
2. Reuse week folders + Buffer row shape.
3. If visuals differ, add `pipeline/{slug}-remotion/` or a composition — do not fork Buffer/hosting rules.
4. Keep CTA and hashtags as campaign parameters, not hardcoded skill dogma (except the current AFFIRM default in `SKILL.md` until the user changes it).
