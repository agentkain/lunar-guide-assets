import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parents[2]
MANIFEST_PATH = REPO_DIR / "production" / "affirm-2026-08-23-to-09-05.json"
SCHEDULE_PATH = REPO_DIR / "production" / "affirm-buffer-schedule.json"
POSTS_PATH = REPO_DIR / "production" / "affirm-buffer-posts-to-create.json"
RAW_BASE_URL = "https://raw.githubusercontent.com/agentkain/lunar-guide-assets/main/"
DENVER_OFFSET = timezone(timedelta(hours=-6))

INSTAGRAM_ID = "6a7a125fb2d9d57743502b43"
FACEBOOK_ID = "6a7a12e8b2d9d577435037aa"

SLOTS = {
    "instagram-feed": {
        "mon": "18:43",
        "tue": "17:28",
        "wed": "10:43",
        "thu": "08:35",
        "fri": "06:20",
        "sat": "06:56",
        "sun": "21:50",
    },
    "instagram-story": {
        "mon": "20:41",
        "tue": "19:56",
        "wed": "18:37",
        "thu": "09:51",
        "fri": "07:05",
        "sat": "22:17",
        "sun": "22:06",
    },
    "facebook-feed": {
        "mon": "06:53",
        "tue": "07:06",
        "wed": "08:15",
        "thu": "08:05",
        "fri": "08:40",
        "sat": "06:33",
        "sun": "09:09",
    },
    "facebook-story": {
        "mon": "07:37",
        "tue": "08:51",
        "wed": "09:00",
        "thu": "09:21",
        "fri": "09:56",
        "sat": "22:43",
        "sun": "10:56",
    },
}

REFLECTIONS = [
    "Let this be the reminder that abundance can arrive through paths you have not considered yet.",
    "Receive the vision, then keep becoming the person who can hold it.",
    "What belongs to you will not need you to shrink before it opens.",
    "You have not been forgotten. The life you asked for is still making its way toward you.",
    "One message can change the direction of an entire season. Stay open.",
    "The next room may value what the last room overlooked.",
    "The limits that protected an older version of you cannot contain who you are becoming.",
    "You are allowed to enter September with higher standards and a clearer sense of worth.",
    "Movement can begin quietly. Do not mistake silence for stagnation.",
    "This month, your consistency and courage will become visible.",
    "The gift you questioned is becoming the work people recognize and reward.",
    "The answer may arrive in a form more expansive than the one you imagined.",
    "Your work can speak for you in rooms you have never entered.",
    "Look for the evidence today. You are not as far away as fear has told you.",
]


def caption_for(message: str, reflection: str) -> str:
    return (
        f"{message}\n\n"
        f"{reflection}\n\n"
        "✨ Comment AFFIRM to lock it in.\n"
        "Follow @lunarguideapp and share this with someone who needs the reminder.\n\n"
        "#affirmation #abundance #manifestation #goodthingsarecoming "
        "#trusttheprocess #spiritualgrowth #lunarguide"
    )


def due_at(date_string: str, time_string: str) -> str:
    hour, minute = map(int, time_string.split(":"))
    date = datetime.strptime(date_string, "%Y-%m-%d")
    return date.replace(
        hour=hour,
        minute=minute,
        tzinfo=DENVER_OFFSET,
    ).isoformat()


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
    schedule_by_date = {item["date"]: item for item in schedule}
    posts = []

    for creative, reflection in zip(manifest["creatives"], REFLECTIONS, strict=True):
        item = schedule_by_date[creative["date"]]
        caption = caption_for(creative["message"], reflection)
        item["caption"] = caption

        caption_path = (
            REPO_DIR
            / item["feedPath"].replace("/feed/", "/captions/").replace(
                f"{creative['date']}_08_AFFIRM_4x5.jpg",
                f"{creative['date']}_AFFIRM_captions.txt",
            )
        )
        caption_path.parent.mkdir(parents=True, exist_ok=True)
        caption_path.write_text(f"{caption}\n", encoding="utf-8")

        day = datetime.strptime(creative["date"], "%Y-%m-%d").strftime("%a").lower()
        variants = [
            (
                "instagram",
                "feed",
                INSTAGRAM_ID,
                "instagram-feed",
                item["feedPath"],
                caption,
                {"instagram": {"type": "post", "shouldShareToFeed": True}},
            ),
            (
                "facebook",
                "feed",
                FACEBOOK_ID,
                "facebook-feed",
                item["feedPath"],
                caption,
                {"facebook": {"type": "post"}},
            ),
            (
                "instagram",
                "story",
                INSTAGRAM_ID,
                "instagram-story",
                item["storyPath"],
                "",
                {"instagram": {"type": "story", "shouldShareToFeed": False}},
            ),
            (
                "facebook",
                "story",
                FACEBOOK_ID,
                "facebook-story",
                item["storyPath"],
                "",
                {"facebook": {"type": "story"}},
            ),
        ]

        for channel, format_name, channel_id, slot_key, image_path, text, metadata in variants:
            posts.append(
                {
                    "date": creative["date"],
                    "creativeId": creative["creativeId"],
                    "channel": channel,
                    "format": format_name,
                    "channelId": channel_id,
                    "dueAt": due_at(creative["date"], SLOTS[slot_key][day]),
                    "text": text,
                    "imageUrl": f"{RAW_BASE_URL}{image_path}",
                    "altText": creative["message"],
                    "metadata": metadata,
                }
            )

    SCHEDULE_PATH.write_text(
        json.dumps(schedule, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    POSTS_PATH.write_text(
        json.dumps(posts, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {len(schedule)} captions and prepared {len(posts)} Buffer posts.")


if __name__ == "__main__":
    main()
