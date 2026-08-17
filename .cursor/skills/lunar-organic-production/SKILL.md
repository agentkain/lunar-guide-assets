---
name: lunar-organic-production
description: >-
  Produce and schedule Lunar Guide organic social assets (AFFIRM, QUIZ, TAROT,
  UGC, Remotion stills/video) in lunar-guide-assets, host via GitHub raw URLs,
  and schedule Buffer posts. Use when building dated social batches, Nano Banana
  backgrounds, Remotion overlays, captions, week-folder packaging, Buffer
  scheduling/rollback, or adapting the pipeline for new post or video ideas.
---

# Lunar Organic Production

Ship organic Lunar Guide creatives from brief → assets → hosted URLs → Buffer.
Strategy/copy research belongs in `lunar-creative-strategist`; this skill runs
**production and distribution** after the user approves the batch.

## Repos and roles

| Repo | Role |
|------|------|
| `lunar-guide-assets` | Final stills/video, captions, production JSON, Remotion pipelines |
| `Lunar-Guide-Home-Page` | UGC Remotion projects, env keys (`GOOGLE_API_KEY`), older video work |
| Buffer MCP (`user-buffer`) | Schedule / edit / delete posts |

Default Buffer org: **My Organization**. Timezone: **America/Denver**. Build
`dueAt` with the account offset from `get_account` (often `-06:00` / `-07:00`).

Do not schedule, delete, or buy credits without explicit user approval.

## Choose a lane

Pick the smallest lane that fits. New ideas should map to a lane, not invent a
parallel system.

| Lane | Typical output | Visual pipeline |
|------|----------------|-----------------|
| **AFFIRM still** | 4:5 feed + 9:16 story | Nano Banana background (no text) → Remotion type overlay |
| **QUIZ / TAROT still** | Same formats | Same pipeline; change template, CTA, hashtags |
| **UGC / presenter video** | 9:16 (and placements as approved) | HeyGen / phone / library footage → Remotion edit → Cloudinary or assets repo |
| **Motion graphic** | Feed/story/reel | Remotion composition only (no Nano Banana unless needed) |
| **Hybrid** | Mix stills + video in one date range | One manifest; separate render scripts per format |

When the user has a new idea: confirm format(s), channels, CTA, claim style, and
whether assets are stills, video, or both — then extend the existing lane.

## End-to-end checklist

Copy and track:

```
- [ ] 1. Scope + approval (dates, channels, formats, CTA, claim style)
- [ ] 2. Creative manifest in production/
- [ ] 3. Generate / source visuals
- [ ] 4. Remotion render (stills and/or video)
- [ ] 5. QA assets
- [ ] 6. Place into week folders + captions
- [ ] 7. Commit/PR/merge to main (raw GitHub hosting)
- [ ] 8. Build Buffer payloads
- [ ] 9. User approves schedule → create_post
- [ ] 10. Save results JSON; spot-check CTA + URLs
```

## 1. Scope

Capture before producing:

- Date range and creative mode (`AFFIRM`, `QUIZ`, `TAROT`, `UGC`, custom)
- Channels (default IG + FB; add TikTok only if asked)
- Formats (default feed 1080×1350, story 1080×1920)
- Claim style and CTA (platform-agnostic; no hard-coded @handles unless asked)
- Caption pattern: message → short reflection → CTA → hashtags

Default AFFIRM feed CTA (update only when the user changes it):

```text
✨ Comment AFFIRM to lock it in and be sure to follow and share.
```

Stories usually ship with empty Buffer `text` and type `story`.

Creative IDs: `LG-{YYYYMMDD}-{MODE}-{ANGLE}-{NN}`.

## 2. Manifest

Write `production/{slug}.json` with campaign meta + `creatives[]`:

```json
{
  "campaign": "…",
  "dateRange": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "claimStyle": "…",
  "distribution": {
    "channels": ["instagram", "facebook"],
    "formats": ["feed-4x5", "story-9x16"],
    "paidEligibility": "organic-only"
  },
  "creatives": [
    {
      "date": "YYYY-MM-DD",
      "creativeId": "LG-…",
      "message": "…",
      "motif": "text-free visual direction for background gen"
    }
  ]
}
```

