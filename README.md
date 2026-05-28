# 🚀 WebPilot: Autonomous Local-First Web Agent
### Microsoft Build AI Hackathon 2026 | Team Project

[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://python.org)
[![Automation Core](https://img.shields.io/badge/Engine-Playwright-orange.svg)](https://playwright.dev)
[![Interface](https://img.shields.io/badge/CLI-Rich-green.svg)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Executive Summary

**WebPilot** is an advanced, lightweight autonomous browser automation agent engineered for the **Microsoft Build AI Hackathon 2026**. Designed by **Nishchal Soni & Kuldeep Parmar**, the framework shifts away from volatile, cost-heavy remote LLM endpoint dependencies, introducing a fully self-contained, **Local Deterministic State Orchestrator**. 

By mirroring the programmatic tool-use loop configurations of cutting-edge frontier models entirely on-device, WebPilot safely decodes complex natural-language objectives into high-precision, sequential browser interactions across live target domains—yielding zero latency, zero API token costs, and rock-solid architectural predictability.

---

## 🛠️ Deep-Dive Architectural Blueprint


```

```text
webpilot/
├── .env                  # Project environment configuration stub
├── requirements.txt      # Production runtime package manifests
├── setup.py              # Structural distribution install packaging
├── main.py               # Production Interactive CLI Terminal core gateway
├── demo.py               # Benchmark automated test-harness evaluation matrix
└── webpilot/             # Consolidated core package bundle
    ├── __init__.py       # Exposes the main top-level operational classes
    ├── agent.py          # Local Rule Engine & simulated Tool-Use orchestrator
    ├── browser.py        # Resilient multi-strategy Playwright abstraction engine
    ├── config.py         # Global runtime variables, parameters, & telemetry 
    └── tools.py          # Declarative JSON schemas enforcing functional boundaries

```

### 🧩 Core Component Subsystems

1. **`agent.py` (The State Brain):** Captures intent via a rule-based parser matrix, transitioning states dynamically. It wraps sequential operations into structured simulated LLM `tool_use` JSON blocks, verifying runtime execution block-by-block.
2. **`browser.py` (The Automation Muscle):** Abstracts Playwright's asynchronous API. Implements a multi-layered fallback strategy for clicking and input injection (CSS Selectors $\rightarrow$ Exact Text $\rightarrow$ Partial Match), safely hiding webdriver telemetry profiles.
3. **`tools.py` (The System Interfaces):** Maintains functional strictness by modeling atomic browser boundaries (`Maps`, `type_text`, `click_element`, `scroll`, `screenshot`) with unified input parameter contracts.

---

## ⚡ Technical Installation

### 1. Repository Setup & Dependencies

Provision a secure virtual python environment (`>= 3.11`) and perform an editable development installation to link local system binaries:

```bash
# Clone the codebase and execute an internal editable installation
pip install -e .

```

### 2. Browser Sandbox Drivers Provisioning

Initialize Playwright's specialized sandboxed Chromium engine binaries directly from your package architecture layout:

```bash
playwright install chromium

```

---

## 🚀 Execution & Operational Modes

### 🎮 Mode A: The Interactive Terminal Sandbox

Engage WebPilot through a terminal interface wrapped with diagnostic telemetry dashboards.

```bash
python main.py

```

* **Visual Telemetry Toggling:** The application prompts `Show browser window? [Y/n]`. Toggle `Y` to spawn a headed browser frame, enabling you to inspect programmatic selectors and inputs live in real-time.

### 📊 Mode B: Automated Multi-Scenario Benchmark Suite

For rapid testing, evaluation, or grading configurations, execute the fully non-blocking test-harness subsystem.

```bash
# Execute all 5 automated hackathon scenarios sequentially (Headless Mode)
python demo.py --all

# Isolate and run an explicit scenario target by index number in Headed Mode
python demo.py --task 2 --headless

```

---

## 🏆 Production Scenario Matrix Evaluator

WebPilot features optimized internal deterministic routing behaviors mapped explicitly to complete 5 high-profile real-world workloads:

| ID | Benchmark Scenario | Automated Target Sequence Workflow |
| --- | --- | --- |
| **01** | **🔍 Web Search & Summarize** | Maps terms directly to Google layouts, bypasses popups, tracks high-relevance headers, and computes deep structural summaries. |
| **02** | **📰 News Aggregation** | Connects to `news.ycombinator.com`, loops active title elements into index arrays, and accurately binds points matrices. |
| **03** | **🛒 E-commerce Research** | Commands retail search terminals (e.g., Flipkart), applies string sorting criteria, and isolates low-price, high-rating equipment options. |
| **04** | **📚 Knowledge Retrieval** | Interfaces with Wikipedia endpoints, scraping structural definition nodes and organizing multiple key facts instantly. |
| **05** | **✈️ Travel Price Research** | Simulates modern airline booking forms, bypassing heavy DOM trees to report low-cost routes across distinct hubs. |

---

## 🛡️ Operational Guardrails & Design Paradigms

* **Security First:** The automation layers enforce a strict non-submission boundary policy. WebPilot will seamlessly crawl items and map e-commerce pipelines right up to checkout fields, but **never** submits sensitive personal identities, credit credentials, or final transactional confirmations.
* **Anti-Fragility Layer:** If target site layouts change unexpectedly, the `BrowserController` triggers an elegant programmatic fallback strategy, ensuring loops conclude cleanly rather than causing execution script crashes.

---

## 👥 Authors & Core Team

* **Nishchal Soni** — *AI Core Developer*
* **Kuldeep Parmar** — *Automation Systems Architect*



