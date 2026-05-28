# 🤖 WebPilot — Autonomous Web Agent

> **Microsoft Build AI Hackathon 2026** — Theme: *Agentic Web*
>
> **Team:** Nishchal Soni & Kuldeep Parmar

---

## 🎯 What is WebPilot?

AI chatbots *answer* questions. **WebPilot *does* things.**

Give it a natural-language goal like:

> *"Find the cheapest flight from Delhi to Mumbai next Friday and hold a ticket"*

WebPilot autonomously:
1. Opens a travel aggregator
2. Fills in origin, destination, and date
3. Filters and sorts results by price
4. Navigates to checkout
5. Returns the fare and booking details — no scripts, no APIs, no human in the loop

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────┐
│                    WebPilot Agent                      │
│                                                        │
│   Natural Language Task                                │
│          │                                             │
│          ▼                                             │
│   ┌─────────────────┐      Tool calls                 │
│   │  Claude (LLM)   │ ──────────────────────┐         │
│   │  Planner +      │                       │         │
│   │  Reasoner       │ ◄──── Tool results ───┘         │
│   └─────────────────┘                       │         │
│          │                                  │         │
│          ▼                                  │         │
│   ┌─────────────────────────────────────┐   │         │
│   │        Browser Controller           │◄──┘         │
│   │  (Playwright — Chromium/Firefox)    │             │
│   │  navigate · click · type · scroll   │             │
│   │  screenshot · extract · go_back     │             │
│   └─────────────────────────────────────┘             │
└──────────────────────────────────────────────────────┘
```

### How the loop works

```
1. User gives high-level task
2. Claude reasons about a plan
3. Claude calls a browser tool (navigate, click, type_text, …)
4. Browser executes the action on the real live web
5. Result returned to Claude
6. Claude observes → adjusts → calls next tool
7. Repeat until task_complete() or task_failed()
```

---

## 🌟 Core Capabilities

| Capability | How it works |
|---|---|
| **Multi-step planning** | Claude decomposes goals into ordered sub-tasks before acting |
| **Resilient execution** | 5-strategy click fallback (CSS → exact text → partial → role button → role link) |
| **Adaptive re-planning** | On failure, Claude revises its approach mid-execution |
| **Structured extraction** | Claude reads page DOM and returns typed results |
| **Form interaction** | Fills search boxes, selects dropdowns, presses Enter — full UX flows |
| **Multi-site workflows** | Can hop across domains within a single task |

---

## 📦 Project Structure

```
webpilot/
├── __init__.py       — Package entry point
├── agent.py          — Core agentic loop (Claude ↔ browser)
├── browser.py        — Playwright browser controller (resilient actions)
├── tools.py          — Claude tool-use schemas (11 browser tools)
├── config.py         — All tuneable settings
├── main.py           — Interactive CLI
├── demo.py           — 5 showcase demo scenarios
├── requirements.txt  — Python dependencies
├── .env.example      — Environment template
└── README.md         — This file
```

---

## 🚀 Quick Start

### 1 — Prerequisites

```bash
# Python 3.11+
python --version

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 2 — Set your API key

```bash
# Option A — environment variable
export ANTHROPIC_API_KEY="sk-ant-..."

# Option B — .env file
cp .env.example .env
# then edit .env and fill in your key
```

### 3 — Run the interactive CLI

```bash
python main.py
```

You'll see a numbered menu of sample tasks or can type any free-form goal.

### 4 — Run the demo suite

```bash
# Interactive demo menu
python demo.py

# Run a specific demo (e.g. demo 2)
python demo.py --task 2

# Run all 5 demos headless and save JSON results
python demo.py --all
```

---

## 🔧 Available Browser Tools

The agent can invoke any of these 11 tools in any order:

| Tool | What it does |
|---|---|
| `navigate(url)` | Open any URL |
| `get_page_content()` | Read title, text, interactive elements |
| `click_element(description)` | Click button/link by text or CSS selector |
| `type_text(selector, text)` | Fill input fields |
| `press_key(key)` | Enter, Tab, Escape, ArrowDown … |
| `scroll(direction, amount)` | Reveal off-screen content |
| `go_back()` | Browser back button |
| `select_option(selector, value)` | Dropdown selection |
| `wait(ms)` | Pause for page load |
| `screenshot()` | Visual snapshot for debugging |
| `task_complete(summary, result)` | Signal success + return data |
| `task_failed(reason)` | Signal irrecoverable failure |

---

## 📋 Demo Scenarios

| # | Demo | Highlights |
|---|---|---|
| 1 | 🔍 Web Search & Summarise | Google navigation, link following, content extraction |
| 2 | 📰 News Aggregation | Direct navigation, structured data extraction |
| 3 | 🛒 E-commerce Research | Flipkart search, price + rating extraction |
| 4 | 📚 Knowledge Retrieval | Wikipedia multi-fact extraction |
| 5 | ✈️ Travel Price Research | MakeMyTrip multi-step form, fare comparison |

---

## 💡 Usage in Code

```python
import asyncio
from webpilot import WebPilotAgent

async def main():
    async with WebPilotAgent(api_key="sk-ant-...", headless=False) as agent:
        result = await agent.run_task(
            "Go to Amazon.in, search for 'mechanical keyboard', "
            "and find the best-rated one under ₹3000"
        )
        if result["success"]:
            print("✅", result["result"])
        else:
            print("❌", result["reason"])

asyncio.run(main())
```

### Result object

```python
{
    "success": True,
    "task": "...",          # original task string
    "summary": "...",       # what the agent did
    "result": "...",        # the final answer/data
    "steps": 12,            # LLM calls made
    "actions": 18,          # browser actions taken
    "elapsed_s": 43.2       # wall-clock time
}
```

---

## ⚙️ Configuration

```python
from webpilot import WebPilotAgent

agent = WebPilotAgent(
    api_key    = "sk-ant-...",
    headless   = True,       # False = visible Chrome window
    max_steps  = 30,         # max LLM reasoning rounds
    model      = "claude-opus-4-5",
)
```

---

## 🛡 Safety

- Never submits real payment information
- For e-commerce tasks: navigates to checkout but does **not** place orders
- Respects site robots.txt through normal browser behaviour
- Max-steps guard prevents infinite loops

---

## 🏆 Why This Wins

| Judging Criterion | WebPilot's Approach |
|---|---|
| **Smart enough to plan** | Claude decomposes any goal into sub-tasks before acting |
| **Resilient enough to recover** | 5-strategy click fallback + mid-task re-planning |
| **End-to-end execution** | Handles full workflows across multiple sites without hand-holding |
| **Real, working solution** | Live Playwright browser — no mocks, no canned responses |
| **Users never go back** | Any web task reduces to a one-line natural language instruction |

---

## 👥 Team

| Name | Role |
|---|---|
| **Nishchal Soni** | Agent Architecture, LLM Integration |
| **Kuldeep Parmar** | Browser Automation, Resilience Layer |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) file.