For video batches, add fields the render script needs (`script`, `voice`,
`durationSec`, `sourceAsset`) without forcing AFFIRM-only keys.

## 3. Visuals

**Prefer** Lunar Guide Operations library / existing assets before paid gen.

**AFFIRM-style backgrounds**

- Model: Google Nano Banana (`gemini-3.1-flash-image`) via `GOOGLE_API_KEY`
- Prompt: text-free celestial motif; forbid frames, pills, watermarks, captions
- Reference an approved AFFIRM look when consistency matters
- Regenerate any frame that bakes UI/CTA into the image

**Video**

- Follow presenter + audio policy from the approved brief
- Mute B-roll by default; do not auto-retry paid jobs past the wait ceiling
  (see `lunar-creative-strategist`)

## 4. Remotion

Reusable AFFIRM still pipeline lives at
`lunar-guide-assets/pipeline/affirm-remotion/`.

- Overlay brand chrome in Remotion — not in the background image
- Windows: call Remotion via `process.execPath` + `remotion-cli.js` (avoid brittle `npx` spawns)
- Prefer the [Remotion Cursor plugin](https://cursor.com/marketplace/remotion) / skills over deprecated Remotion MCP
- For a new template (QUIZ, TAROT, video): fork the pipeline folder or add a composition; keep scripts parameterized by manifest path

## 5. QA before hosting

- Counts: N dates → expected stills/videos + captions
- Dims: feed 1080×1350, story 1080×1920 (or approved video specs)
- No white/blank frames; no baked CTA/frames in backgrounds
- Unique messages; CTA matches approved copy
- Paths map to correct week folders (see [reference.md](reference.md))

## 6. Week-folder packaging

```text
{YYYY}/{MM}/week-{MM-DD}/feed|stories|video|captions/
```

- `week-{MM-DD}` = Monday of that post’s week (`MM-DD` UTC)
- Cross-month weeks keep the Monday folder name under the post’s month dir
- Naming: `{YYYY-MM-DD}_{slot}_{MODE}_{ratio}.{ext}`  
  Example: `2026-08-24_08_AFFIRM_4x5.jpg`

Gitignore working artifacts (`node_modules/`, `.remotion/`, `public/backgrounds/`, `out/`, `*.local.json`). Commit finals + captions + production JSON.

## 7. Host for Buffer

Buffer needs public media URLs. Default for stills:

```text
https://raw.githubusercontent.com/agentkain/lunar-guide-assets/main/{path}
```

1. Commit on a feature branch → PR → merge to `main`
2. Verify sample raw URLs return 200 before scheduling
3. Video may use Cloudinary when already established for that lane — keep one host per batch and record it in results JSON

## 8–10. Buffer

1. `get_account` → confirm org + timezone/`currentTime`
2. `list_channels` → use exact channel IDs (never invent)
3. Build `production/{slug}-buffer-posts-to-create.json` (one row per channel×format×date)
4. Prefer `mode: customScheduled` + channel schedule slots; `schedulingType: automatic`
5. Instagram feed: `metadata.instagram.type: post`, `shouldShareToFeed: true`
6. Instagram story: `type: story`, `shouldShareToFeed: false`
7. Facebook: `metadata.facebook.type: post|story`
8. Create posts only after user approval
9. Write `production/{slug}-buffer-results.json` with every Buffer post ID
10. Caption edits after scheduling: `get_post` → `edit_post` (carry assets + metadata; change only text)
11. Rollback: delete only IDs in that results file — never unrelated campaigns

Rate limits are shared across Buffer MCP calls. Batch carefully; stop when the advisory window is nearly empty.

## Flexibility rules

- New post idea → new/extended manifest + CTA/hashtags; reuse folder + Buffer patterns
- New video idea → same packaging/hosting/Buffer steps; swap the render lane
- Do not hard-code platform @handles in captions unless the user asks
- Keep organic and paid lanes separate; this skill does not activate ads
- When unsure, ask for formats/channels/CTA — not for reinventing folder layout

## Related skills

- `lunar-creative-strategist` — research, briefs, paid gates, Higgsfield/HeyGen waits
- Remotion plugin/skills — composition authoring and render details

## Reference

Channel IDs, week mapping, payload shapes, and gotchas: [reference.md](reference.md)
