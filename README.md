# Sales Call Prep Agent

A lightweight CLI tool that turns a company name, a prospect's role, and a few notes into a complete pre-call briefing. Built for sales reps who want to walk into discovery calls already two steps ahead.

## What it produces

For every account you point it at, you get a single markdown briefing with:

1. **Company overview**: a short read on what the company does and where it plays.
2. **Likely pain points**: 3 to 5 problems the persona is probably wrestling with.
3. **5 discovery questions**: open-ended, tailored to the role.
4. **Sample cold email**: under 120 words, low-friction ask.
5. **Pre-call briefing**: a 5 to 6 line scan you can read 60 seconds before the call.

Output saves to `output/[company]_[timestamp].md` so every briefing is preserved.

## Why this exists

Most cold calls and discovery calls suffer from one thing: the rep walked in cold. This tool gives you a structured, repeatable prep flow in under a minute, so you spend your time selling, not researching.

## Setup

Requires Python 3.9 or later and an Anthropic API key.

```bash
git clone <this-repo>
cd sales-call-prep-agent
pip install -r requirements.txt
```

Set your API key. Either export it:

```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or create a `.env` file in the project root:

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
├── prompts.py           # System prompt and user prompt builder
├── sample_input.json    # Example input
├── requirements.txt     # Dependencies
├── README.md
└── output/              # Generated briefings land here
    └── acme_logistics_example.md
```

## How it works

The agent makes one call to Claude per briefing. The system prompt enforces a direct, sales-friendly tone, and the user prompt instructs the model to produce all five sections in markdown with consistent headers.

Research is handled by `research_company()` in `agent.py`. In v1 it returns an empty string, so the model uses its own knowledge plus whatever notes you pass in. To plug in real web search later, swap the body of `research_company()` with a call to your preferred source (Tavily, SerpAPI, Anthropic's built-in web search, an internal CRM lookup, etc.). The rest of the agent does not need to change.

## Roadmap (v2 ideas)

- Wire `research_company()` into a live web search tool for richer context.
- Add LinkedIn or company-news lookup for the prospect specifically.
- Multi-account batch mode: feed a CSV of accounts, get back a folder of briefings.
- Push briefings into a CRM (HubSpot, Salesforce) instead of, or in addition to, local markdown.
- A second-pass critic that tightens the cold email and pressure-tests the discovery questions.
- A small evaluation harness so prompt changes can be A/B tested across a fixed set of accounts.

## License

MIT
