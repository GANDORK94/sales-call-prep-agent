"""
Core agent logic for the Sales Call Prep Agent.

Runs a four-step workflow per briefing:
  1. plan_approach  -- decide the angle before generating
  2. gather_context -- organize what is known about the company
  3. generate_brief -- produce the full seven-section briefing
  4. review_brief   -- flag weak spots in the output

run_agent() is the main entry point. It runs all four steps and returns
a formatted markdown string ready to save.

Each step is a separate function so they can be read, tested, or swapped
out independently. To add live web search, extend gather_context().
"""

from datetime import datetime

from anthropic import Anthropic

from prompts import (
    SYSTEM_PROMPT,
    PLANNING_PROMPT,
    CONTEXT_PROMPT,
    BRIEFING_PROMPT,
    REVIEW_PROMPT,
)

MODEL = "claude-sonnet-4-6"


def _call(client, prompt, max_tokens):
    """Make a single API call and return the text response."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def plan_approach(client, company_name, persona_title, notes):
    """Step 1: Plan the angle before generating the brief."""
    prompt = PLANNING_PROMPT.format(
        company_name=company_name,
        persona_title=persona_title,
        notes=notes or "None provided.",
    )
    return _call(client, prompt, max_tokens=400)


def gather_context(client, company_name, persona_title, plan):
    """Step 2: Organize what is known about the company and persona."""
    prompt = CONTEXT_PROMPT.format(
        company_name=company_name,
        persona_title=persona_title,
        plan=plan,
    )
    return _call(client, prompt, max_tokens=600)


def generate_brief(client, company_name, persona_title, notes, plan, context):
    """Step 3: Generate the full seven-section briefing."""
    prompt = BRIEFING_PROMPT.format(
        company_name=company_name,
        persona_title=persona_title,
        notes=notes or "None provided.",
        plan=plan,
        context=context,
    )
    return _call(client, prompt, max_tokens=3000)


def review_brief(client, brief):
    """Step 4: Flag weak spots in the generated output."""
    prompt = REVIEW_PROMPT.format(brief=brief)
    return _call(client, prompt, max_tokens=400)


def format_output(company_name, persona_title, brief, review):
    """Assemble the final markdown document with metadata and review notes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""# Sales Call Brief

**Company:** {company_name}
**Persona:** {persona_title}
**Generated:** {timestamp}

---

{brief}

---

## Agent Review Notes

{review}
"""


def run_agent(company_name, persona_title, notes="", on_step=None):
    """
    Run the full four-step agent workflow and return formatted markdown.

    on_step is an optional callback that receives a status string at each step.
    main.py uses it to print progress without this module knowing about the UI.
    """
    def step(msg):
        if on_step:
            on_step(msg)

    client = Anthropic()

    step("Planning approach...")
    plan = plan_approach(client, company_name, persona_title, notes)

    step("Gathering context...")
    context = gather_context(client, company_name, persona_title, plan)

    step("Generating briefing...")
    brief = generate_brief(client, company_name, persona_title, notes, plan, context)

    step("Running self-check...")
    review = review_brief(client, brief)

    return format_output(company_name, persona_title, brief, review)
