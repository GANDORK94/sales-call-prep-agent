# Sales Call Prep Agent

A lightweight CLI tool that turns a company name, a prospect's role, and a few notes into a complete pre-call briefing. Built for sales reps who want to walk into discovery calls already two steps ahead.

## What it produces

For every account you point it at, you get a single markdown briefing with:

1. **Account snapshot**: what the company does, who they serve, and where they sit in the market.
2. **Persona profile**: what this specific role owns, cares about, and is measured on.
3. **Likely priorities**: what this person is probably focused on right now.
4. **Potential pain points**: 3 to 5 problems specific to the role and company, each with a commercial why-it-matters line.
5. **Discovery questions**: 5 open-ended questions tailored to the persona.
6. **Sample outreach**: a short email or LinkedIn message under 100 words.
7. **Assumptions and gaps**: an honest list of what is uncertain or needs verifying before the call.

Output saves to `output/[company]_[timestamp].md` so every briefing is preserved.

## Why this exists

Most cold calls and discovery calls suffer from one thing: the rep walked in cold. This tool gives you a structured, repeatable prep flow in under a minute, so you spend your time selling, not researching.

## What changed in v2 (and why)

The first version of this tool worked, but the output it produced was generic. It gave you a company overview and some pain points, but they could have applied to almost any company in that category. A rep reading it before a call would not feel meaningfully more prepared than one who had done a quick Google search.

The v2 update was about making the output actually useful, not just complete.

Three things changed:

**The agent now thinks like a seller, not a researcher.** The original prompt told the AI to behave like a "B2B sales strategist." The new one tells it to think like an SDR/AE hybrid: someone who has been on hundreds of calls, knows what questions open conversations, and can spot the difference between a real pain and a polite complaint. That shift in framing changes the tone and specificity of everything it produces.

**The output now flags what it does not know.** The original briefings presented everything with the same confidence, even when the AI was guessing. The new version labels inferences as "Assumption" and adds a dedicated section called Assumptions and Gaps at the end. This matters because walking into a call with false confidence is worse than walking in knowing what you still need to find out. The gaps section tells the rep exactly what to verify in the first few minutes of the conversation.

**The prompts were split into three separate layers.** Previously, all the instructions to the AI were bundled together in one block. Now they are separated into three distinct pieces: one that defines the agent's role and rules, one that describes the specific task for each call, and one that defines the exact structure of the output. This makes the tool easier to improve over time. If the tone feels off, you change one layer. If you want to add a new section to the briefing, you change a different layer. Nothing bleeds into anything else.

The result is a briefing that reads less like a Wikipedia summary and more like prep notes from a colleague who has already done the homework.

## Setup

Requires Python 3.9 or later and an Anthropic API key.

```bash
git clone <this-repo>
cd sales-call-prep-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your API key by creating a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_key_here
```

## Usage

Three ways to run it.

**Interactive (easiest):**

```bash
python main.py
```

**From a JSON file:**

```bash
python main.py --input sample_input.json
```

**From command-line flags:**

```bash
python main.py --company "Acme Logistics" --persona "VP of Operations" --notes "Mid-market 3PL, expanded into last-mile."
```

Generated briefings land in `output/` as timestamped markdown files.

## File structure

```
sales-call-prep-agent/
├── main.py              # CLI entry, input handling, file output
├── agent.py             # Core agent: calls the LLM, returns markdown
├── prompts.py           # All prompts: system, task template, output format
├── sample_input.json    # Example input
├── requirements.txt     # Dependencies
├── README.md
└── output/              # Generated briefings land here
```

## How it works

The agent makes one call to Claude per briefing. The prompts are split into three layers in `prompts.py`:

- **System prompt**: sets the agent's role, tone, and rules (stable across every call).
- **Task prompt template**: describes what to do with the specific company, persona, and notes for this call.
- **Output format template**: defines the exact seven-section markdown structure the model must follow.

`research_company()` in `agent.py` is a stub that returns an empty string in v1, so the model draws on its training knowledge plus whatever notes the rep provides. To plug in live web search later, swap the body of that function with a call to your preferred source (Tavily, SerpAPI, Anthropic's built-in web search, an internal CRM lookup, etc.). Nothing else needs to change.

## Roadmap (v2 ideas)

- Wire `research_company()` into a live web search tool for richer, more current context.
- Add LinkedIn or company-news lookup for the prospect specifically.
- Multi-account batch mode: feed a CSV of accounts, get back a folder of briefings.
- Push briefings into a CRM (HubSpot, Salesforce) instead of, or in addition to, local markdown.
- A second-pass critic that tightens the outreach and pressure-tests the discovery questions.
- A small evaluation harness so prompt changes can be A/B tested across a fixed set of accounts.

## License

MIT
