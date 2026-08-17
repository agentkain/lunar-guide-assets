import json
import os
from pathlib import Path

from google import genai
from google.genai import types


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
REPO_DIR = PROJECT_DIR.parents[1]
MANIFEST_PATH = REPO_DIR / "production" / "affirm-2026-08-23-to-09-05.json"
REFERENCE_PATH = (
    REPO_DIR
    / "2026"
    / "08"
    / "week-08-17"
    / "stories"
    / "2026-08-17_01_AFFIRM_9x16.jpg"
)
OUTPUT_DIR = PROJECT_DIR / "public" / "backgrounds"
LOG_PATH = REPO_DIR / "production" / "affirm-background-generation.json"
MODEL = "gemini-3.1-flash-image"


def load_env_value(key: str) -> str:
    if value := os.environ.get(key):
        return value

    env_path = REPO_DIR.parent / "Lunar-Guide-Home-Page" / ".env.local"
    if not env_path.exists():
        raise RuntimeError(f"{key} is not set and {env_path} does not exist")

    for raw_line in env_path.read_text(encoding="utf-8-sig").splitlines():
        if raw_line.startswith(f"{key}="):
            return raw_line.split("=", 1)[1].strip().strip("\"'")

    raise RuntimeError(f"{key} is not present in {env_path}")


def make_prompt(motif: str) -> str:
    return f"""
Use the attached Lunar Guide artwork only as a color, lighting and texture reference.
Do not copy its layout, frame, text placement, button, capsule or border.
Create a new text-free vertical background for an affirmation card.

Visual direction:
- restrained celestial editorial minimalism
- deep midnight plum, black-violet, muted burgundy and warm copper
- subtle film grain, sparse tiny stars, soft lens bloom, gentle atmospheric haze
- refined, quiet, premium and mystical; not fantasy illustration or stock art
- central motif: {motif}
- keep the middle 55% calm and low-detail for large ivory typography
- keep the lower 22% calm for a gold call-to-action badge
- fine tonal depth with one understated warm-gold focal light
- full-bleed vertical 9:16 composition with color reaching every outer edge

Do not include any words, letters, logos, borders, watermarks, UI, symbols that
look like writing, people facing the camera, currency, coins, dollar signs,
buttons, pills, capsules, labels, frames, white margins or reserved blank bars.
Return only the finished background image.
""".strip()


def generate_background(client: genai.Client, motif: str, output_path: Path) -> None:
    reference = types.Part.from_bytes(
        data=REFERENCE_PATH.read_bytes(),
        mime_type="image/jpeg",
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=[reference, make_prompt(motif)],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="9:16",
                image_size="2K",
            ),
        ),
    )

    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            if part.inline_data and part.inline_data.data:
                output_path.write_bytes(part.inline_data.data)
                return

    raise RuntimeError(f"{MODEL} returned no image for {output_path.name}")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=load_env_value("GOOGLE_API_KEY"))
    results = []
    generation_limit = int(os.environ.get("GENERATION_LIMIT", "0"))
    force_dates = {
        value.strip()
        for value in os.environ.get("FORCE_DATES", "").split(",")
        if value.strip()
    }
    creatives = manifest["creatives"]
    if force_dates:
        creatives = [
            creative for creative in creatives if creative["date"] in force_dates
        ]
    if generation_limit:
        creatives = creatives[:generation_limit]

    for creative in creatives:
        output_path = OUTPUT_DIR / f"{creative['date']}.png"
        if (
            creative["date"] not in force_dates
            and output_path.exists()
            and output_path.stat().st_size > 100_000
        ):
            status = "reused"
        else:
            print(f"Generating {creative['date']} with {MODEL}...", flush=True)
            generate_background(client, creative["motif"], output_path)
            status = "generated"

        results.append(
            {
                "date": creative["date"],
                "creativeId": creative["creativeId"],
                "model": MODEL,
                "reference": str(REFERENCE_PATH.relative_to(REPO_DIR)).replace("\\", "/"),
                "output": str(output_path.relative_to(REPO_DIR)).replace("\\", "/"),
                "bytes": output_path.stat().st_size,
                "status": status,
            }
        )
        print(f"{status}: {output_path.name} ({output_path.stat().st_size:,} bytes)")

    LOG_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
