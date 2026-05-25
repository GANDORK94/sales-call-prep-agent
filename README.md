# Sales Call Prep Agent

A Python command-line tool that turns a company name, a prospect's job title, and a few optional notes into a structured pre-call briefing. It runs in under 30 seconds and saves every output as a timestamped markdown file you can read before picking up the phone.

---

## Why I built this

I spent several years in sales before moving into AI-enabled workflows. Before every discovery call, the prep was manual and inconsistent. Sometimes I spent twenty minutes researching. Sometimes I walked in cold. The quality of preparation depended entirely on how much time I had that day, which meant it never scaled.

This tool solves that problem. Give it a company name and a job title, and it returns a structured briefing that tells you what the person likely cares about, what questions will open a real conversation, and, just as importantly, what you do not yet know and should verify before the call.

The second goal was to build something that demonstrates how to design a practical AI workflow, not just call an API and dump unstructured text.

---

## Who it's for

- **Sales reps and SDRs** who want structured, consistent prep without spending twenty minutes on LinkedIn and Crunchbase before every call.
- **Account executives** who need a fast way to get up to speed on a new account before a handoff call.
- **Hiring managers and technical interviewers** evaluating a candidate who has built and shipped an end-to-end AI workflow.
- **Developers** looking for a practical example of prompt architecture and Claude API integration.

---

## Features

- Generates a seven-section pre-call briefing from minimal input
- Flags inferences and uncertain claims with "(Assumption)" or "(Needs verification)" rather than presenting guesses as fact
- Includes a dedicated Assumptions and Gaps section so reps know what to confirm in the first few minutes of the call
- Saves every briefing as a timestamped markdown file so nothing gets lost
- Three input modes: interactive prompts, JSON file, or command-line flags
- Prompt architecture split into three independent layers, making it easy to tune tone, sections, or output structure without rewriting the whole thing

---

## What it produces

Each briefing contains seven sections:

| Section | What it contains |
|---|---|
| **Account** | What the company does, who they serve, and their current situation |
| **Persona** | What this role owns, cares about day-to-day, and is measured on |
| **Likely Priorities** | What this person is probably focused on right now |
| **Potential Pain Points** | 3 to 5 role-specific problems, each with a commercial why-it-matters line |
| **Discovery Questions** | 5 open-ended questions that surface real problems and decision criteria |
| **Sample Outreach** | A cold email or LinkedIn message under 100 words with a low-friction ask |
| **Assumptions and Gaps** | An honest list of what is uncertain or needs verifying before the call |

---

## How it works

The agent makes one call to Claude per briefing. The prompts are structured in three layers, each with a distinct job:

**System prompt** sets the agent's role and rules. It tells Claude to think like a strong SDR/AE hybrid: concise, commercially aware, and honest about uncertainty. This layer is stable and does not change based on the prospect.

**Task prompt template** injects the specific inputs for this call: company name, persona title, and any rep notes. It tells the model what to do with those inputs.

**Output format template** defines the exact seven-section markdown structure the model must follow. Each section has a brief instruction so the model knows what "good" looks like, not just what the section is called.

These three layers are defined separately in `prompts.py`. If you want to change the tone, you edit the system prompt. If you want to add a new section, you edit the output format. Nothing bleeds into anything else.

