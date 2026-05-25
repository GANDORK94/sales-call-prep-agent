"""
Core agent logic for the Sales Call Prep Agent.

Exposes generate_briefing(), which takes a company name, prospect persona,
and optional notes, and returns a markdown-formatted call prep briefing.
"""

from anthropic import Anthropic

from prompts import SYSTEM_PROMPT, build_user_prompt

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2500


def research_company(company):
    """
    Optional research step. Returns context about the company that gets
    passed into the prompt.

    In v1 this is a stub and returns an empty string. The model relies on its
    training knowledge plus any notes the rep provides.

    To upgrade in v2, plug in a search tool here (Tavily, SerpAPI, Anthropic's
    built-in web search, an internal CRM lookup, etc.) and return a string of
    relevant context. Keep the function signature stable so the rest of the
    agent does not need to change.
    """
    return ""


def generate_briefing(company, persona, notes=""):
    """
    Generate a full sales call prep briefing for a single account.

    Returns a markdown string with five sections:
      1. Company Overview
      2. Likely Pain Points
      3. Discovery Questions
      4. Sample Cold Email
      5. Pre-Call Briefing
    """
    research = research_company(company)
    user_prompt = build_user_prompt(company, persona, notes, research)

    client = Anthropic()  # Reads ANTHROPIC_API_KEY from the environment

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return response.content[0].text
