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

The following is excerpted from a real briefing generated for a VP of Sales at Capital One. [See the full output here](output/example_briefing.md), including the Agent Review Notes at the end.

---

### Persona
This VP likely owns revenue or portfolio targets across a distributed team of AEs or relationship managers, with day-to-day focus on pipeline health, forecast accuracy, and whether their reps are showing up to customer conversations ready to have the right discussion. They are measured on quota attainment and team productivity, which means rep ramp time and call quality inconsistency are personal problems, not abstract ones.

### Potential Pain Points
- **Inconsistent call preparation across the team.** When reps do their own research differently, some show up sharp and some show up generic, and the VP has no lever to fix that at scale without a process change.
- **Managers spending coaching time on basics instead of strategy.** If frontline managers are reviewing decks and coaching reps on who the buyer is, they are not spending time on deal strategy or skill development where it actually matters.

### Discovery Questions
1. When you think about your top-performing reps versus the rest of the team, what do you see them doing differently in how they prepare for a first call?
2. How are your AEs currently researching prospects before discovery calls, and how much time are they typically spending on that?
3. When a deal stalls after the first call, what do you usually trace it back to in your deal reviews?

### Agent Review Notes
*This section is generated automatically by the self-check step.*

Pain point "High prep time per call" cites a 45-minute figure presented as fact — label as assumption or benchmark, not Capital One-specific data. Discovery questions 1 and 3 can be answered with a short closed response — reframe to "walk me through" to force a real answer. The brief is otherwise strong, especially the Assumptions and Gaps section.

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

The agent runs four steps per briefing, each a separate call to Claude:

| Step | What it does |
|---|---|
| **1. Plan** | Decides the angle to take before generating anything |
| **2. Context** | Organizes what is known about the company and persona |
| **3. Brief** | Generates the full seven-section briefing, informed by steps 1 and 2 |
| **4. Review** | Reads its own output and flags weak spots: generic claims, bad questions, unlabeled assumptions |

When you run the agent you see each step as it happens:

```
Preparing briefing for VP of Sales at Capital One...

  Planning approach...
  Gathering context...
  Generating briefing...
  Running self-check...

Done. Briefing saved to: output/capital_one_20260525_1428.md
```

Each step is a separate function in `agent.py`. Each prompt lives in `prompts.py` and can be edited without touching any other step. A single system prompt applies to all four calls and sets the agent's role and rules.

`gather_context()` in `agent.py` is the intended hook for live web search in v2. Add a search API call there and the results feed directly into the briefing step without changing anything else.

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
