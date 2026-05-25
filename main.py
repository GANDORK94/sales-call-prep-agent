"""
CLI entry point for the Sales Call Prep Agent.

Three ways to run it:
    python main.py                                    # interactive prompts
    python main.py --input sample_input.json          # from a JSON file
    python main.py --company "Acme" --persona "VP Ops"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from agent import generate_briefing


def get_inputs_interactively():
    print("\n=== Sales Call Prep Agent ===\n")
    company = input("Company name: ").strip()
    persona = input("Prospect role/title: ").strip()
    notes = input("Optional notes (press Enter to skip): ").strip()
    return company, persona, notes


def load_inputs_from_file(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data["company"], data["persona"], data.get("notes", "")


def save_output(content, company):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    slug = company.lower().replace(" ", "_").replace("/", "_").replace(".", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = output_dir / f"{slug}_{timestamp}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def main():
    # Loads ANTHROPIC_API_KEY from a .env file if present. Safe no-op otherwise.
    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate a sales call prep briefing.")
    parser.add_argument("--input", "-i", help="Path to a JSON input file")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--persona", help="Prospect role or title")
    parser.add_argument("--notes", default="", help="Optional notes for context")
    args = parser.parse_args()

    if args.input:
        company, persona, notes = load_inputs_from_file(args.input)
    elif args.company and args.persona:
        company, persona, notes = args.company, args.persona, args.notes
    else:
        company, persona, notes = get_inputs_interactively()

    if not company or not persona:
        print("Error: company and persona are both required.")
        sys.exit(1)

    print(f"\nGenerating briefing for {persona} at {company}...")

    try:
        briefing = generate_briefing(company, persona, notes)
    except Exception as e:
        print(f"\nError generating briefing: {e}")
        print("Check that ANTHROPIC_API_KEY is set in your environment.")
        sys.exit(1)

    output_path = save_output(briefing, company)
    print(f"\nBriefing saved to: {output_path}\n")


if __name__ == "__main__":
    main()
