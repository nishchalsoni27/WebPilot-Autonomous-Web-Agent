"""
WebPilot — Interactive CLI
Microsoft Build AI Hackathon 2026
Team: Nishchal Soni & Kuldeep Parmar
"""

import asyncio
import json
import os
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

sys.path.insert(0, str(Path(__file__).parent))
from webpilot import WebPilotAgent

BANNER = r"""
 __        __   _     ____  _ _       _
 \ \      / /__| |__ |  _ \(_) | ___ | |_
  \ \ /\ / / _ \ '_ \| |_) | | |/ _ \| __|
   \ V  V /  __/ |_) |  __/| | | (_) | |_
    \_/\_/ \___|_.__/|_|   |_|_|\___/ \__|

  Autonomous Web Agent — Microsoft Build AI 2026
  Team: Nishchal Soni & Kuldeep Parmar (Local Sandbox Mode)
"""

SAMPLE_TASKS = [
    "Search 'best AI frameworks 2026' on Google and summarise the top 3 results",
    "Go to Wikipedia and get the key facts about Artificial General Intelligence",
    "Find the top 3 trending GitHub repositories today",
    "Search for 'Python 3.13 features' and list the major new features",
    "Go to news.ycombinator.com and list the top 5 stories right now",
    "Find the current USD to INR exchange rate",
    "Search for 'laptop under 50000 India 2026' and find the best-rated option",
    "Go to python.org and find the latest stable Python release version",
]


def _print(text: str, style: str = ""):
    if HAS_RICH:
        console.print(text, style=style or "default")
    else:
        print(text)


def _prompt(msg: str) -> str:
    if HAS_RICH:
        return Prompt.ask(msg)
    else:
        return input(msg + ": ")


def _confirm(msg: str, default: bool = True) -> bool:
    if HAS_RICH:
        return Confirm.ask(msg, default=default)
    ans = input(f"{msg} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    if not ans:
        return default
    return ans.startswith("y")


def print_banner():
    if HAS_RICH:
        console.print(Panel(BANNER, style="bold cyan"))
    else:
        print(BANNER)


def print_result(result: dict):
    if result["success"]:
        msg = (
            f"✅  Task Completed\n\n"
            f"Summary : {result.get('summary', 'N/A')}\n\n"
            f"Result  : {result.get('result', 'N/A')}\n\n"
            f"Steps: {result.get('steps', 0)}  |  "
            f"Actions: {result.get('actions', 0)}  |  "
            f"Time: {result.get('elapsed_s', 0)}s"
        )
        if HAS_RICH:
            console.print(Panel(msg, title="[bold green]Success[/bold green]", style="green"))
        else:
            print("\n" + "=" * 60)
            print(msg)
            print("=" * 60)
    else:
        msg = (
            f"❌  Task Failed\n\n"
            f"Reason : {result.get('reason', 'Unknown')}\n"
        )
        if HAS_RICH:
            console.print(Panel(msg, title="[bold red]Failed[/bold red]", style="red"))
        else:
            print("\n" + "=" * 60)
            print(msg)
            print("=" * 60)


async def interactive_loop():
    print_banner()
    headless = not _confirm("Show browser window?", default=True)

    _print("\n⚙️  Starting WebPilot Local Sandbox Core...", "yellow")
    agent = WebPilotAgent(headless=headless)

    try:
        await agent.start()
        _print("✅  Agent Ready (No Token Required)!\n", "green")

        while True:
            _print("\n[bold cyan]Sample Tasks:[/bold cyan]" if HAS_RICH else "\nSample Tasks:")
            if HAS_RICH:
                tbl = Table(show_header=False, box=None, padding=(0, 1))
                for i, t in enumerate(SAMPLE_TASKS, 1):
                    tbl.add_row(f"[dim]{i}[/dim]", t)
                console.print(tbl)
            else:
                for i, t in enumerate(SAMPLE_TASKS, 1):
                    print(f"  {i}. {t}")

            _print("\nEnter a number, type your own task, or 'quit' to exit.")
            raw = _prompt("\n🎯 Task").strip()

            if raw.lower() in ("quit", "exit", "q", ""):
                break

            task = raw
            if raw.isdigit():
                idx = int(raw) - 1
                if 0 <= idx < len(SAMPLE_TASKS):
                    task = SAMPLE_TASKS[idx]
                    _print(f"[dim]Using: {task}[/dim]" if HAS_RICH else f"Using: {task}")

            _print(f"\n🚀 Running: {task}", "yellow")
            print("-" * 60)

            try:
                result = await agent.run_task(task)
                print_result(result)

                if _confirm("\nSave result to JSON?", default=False):
                    fname = f"result_{int(asyncio.get_event_loop().time())}.json"
                    Path(fname).write_text(json.dumps(result, indent=2))
                    _print(f"Saved → {fname}", "dim")

            except Exception as exc:
                _print(f"\n[red]Error: {exc}[/red]" if HAS_RICH else f"\nError: {exc}")

            if not _confirm("\nRun another task?", default=True):
                break

    finally:
        await agent.stop()
        _print("\n👋 WebPilot stopped gracefully.", "yellow")


def main():
    asyncio.run(interactive_loop())


if __name__ == "__main__":
    main()
