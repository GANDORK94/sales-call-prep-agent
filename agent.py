"""
Core agent logic for the Sales Call Prep Agent.

Exposes generate_briefing(), which takes a company name, persona title,
and optional rep notes, and returns a markdown sales call brief.
"""

from anthropic import Anthropic

from prompts import SYSTEM_PROMPT, build_user_prompt

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 3000


def research_company(company_name):
    """
    Stub for a future live research step.

    Returns an empty string in v1. The model falls back to its training
    knowledge plus any notes the rep provides.

    To upgrade: replace the body with a call to Tavily, SerpAPI, Anthropic's
    built-in web search, or an internal CRM lookup. Return a plain string of
    relevant context. The rest of the agent does not need to change.
    """
    return ""


def generate_briefing(company_name, persona_title, notes=""):
    """
    Generate a sales call brief for a single prospect.

    Returns a markdown string with seven sections:
      - Account
      - Persona
      - Likely Priorities
      - Potential Pain Points
      - Discovery Questions
      - Sample Outreach
      - Assumptions / Gaps
    """
    research = research_company(company_name)
    if research:
        notes = f"{notes}\n\nResearch context:\n{research}".strip()

    user_prompt = build_user_prompt(company_name, persona_title, notes)

    client = Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return response.content[0].text
