# Sales Call Prep Agent

A Python CLI tool that turns a company name, a prospect's job title, and a few optional notes into a structured pre-call briefing. Runs in under 30 seconds. Output saves as a timestamped markdown file.

---

## Overview

I spent several years in sales before moving into AI-enabled workflows. Before every discovery call, prep was manual and inconsistent. Sometimes I spent twenty minutes researching. Sometimes I walked in cold. The quality of preparation depended entirely on how much time I had that day.

This tool solves that. Give it a company name and a title, and it returns a briefing that tells you what the person likely cares about, what questions will open a real conversation, and what you do not yet know and should verify before the call. That last part matters as much as the rest.

---

## What it produces

| Section | What it contains |
|---|---|
| **Account** | What the company does, who they serve, and their current situation |
| **Persona** | What this role owns, cares about day-to-day, and is measured on |
| **Likely Priorities** | What this person is probably focused on right now |
| **Potential Pain Points** | 3 to 5 role-specific problems, each with a commercial why-it-matters line |
| **Discovery Questions** | 5 open-ended questions tailored to this persona |
| **Sample Outreach** | A cold email or LinkedIn message under 100 words |
| **Assumptions and Gaps** | What is uncertain and should be verified before the call |

---

## Example output

The following is excerpted from a real briefing generated for a Head of Engineering at a Series B dev tooling company. [See the full output here](output/example_briefing.md).

---

### Persona
The Head of Engineering at a company this size typically owns engineering productivity, team structure, and delivery reliability. Day to day, they are navigating sprint planning, cross-functional alignment with product, and keeping engineers unblocked. They are likely measured on shipping velocity, team retention, and their ability to scale the org without introducing process debt.

### Potential Pain Points
- **Jira overhead eating into engineering time.** When engineers spend meaningful time updating tickets or navigating complex workflows, that is time not spent shipping. At a Series B company, velocity is a competitive advantage, and anything slowing it down has a direct cost.
- **Lack of visibility into real progress without manual effort.** Getting a clear picture of what is in flight, what is blocked, and what is at risk often requires chasing updates or running standup questions that should already have answers.

### Discovery Questions
1. When your engineers push back on Jira, what specifically are they running into? Is it the day-to-day workflow, the setup and configuration, or something else?
2. How are you currently getting visibility into what is actually in progress versus what is at risk in a given sprint or cycle?
3. If you were to replace Jira, what would the team need to see to feel confident the new tool was actually better and not just different?

### Assumptions and Gaps
- Headcount is estimated at 50 to 100 engineers. Confirm actual size and growth rate.
- It is unclear whether the Head of Engineering owns the tooling decision or whether it sits with engineering managers or an internal platform team.
- No information on whether there is an active evaluation underway. Try to surface this early.

---

## How to run locally

**1. Clone the repo**

```bash
git clone https://github.com/GANDORK94/sales-call-prep-agent.git
cd sales-call-prep-agent
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your Anthropic API key**

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com). A $5 credit top-up runs hundreds of briefings.

**5. Run it**

```bash
# From a JSON file
python main.py --input sample_input.json

# From command-line flags
python main.py --company "Acme Logistics" --persona "VP of Operations" --notes "Mid-market 3PL, expanded into last-mile."

# Interactive
python main.py
```

Briefings save to `output/` automatically.

---

## How it works

The agent makes one call to Claude per briefing. The prompts are split into three named layers in `prompts.py`:

- **System prompt** sets the agent's role and rules: think like an SDR/AE hybrid, be specific when you have evidence and general when you do not, label anything uncertain. This layer does not change based on the prospect.
- **Task prompt template** injects the specific inputs for this call: company name, persona title, and any rep notes.
- **Output format template** defines the exact seven-section markdown structure the model must follow, with per-section instructions so the model knows what good looks like, not just what the section is called.

Each layer is edited independently. Changing the tone does not touch the output format. Adding a section does not touch the system rules.

The `research_company()` function in `agent.py` is a stub that currently returns an empty string. That is the intended extension point: swap the body with a call to a live search API and the rest of the agent does not need to change.

---

## Tech stack

| | |
|---|---|
| Python 3.9+ | Core language |
| [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) | Claude API client |
| Claude Sonnet (`claude-sonnet-4-6`) | Language model |
| python-dotenv | Loads the API key from `.env` |

No frameworks. No databases. Four Python files and two dependencies.

---

## File structure

```
sales-call-prep-agent/
├── main.py              # CLI entry point: input modes, validation, file output
├── agent.py             # Calls the Claude API, returns markdown
├── prompts.py           # Three-layer prompt architecture: system, task, format
├── sample_input.json    # Example input for quick testing
├── requirements.txt     # Dependencies
└── output/
    └── example_briefing.md   # Full example output
```

---

## Limitations

- **No live web search.** The agent draws on Claude's training knowledge plus whatever notes you provide. It does not fetch current news, recent funding rounds, or live job postings. The `research_company()` stub in `agent.py` is the hook for adding this later.
- **One briefing per run.** Batch mode is not yet implemented.
- **Output quality scales with input quality.** A company name alone produces a more generic briefing than one with specific rep notes.
- **No CRM integration.** Briefings save as local markdown files.

---

## Future improvements

- Connect `research_company()` to a live search API (Tavily, SerpAPI, or Anthropic's web search tool) for current, sourced context
- Add LinkedIn profile or recent news lookup for the specific prospect
- Batch mode: accept a CSV of accounts, output a folder of briefings
- CRM push: write briefings directly into HubSpot or Salesforce as contact notes
- A second-pass step that tightens the outreach draft and pressure-tests the discovery questions

---

## Design notes

The most common mistake in early AI projects is treating the model as a black box: put a question in, get an answer out, ship it. That breaks down when you need consistent, structured, trustworthy output across many different inputs. This project is built around three deliberate choices. First, the prompts are split into separate layers so tone, task, and output structure can each be changed without affecting the others. Second, the agent is explicitly instructed to label inferences as assumptions and surface uncertainty in a dedicated section, because a briefing that presents guesses as facts is worse than no briefing. Third, the research function is a named stub, not an afterthought, because the right place to extend an agent's capabilities is a defined interface, not a scattered rewrite. These are the same decisions that make any software system easier to maintain and extend over time.

---

## License

MIT
