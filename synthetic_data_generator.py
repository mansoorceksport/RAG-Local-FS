import os
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

OUTPUT_DIR = "data/employees"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# LLM PROMPT TEMPLATE
# ----------------------------
PROMPT_TEMPLATE = """
You are generating synthetic HR records for a fictional football club called FC Barcelona.

You MUST respond ONLY in markdown (.md) format.

The structure MUST follow EXACTLY this format:

# HR Record

# <Employee Full Name>

## Summary
- **Date of Birth:** <Month DD, YYYY>
- **Position:** <Player Position, or Staff Role>
- **Nationality:** <Country>
- **Current Salary:** $<salary>

## FC Barcelona Career Progression
- <Timeline with dates, signings, promotions, transfers, major contributions>

## Annual Performance History
- <Year>:
  - <Point 1 — match performance, stats, achievements>
  - <Point 2 — training, discipline, important events>
  - <Point 3 — any notable improvements or declines>

(Do this for 4 years, matching the example style.)

## Compensation History
- <Year>: Base Salary: $<Amount>
- <Year>: Salary Increase to $<Amount>; include bonuses (performance, goals, clean sheets, trophies, etc.)

## Other HR Notes
- <3–5 notes: training attitude, teamwork, injuries, community involvement, media interactions>

At the end, include a closing statement like:
"<Name> continues to contribute to FC Barcelona..."

-------------------------------------
ADDITIONAL RULES:
-------------------------------------

1. The employee performance category MUST be: GOOD, AVERAGE, or BAD.
2. You must generate the record according to the assigned category:

- GOOD performer:
  - Strong improvements
  - Major match contributions
  - High ratings (7.5–10/10 yearly avg)
  - Strong bonuses
  - Positive notes

- AVERAGE performer:
  - Decent but inconsistent contributions
  - Moderate ratings (6.0–7.4/10)
  - Ordinary bonuses
  - Mixed notes

- BAD performer:
  - Weak match impact
  - Low ratings (4.0–5.9/10)
  - Possible disciplinary notes, minor injuries, low bonuses
  - Still safe and professional, no extreme negativity

3. DO NOT mention the performance category in the markdown output.
4. Write realistic, human-like HR data.
5. Keep the writing style consistent and natural.

-------------------------------------

Generate ONE employee record now.
Employee performance category: **{category}**
Employee name style: Spanish, South American, European, African — random.
"""


# ----------------------------
# GENERATION FUNCTION
# ----------------------------
def generate_employee_record(category: str):
    """Generate one markdown HR record for a given performance category."""

    prompt = PROMPT_TEMPLATE.format(category=category)

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
    )

    content = response.output_text

    return content


# ----------------------------
# SAVE FILE
# ----------------------------
def save_markdown(name_slug: str, content: str):
    filepath = os.path.join(OUTPUT_DIR, f"{name_slug}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {filepath}")


# ----------------------------
# NAME SLUG GENERATOR
# ----------------------------
def extract_name(md_content: str) -> str:
    """
    Extract the employee name from the markdown title.
    Expected format: '# <Name>'
    """
    for line in md_content.splitlines():
        if line.startswith("# ") and "HR Record" not in line:
            return line.replace("#", "").strip().lower().replace(" ", "_")
    return "employee_" + str(uuid.uuid4()).split("-")[0]


# ----------------------------
# MAIN: GENERATE EVEN SPLIT
# ----------------------------
def generate_dataset(total=9):
    """
    Generate dataset evenly split between:
    - GOOD
    - AVERAGE
    - BAD
    """
    categories = ["GOOD", "AVERAGE", "BAD"]
    per_category = total // 3

    print(f"Generating {total} employees "
          f"(~{per_category} per category)...")

    for category in categories:
        for _ in range(per_category):
            md = generate_employee_record(category)
            name_slug = extract_name(md)
            save_markdown(name_slug, md)


if __name__ == "__main__":
    generate_dataset(total=4)
