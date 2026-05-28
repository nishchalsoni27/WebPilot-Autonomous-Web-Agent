import os

# Create the directory structure for webpilot if it doesn't exist to make it a neat clean package layout representation
os.makedirs("webpilot", exist_ok=True)

readme_content = """# WebPilot — Autonomous Web Agent

An elegant, local deterministic web automation agent designed for the **Microsoft Build AI Hackathon 2026**. 

WebPilot drives browser actions end-to-end via a localized rule-based parser combined with a robust **Playwright** framework. This project architecture simulates the exact tool-use loop patterns of large language models (LLM) completely locally, executing complex multi-step workflows across live sites with **zero API costs**, **no keys required**, and **unlimited offline performance evaluation**.

---

## 🚀 Key Features

* **Zero-API Autonomous Loop:** Emulates an intelligent task orchestrator that parses user objectives into structured operational tool calls entirely on your machine.
* **Resilient Browser Controller:** Built on Playwright with built-in multi-strategy selectors (exact text matching, positional fallback tracking, human-like delays, and automatic viewport hidden flag bypasses).
* **Rich Console Layout:** High-fidelity interactive CLI terminal dashboards with structured logging panels, automated runtime stats, and task-success tracing wrappers.
* **Pre-Engineered Benchmarks:** Ready-to-run showcase configurations optimized to complete real-world web navigation tasks automatically.

---

## 📂 Repository Blueprint
```text
webpilot-agent/
├── .env                  # Environment management file layout stub
├── requirements.txt      # Core python runtime dependency manifests
├── setup.py              # Packaging configurations for direct executable script distribution
├── main.py               # Main terminal launcher for the interactive multi-task sandbox
├── demo.py               # Benchmark automated test harness tracking standard test matrices
└── webpilot/             # Internal agent implementation pack modules
    ├── __init__.py       # Package hook configurations exporting top-level controllers
    ├── agent.py          # The core rule-based state orchestrator driving simulated tool-use loops
    ├── browser.py        # Playwright automation layer tracking element actions
    ├── config.py         # Global runtime and viewport telemetry configurations
    └── tools.py          # Standard JSON-schema declarations for functional action boundaries

🔧 Installation & Verification
1. Clone & Install Dependencies
Ensure you have Python >= 3.11 ready. Install the project package locally in editable development mode along with terminal rendering libraries:

Bash
pip install -e .
2. Provision Local Browsers
Initialize the secure isolated underlying Webkit/Chromium binary drivers used by the browser tracking layers:

Bash
playwright install chromium
🎯 How to Use
🎮 The Interactive Sandbox CLI
Run the main terminal application to enter a conversational loop where you can specify custom parameters or execute standard shortcut tasks immediately:

Bash
python main.py
Visual Mode Prompt: The utility asks whether it should launch a visible browser instance (Show browser window? [Y/n]). Pass Y to track element clicks and inputs visually in real-time.

📊 Benchmark Automated Evaluation Suite
To launch continuous non-blocking tracking scripts verifying standard evaluation scenarios for hackathon grading metrics:

Bash
# Execute all 5 pre-configured automated benchmark scenarios sequentially (Headless Mode)
python demo.py --all

# Launch a highly specific scenario target task index (e.g., Scenario 2: News Aggregator) in Headed Mode
python demo.py --task 2
🏆 Hackathon Evaluator Reference Matrix
The internal routing engine is configured to execute five comprehensive production automation cases end-to-end:

🔍 Web Search & Summarise: Connects to Google, fires a dynamic search string, reads search headers, follows references, and isolates core bulleted summaries.

📰 News Aggregation: Crawls news.ycombinator.com, loops through primary interactive title containers, and maps individual story lines to vote scores.

🛒 E-commerce Research: Surfaces target product pages, inputs sorting criteria, and isolates optimal ratings alongside specific price limits.

📚 Knowledge Retrieval: Queries Wikipedia records to securely construct multi-fact index parameter points for deep data lookups.

✈️ Travel Price Research: Bridges typical form components, configures standard geographic parameters, and flags low-cost options.

👥 Authors & Team
Nishchal Soni

Kuldeep Parmar

Developed for the Microsoft Build AI Hackathon 2026. Built with speed, safety, and deterministic precision.
"""
