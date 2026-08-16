# Lunar Guide — social assets

Static host so Buffer can fetch post media by URL.

    <year>/<month>/week-<MM-DD>/feed/     4:5   1080x1350  feed posts
    <year>/<month>/week-<MM-DD>/stories/  9:16  1080x1920  stories
    <year>/<month>/week-<MM-DD>/video/    9:16  mp4        reels / TikTok
    <year>/<month>/week-<MM-DD>/captions/ txt              one file per posting day

Week folders are named for the Monday of that week. Filenames are
`YYYY-MM-DD_SS_KEYWORD_FORMAT.ext` where SS is the posting slot number.
Caption files are `YYYY-MM-DD_DDD_captions.txt` and cover every slot for that
day across both formats.

Raw URL pattern:

    https://raw.githubusercontent.com/agentkain/lunar-guide-assets/main/2026/08/week-08-17/feed/2026-08-17_01_AFFIRM_4x5.jpg

Excluded from search indexing via robots.txt.

## Note on the root copies

The 98 posts scheduled for 17–23 Aug 2026 reference the old flat root URLs, so
those files are kept at the root until that week has published. They are safe to
delete on or after 24 Aug 2026.
