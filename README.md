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

You will do everything through the Terminal app on your Mac. No coding experience needed — just copy and paste each command exactly as shown.

---

### Step 1 — Open Terminal

Press **Command + Space**, type **Terminal**, and hit Enter. A black or white window will open with a `%` prompt. That is where you type commands.

---

### Step 2 — Download the project

Copy and paste this command, then hit Enter:

```bash
git clone https://github.com/GANDORK94/sales-call-prep-agent.git ~/Desktop/sales-call-prep-agent
```

This saves the project to your Desktop.

---

### Step 3 — Navigate into the project folder

```bash
cd ~/Desktop/sales-call-prep-agent
```

> **Important:** You must run this command every time you open a new Terminal window before doing anything else. Think of it as "opening the project folder" — all other commands only work from inside it.

---

### Step 4 — Set up a Python environment

Copy and paste both lines, hitting Enter after each:

```bash
python3 -m venv venv
source venv/bin/activate
```

After the second line, your prompt will change to start with `(venv)`. That means it worked. You will need to run `source venv/bin/activate` again any time you open a new Terminal window.

---

### Step 5 — Install the required packages

```bash
pip install -r requirements.txt
```

This only needs to be done once.

---

### Step 6 — Add your API key

The tool uses Claude to generate briefings. You need a free API key from Anthropic.

1. Go to [console.anthropic.com](https://console.anthropic.com) and create an account
2. Get your API key from the dashboard
3. In the project folder, create a file called `.env` and add this line:

```
ANTHROPIC_API_KEY=your_key_here
```

Replace `your_key_here` with your actual key. A $5 credit top-up runs hundreds of briefings.

To create the `.env` file from Terminal:

```bash
echo 'ANTHROPIC_API_KEY=your_key_here' > .env
```

Replace `your_key_here` with your actual key before running it.

---

### Step 7 — Run it

```bash
python3 main.py
```

The tool will ask you for a company name, a job title, and any notes. Fill those in and it will generate your briefing. Output saves automatically to the `output/` folder on your Desktop inside the project.

You can also run it with everything on one line:

```bash
python3 main.py --company "Acme Logistics" --persona "VP of Operations" --notes "Mid-market 3PL, expanded into last-mile."
```

---

### Step 8 — View your output

Briefings save as `.md` files in the `output/` folder. To read one in the Terminal without needing VS Code or any other app installed, use one of these commands.

**List all saved briefings:**

```bash
ls output/
```

**Read a file (prints the whole thing at once):**

```bash
cat output/filename.md
```

**Read a file with scroll controls (better for long files):**

```bash
less output/filename.md
```

Use the arrow keys to scroll. Press `q` to exit.

Replace `filename.md` with the name shown when you ran `ls output/`.

---

### Every time you come back

Open Terminal and run these two lines before anything else:

```bash
cd ~/Desktop/sales-call-prep-agent
source venv/bin/activate
```

Then run `python3 main.py` to generate a briefing.

---

### Something went wrong?

| What you see | What to do |
|---|---|
| `no such file or directory: sales-call-prep-agent` | You skipped Step 3. Run `cd ~/Desktop/sales-call-prep-agent` |
| `can't open file 'main.py'` | You are not in the project folder. Run `cd ~/Desktop/sales-call-prep-agent` |
| `No such file or directory: 'requirements.txt'` | Same fix — run `cd ~/Desktop/sales-call-prep-agent` first |
| `No module named 'dotenv'` | Run `source venv/bin/activate` then `pip install -r requirements.txt` |
| `AuthenticationError` | Your API key is missing or incorrect. Check your `.env` file |

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

| Tool | Purpose |
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
├── prompts.py           # One prompt per agent step plus a shared system prompt
├── sample_input.json    # Example input for quick testing
├── requirements.txt     # Dependencies
└── output/
    └── example_briefing.md   # Full example output
```

---

## Limitations

- **No live web search.** The agent draws on Claude's training knowledge plus whatever notes you provide. It does not fetch current news, recent funding rounds, or live job postings. `gather_context()` in `agent.py` is the intended hook for adding this in v2.
- **One briefing per run.** Batch mode is not yet implemented.
- **Output quality scales with input quality.** A company name alone produces a more generic briefing than one with specific rep notes.
- **No CRM integration.** Briefings save as local markdown files.

---

## Future improvements

- Connect `gather_context()` to a live search API (Tavily, SerpAPI, or Anthropic's web search tool) for current, sourced context
- Add LinkedIn profile or recent news lookup for the specific prospect
- Batch mode: accept a CSV of accounts, output a folder of briefings
- CRM push: write briefings directly into HubSpot or Salesforce as contact notes
- A second-pass step that tightens the outreach draft and pressure-tests the discovery questions

---

## Design notes

What makes this an agent rather than a script: each step uses the output of the previous one as input, the system plans before it generates, and it reviews its own output before returning anything. The workflow is sequential and stateful, not a single prompt with a single response.

Three specific decisions worth noting:

- **Prompts are separated by step, not bundled.** Changing the tone of the planning step does not affect the briefing format. Adding a new output section does not touch the system rules. Each layer can be changed independently.
- **Uncertainty is a first-class output.** The agent is instructed to label inferences as assumptions and surface everything it does not know in a dedicated section. A briefing that presents guesses as facts is worse than no briefing.
- **The extension point is named.** `gather_context()` in `agent.py` is where live search goes when this gets upgraded. It is a defined interface, not a comment in a README.

---

