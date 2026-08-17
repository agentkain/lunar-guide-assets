# Lunar Guide — weekly content pipeline

**Source of truth.** Keep this file in the `agentkain/lunar-guide-assets` repo under `pipeline/`.
Any scheduled session can read it anonymously via
`https://raw.githubusercontent.com/agentkain/lunar-guide-assets/main/pipeline/PIPELINE.md`.
Do **not** keep operational docs in the Claude project store — a freshly-fired scheduled
session cannot read them, which is why the video half of the build silently produced nothing
for weeks while the image half kept working.

---

## 1. Network reality — read before planning anything

| Environment | Can reach | Cannot reach |
|---|---|---|
| Claude cloud container (`Bash`) | raw.githubusercontent.com, npm/pip registries | **HeyGen, Cloudinary, Higgsfield CDN** |
| Higgsfield `sandbox_exec` | everything (HeyGen 403 = reachable, Cloudinary, GitHub) | — |
| `device_bash` (user's machine) | user's mounted folders | **no network at all** |

Consequences:

- **All video assembly happens in the Higgsfield sandbox.** The container cannot download
  HeyGen output, so it cannot composite. This is not negotiable.
- The container cannot `curl` a Cloudinary delivery URL to verify HTTP 200 before scheduling.
  Verify server-side with `get-asset-details` (returns bytes/format/dimensions) instead, and
  treat a `create_post` that returns `error: null` as the real proof Buffer could fetch it.
- `sandbox_exec` is **compute only — it does not consume Higgsfield generation credits.**
  Generation credits are reserved for ads.

## 2. The sandbox lifecycle trap — cost us two complete renders

The Higgsfield sandbox is destroyed roughly **60 seconds after the last call finishes**, taking
`node_modules`, the project, and any rendered output with it.

Rules that follow from this:

1. **One self-contained call.** A single `sandbox_exec` must write the project, install, fetch
   inputs, render, QA, *and upload the result*. Never split setup across calls — the time you
   spend composing the second command is enough to kill the first.
2. **Get presigned upload URLs BEFORE starting the job**, and put the `curl -X PUT` inside the
   same background script. Never upload in a follow-up call.
3. **Poll every <60s and never interleave another tool call.** One `get_video` check between
   polls is enough to lose a 15-minute render.
4. `set -e` plus `test -s out.mp4` before uploading. A missing file makes
   `curl --data-binary @out.mp4` PUT an empty body that **S3 accepts with HTTP 200** — a silent
   corruption that looks like success.
5. **Never reuse a media_id after a failed upload.** CloudFront caches the zero-byte object and
   will keep serving empty forever; query-string cache-busting does not help because the default
   cache key ignores them. Request a fresh `media_upload` and use the new UUID.

## 3. Remotion

- Remotion 4 requests **old headless mode**, which the preinstalled Playwright Chromium removed.
  Use `npx remotion browser ensure` and point `--browser-executable` at the
  `chrome-headless-shell` it downloads. (In the Claude container, the equivalent binary is
  `/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`.)
- Render cost: **~4–8 min per 725-frame 1080x1920 video at `--concurrency=2`.** Seven videos is
  roughly an hour of wall clock, all of it needing heartbeat polls.
- **Presenter renders in a panel — this is ACCEPTED, do not "fix" it.** HeyGen's
  `outputFormat: "webm"` carries alpha (`alpha_mode: 1`) but it does not composite in the
  Remotion render, so the presenter appears inside a visible rectangle rather than cut out over
  the background. Chi reviewed this on 2026-08-17 and chose to keep it — he reads it as a
  UGC-style look. **Do not block shipping on it and do not silently change it.**
  (ffprobe reports `pix_fmt=yuv420p` and flattens transparency to black, so this is invisible
  to automated checks — you will only see it on a rendered frame. That is expected now.)
  Because the panel's appearance depends on whatever background HeyGen renders for a given
  avatar look, it will drift between looks. If it ever needs to be consistent across all seven
  videos, make it a deliberate framed treatment rather than relying on the artifact.

## 4. Assets and identities

- **Presenter: Sarah** — avatar group `48f2582266514075b1ad35edd847e6d9`,
  portrait look `fe8c6678fafe4fceaf0b6ba4bad35e12` (941x1672, native 9:16),
  voice `0e722b2792904411a99856dbc698e50c`.
  Note there is a *second, different* "Sarah" group (`32d443200f084cf49671072cd73fee0e`) with a
  different voice — do not mix them. Never substitute another avatar; stop and ask.
- Ask HeyGen for `caption: {file_format: "srt"}` — the SRT gives real word timings, which is how
  captions and punch-ins get synced. Never hand-estimate timings; speech is faster than you think.
- **Higgsfield generation is reserved for ads.** Reels use Sarah over procedural Remotion
  celestial backgrounds, including videos 2, 5 and 7 which the original design had Higgsfield leading.

## 5. Hosting

- **Cloudinary is the primary host** — it is the only one that can be written to unattended.
  Path mirrors the repo: `lunar-guide/<year>/<month>/week-<MM-DD>/{feed,stories,video}/`.
- Verify integrity by comparing Cloudinary's returned `etag` to the md5 of the source file.
- Budget: steady state is ~3 credits/month against a 25 credit free allowance (~85% of bandwidth
  is video). Cap video renders under ~15 MB. Prune weeks older than 60 days.
- **GitHub is the archive of record**, mirrored when a browser is connected. The git proxy refuses
  pushes (`not in this session's authorized repository set`) and there is no GitHub connector, so
  the repo can never be written unattended. Do not design around pushing.

## 6. QA gate — what actually blocks

`qa.py <video> <manifest>` exits non-zero on:

1. **Silent audio.** Remotion writes a silent track by default, so "does an audio stream exist"
   passes a muted render. Measure with `volumedetect`: fail if `mean_volume < -60 dB`
   (silence), warn under -40, fail if peak > -0.5 dB (clipping).
2. **CTA on a blank frame.** Check ink coverage on sampled frames in the final 3–4s.
3. **Caption/end-card collision**, safe-zone intrusion (top 220px, bottom 480px, right 220px),
   spec conformance (1080x1920, 30fps, 20–30s, under size cap).

**Automated checks are necessary but not sufficient.** Always render one video, build a contact
sheet at beat boundaries, and *look at it* before batching the rest. In this session the gate
passed a cut where the presenter sat in a visible rectangle — only the contact sheet caught it.

To view frames when the container cannot reach the CDN: upload to Cloudinary, then open
`.../video/upload/so_<seconds>,w_400/<public_id>.jpg` in the connected browser and screenshot.

## 7. Hard punch-in — now machine-verifiable

100% → 110–114%, over **no more than 2 frames**, linear and clamped. No easing, bounce,
overshoot or settling. Implemented in `src/punch.ts` with plain `interpolate` (linear by default).

Verify empirically by measuring the caption bounding-box width across frames — a correct punch
reads flat, then a two-frame linear ramp, then clamped (e.g. 828 → 828 → 877 → 928, where 877 is
the exact midpoint). Measure inside the caption band, not the whole frame, or the presenter
dominates the bbox.