The `research_company()` function in `agent.py` is currently a stub that returns an empty string. In this version, Claude draws on its training knowledge plus whatever notes the rep provides. The stub is the intended extension point for v2: swap the body of that function with a call to a live search tool (Tavily, SerpAPI, or Anthropic's built-in web search) and the rest of the agent does not need to change.

---

## Tech stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) | Claude API client |
| Claude Sonnet (claude-sonnet-4-6) | Language model |
| python-dotenv | Loads the API key from a local `.env` file |

No frameworks. No databases. No web server. The entire tool is four Python files and two dependencies.

---

## File structure

```
sales-call-prep-agent/
├── main.py              # CLI entry point: handles input modes and saves output
├── agent.py             # Calls the Claude API and returns a markdown briefing
├── prompts.py           # Three-layer prompt architecture: system, task, output format
├── sample_input.json    # Example JSON input for quick testing
├── requirements.txt     # anthropic and python-dotenv
├── README.md
└── output/              # Generated briefings saved here as timestamped .md files
```

---

## Example input

**From a JSON file:**

```json
{
  "company": "Acme Logistics",
  "persona": "VP of Operations",
  "notes": "Mid-market 3PL based in the Midwest. Recently expanded into last-mile delivery. We sell route optimization software that reduces fuel costs and missed delivery windows."
}
```

**From the command line:**

```bash
python main.py --company "Acme Logistics" --persona "VP of Operations" --notes "Mid-market 3PL, expanded into last-mile."
```

---

## Example output

The following is an excerpt from a real briefing generated for a Head of Engineering at a Series B dev tooling company.

---

**## Persona**
The Head of Engineering at a company this size typically owns engineering productivity, team structure, and delivery reliability. Day to day, they are navigating sprint planning, cross-functional alignment with product, and keeping engineers unblocked. They are likely measured on shipping velocity, team retention, and their ability to scale the org without introducing process debt.

**## Potential Pain Points**
- **Jira overhead eating into engineering time.** When engineers spend meaningful time updating tickets or navigating complex workflows, that is time not spent shipping. At a Series B company, velocity is a competitive advantage, and anything slowing it down has a direct cost.
- **Tooling that does not reflect how modern engineering teams actually work.** If the workflow does not match how the team thinks, engineers route around it, which means the data in the tool becomes unreliable for the Head of Engineering trying to understand delivery health.
- **Constant team complaints becoming a management distraction.** If engineers are vocal about tooling frustration, the Head of Engineering is fielding that feedback and choosing between fixing it or absorbing the morale cost.

**## Discovery Questions**
1. When your engineers push back on Jira, what specifically are they running into? Is it the day-to-day workflow, the setup and configuration, or something else?
2. How are you currently getting visibility into what is actually in progress versus what is at risk in a given sprint or cycle?
3. If you were to replace Jira, what would the team need to see to feel confident the new tool was actually better and not just different?

**## Assumptions and Gaps**
- Headcount is estimated at 50 to 100 engineers. Confirm actual size and growth rate.
- It is unclear whether the Head of Engineering owns the tooling decision or whether it sits with engineering managers, a VP of Engineering, or an internal platform team.
- No information on whether there is an active evaluation underway or a budget cycle approaching. Try to surface this early.

---

## How to run locally

**1. Clone the repo and navigate into it**

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

Get a key at [console.anthropic.com](https://console.anthropic.com). You will need a small amount of API credit. A $5 top-up runs hundreds of briefings.

**5. Run the agent**

```bash
python main.py --input sample_input.json
```

Or interactively:

```bash
python main.py
```

The briefing saves to `output/` automatically.

---

## Limitations

- **No live web search.** The agent draws on Claude's training knowledge and whatever notes you provide. It does not look up current news, recent funding rounds, or live job postings. The `research_company()` function in `agent.py` is the intended hook for adding this in v2.
- **One briefing per run.** Batch mode (feed a CSV, get back a folder of briefings) is not yet implemented.
- **Output quality depends on input quality.** A company name alone produces a generic briefing. The more context you give in the notes field, the more specific and useful the output.
- **No CRM integration.** Briefings save as local markdown files. Pushing them into HubSpot, Salesforce, or a shared drive is a future improvement.

---

## Future improvements

- Wire `research_company()` into a live search API (Tavily, SerpAPI, or Anthropic's built-in web search) for current, sourced context.
- Add LinkedIn profile or recent news lookup for the specific prospect.
- Batch mode: accept a CSV of accounts and output a folder of briefings.
- CRM integration: push briefings directly into HubSpot or Salesforce as notes on the contact record.
- A second-pass review step that tightens the outreach draft and pressure-tests the discovery questions.
- An evaluation harness so prompt changes can be tested against a fixed set of sample accounts before being deployed.

---

## Why this project matters

### What it demonstrates technically

This project is a practical example of how to design a structured AI workflow rather than just write a prompt and hope for the best.

Most early AI projects make one mistake: they treat the language model as a magic box where you put a question in and get an answer out. That works for simple tasks but breaks down quickly when you need consistent, structured, trustworthy output at scale.

This agent was built with a different approach:

**Separation of concerns in the prompt layer.** The instructions to the model are split into three named layers: one that defines the agent's role and rules, one that describes the task for this specific call, and one that defines the exact output structure. Each layer can be edited independently. This is the same kind of thinking that makes software maintainable: you should be able to change the tone of the agent without accidentally changing its output format.

**Epistemic honesty as a design requirement.** The agent is explicitly instructed to label uncertain claims as "Assumption" or "Needs verification" and to surface everything it does not know in a dedicated section. This is not a minor detail. An agent that presents guesses with the same confidence as known facts is not useful in a professional context. Building in honesty as a rule, not an afterthought, is one of the things that separates a usable tool from a demo.

**A clean extension point for tool use.** The `research_company()` function is currently a stub. Its job is to return context about the company before the prompt is built. In v2, that function becomes the agent's tool call: a live web search, a CRM lookup, a news API. The rest of the system does not change. This reflects how real agentic systems are designed: the reasoning loop stays stable while the tools it can call expand over time.

### What it demonstrates professionally

This project was built by someone who has sat on the phone doing discovery calls and knows what a useful briefing actually looks like versus one that sounds good but does not help. The output sections, the assumptions flagging, and the Assumptions and Gaps section at the end are not arbitrary design choices. They reflect what a rep actually needs before a call: what to anchor the conversation on, what questions to ask, and what they do not yet know.

Building a tool that solves a problem you have personally experienced, and designing it well enough to extend it, is the point.

---

## License

MIT
