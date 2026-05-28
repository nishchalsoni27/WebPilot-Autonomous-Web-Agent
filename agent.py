"""
WebPilot Agent — Core Orchestrator
Autonomous web agent powered by Claude tool-use loop.

Microsoft Build AI Hackathon 2026
Team: Nishchal Soni & Kuldeep Parmar
"""

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import anthropic

from .browser import BrowserController
from .tools import BROWSER_TOOLS

# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are WebPilot, an expert autonomous web agent. Your mission is to
complete real-world web tasks end-to-end — no human in the loop.

━━━  OPERATING PRINCIPLES  ━━━

1. PLAN FIRST  – Before touching the browser, think: which site, which steps, what
   to look for.  Spell out sub-goals if the task is multi-step.

2. OBSERVE → ACT → VERIFY  – After every navigation or click call get_page_content
   to confirm where you are and what changed.

3. RESILIENCE  – If a selector or text doesn't match, try:
     • A different description or CSS selector
     • Scrolling to reveal the element
     • Searching via Google/Bing as a fallback entry-point
     • Waiting a moment with wait() then retrying

4. END-TO-END  – Don't stop at the search results page. Drill into results, extract
   the real data, and assemble the complete answer.

5. SAFETY  – Never submit personal/payment information.  For e-commerce tasks,
   reach the checkout page but DO NOT confirm/place the order.

━━━  SEARCH STRATEGY  ━━━
• For any factual lookup: navigate to https://www.google.com → type query → press
  Enter → get_page_content → click the most relevant result → extract data.
• For site-specific tasks (Amazon, Flipkart, MakeMyTrip, etc.): navigate directly
  to the site, then use its search box.

━━━  COMPLETION  ━━━
Call task_complete once the goal is fully achieved.
Call task_failed only after genuinely exhausting alternatives."""
# ─────────────────────────────────────────────────────────────────────────────


class WebPilotAgent:
    """Agentic loop: Claude decides actions → browser executes → loop continues."""

    def __init__(
        self,
        api_key: str = None,
        headless: bool = False,
        max_steps: int = 30,
        model: str = "claude-opus-4-5",
        on_step: Optional[Callable[[str, str], None]] = None,
    ):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.browser = BrowserController(headless=headless)
        self.max_steps = max_steps
        self.model = model
        self.on_step = on_step  # optional callback(step_label, detail)

        # Session state
        self.conversation: List[Dict] = []
        self.action_log: List[Dict] = []
        self.start_time: Optional[float] = None

    # ─────────────────────────── Lifecycle ───────────────────────────

    async def start(self):
        await self.browser.start()

    async def stop(self):
        await self.browser.close()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *_):
        await self.stop()

    # ──────────────────────────── Core Loop ──────────────────────────

    async def run_task(self, task: str) -> Dict[str, Any]:
        """Execute a natural-language task and return a result dict."""
        self.conversation = []
        self.action_log = []
        self.start_time = time.time()

        self._emit("🎯 Task started", task)

        self.conversation.append(
            {
                "role": "user",
                "content": (
                    f"Complete this task autonomously: {task}\n\n"
                    "Think through your plan, then execute it step by step using the tools."
                ),
            }
        )

        final: Dict[str, Any] = {"success": False, "task": task}

        for step in range(1, self.max_steps + 1):
            self._emit(f"Step {step}", "Calling Claude…")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=BROWSER_TOOLS,
                messages=self.conversation,
            )

            tool_results, done = [], False

            for block in response.content:
                if block.type == "text" and block.text.strip():
                    self._emit(f"Step {step} 💭", block.text[:300])

                elif block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    self._emit(f"Step {step} 🔧", f"{tool_name}({json.dumps(tool_input)[:120]})")

                    if tool_name == "task_complete":
                        final = {
                            "success": True,
                            "task": task,
                            "summary": tool_input.get("summary", ""),
                            "result": tool_input.get("result", ""),
                            "steps": step,
                            "actions": len(self.action_log),
                            "elapsed_s": round(time.time() - self.start_time, 1),
                        }
                        done = True
                        tool_results.append(
                            {"type": "tool_result", "tool_use_id": block.id,
                             "content": '{"acknowledged": true}'}
                        )
                        self._emit("✅ Complete", final["summary"])
                        break

                    if tool_name == "task_failed":
                        final = {
                            "success": False,
                            "task": task,
                            "reason": tool_input.get("reason", ""),
                            "partial_result": tool_input.get("partial_result", ""),
                            "steps": step,
                            "elapsed_s": round(time.time() - self.start_time, 1),
                        }
                        done = True
                        tool_results.append(
                            {"type": "tool_result", "tool_use_id": block.id,
                             "content": '{"acknowledged": true}'}
                        )
                        self._emit("❌ Failed", final["reason"])
                        break

                    result_str = await self._execute(tool_name, tool_input)
                    self._emit(f"   ↳ result", result_str[:150])
                    tool_results.append(
                        {"type": "tool_result", "tool_use_id": block.id, "content": result_str}
                    )

            # Append assistant turn
            self.conversation.append({"role": "assistant", "content": response.content})

            if done:
                break

            if tool_results:
                self.conversation.append({"role": "user", "content": tool_results})

            if response.stop_reason == "end_turn":
                self._emit("⚠️ Warning", "Claude stopped without calling task_complete")
                break

        if not final.get("success") and "steps" not in final:
            final["reason"] = f"Max steps ({self.max_steps}) reached"
            final["steps"] = self.max_steps
            final["elapsed_s"] = round(time.time() - self.start_time, 1)

        return final

    # ─────────────────────────── Tool Dispatch ───────────────────────

    async def _execute(self, name: str, inp: Dict) -> str:
        b = self.browser
        result = None

        dispatch = {
            "navigate":        lambda: b.navigate(inp["url"]),
            "get_page_content":lambda: b.get_page_content(),
            "click_element":   lambda: b.click_element(inp["description"], inp.get("selector")),
            "type_text":       lambda: b.type_text(inp["selector"], inp["text"], inp.get("clear_first", True)),
            "press_key":       lambda: b.press_key(inp["key"]),
            "scroll":          lambda: b.scroll(inp.get("direction", "down"), inp.get("amount", 300)),
            "go_back":         lambda: b.go_back(),
            "select_option":   lambda: b.select_option(inp["selector"], inp["value"]),
            "wait":            lambda: b.wait(min(inp.get("milliseconds", 2000), 8000)),
            "screenshot":      lambda: b.screenshot(),
        }

        fn = dispatch.get(name)
        if fn:
            result = await fn()
        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        # Log action
        self.action_log.append({"step": len(self.action_log) + 1, "tool": name, "input": inp, "result": result})

        # Strip screenshot bytes from returned string to keep history lean
        if name == "screenshot" and result.get("success"):
            return json.dumps({"success": True, "message": "Screenshot captured"})

        return json.dumps(result)

    # ─────────────────────────── Helpers ─────────────────────────────

    def _emit(self, label: str, detail: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {label}: {detail}")
        if self.on_step:
            self.on_step(label, detail)
