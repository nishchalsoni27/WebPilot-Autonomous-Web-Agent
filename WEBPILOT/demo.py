#!/usr/bin/env python3
"""
WebPilot Demo Script
Runs 5 showcase scenarios that highlight autonomous web agent capabilities.

Microsoft Build AI Hackathon 2026
Team: Nishchal Soni & Kuldeep Parmar

Usage:
    python demo.py              # interactive menu
    python demo.py --all        # run all demos (headless)
    python demo.py --task 2     # run demo #2 with browser visible
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from webpilot import WebPilotAgent

# ─── Demo catalogue ─────────────────────────────────────────────────────────
DEMOS = [
    {
        "id": 1,
        "name": "🔍  Web Search & Summarise",
        "task": (
            "Search for 'top AI breakthroughs 2026' on Google, open the first result, "
            "and summarise the 3 most important breakthroughs mentioned."
        ),
        "highlights": ["Google navigation", "Link following", "Content extraction"],
    },
    {
        "id": 2,
        "name": "📰  News Aggregation",
        "task": (
            "Go to https://news.ycombinator.com and list the top 5 story titles "
            "along with their point scores."
        ),
        "highlights": ["Direct navigation", "Structured data extraction"],
    },
    {
        "id": 3,
        "name": "🛒  E-commerce Research",
        "task": (
            "Go to https://www.flipkart.com, search for 'wireless headphones under 2000', "
            "and find the highest-rated product along with its price and rating."
        ),
        "highlights": ["E-commerce navigation", "Search", "Price/rating extraction"],
    },
    {
        "id": 4,
        "name": "📚  Knowledge Retrieval",
        "task": (
            "Go to Wikipedia and look up 'Large Language Model'. "
            "Extract: (1) the definition, (2) three notable examples, (3) the year the term was coined."
        ),
        "highlights": ["Wikipedia navigation", "Multi-fact extraction"],
    },
    {
        "id": 5,
        "name": "✈️  Travel Price Research",
        "task": (
            "Go to https://www.makemytrip.com, search for one-way flights from Delhi (DEL) "
            "to Mumbai (BOM) for the soonest available date, and report the cheapest fare found."
        ),
        "highlights": [
            "Multi-step form interaction",
            "Date selection",
            "Price comparison",
        ],
    },
]

# ─── Separator helper ────────────────────────────────────────────────────────
SEP = "─" * 64


def print_demo_header(demo: dict):
    print(f"\n{SEP}")
    print(f"  Demo {demo['id']}: {demo['name']}")
    print(f"  Task : {demo['task'][:120]}{'...' if len(demo['task']) > 120 else ''}")
    print(f"  Shows: {', '.join(demo['highlights'])}")
    print(SEP)


def print_result(result: dict, demo_name: str):
    print(f"\n{'─'*64}")
    if result["success"]:
        print(f"✅  {demo_name}  →  SUCCESS")
        print(f"Summary : {result.get('summary', 'N/A')}")
        print(f"Result  :\n{result.get('result', 'N/A')}")
        print(
            f"\nStats — Steps: {result.get('steps',0)} | "
            f"Actions: {result.get('actions',0)} | "
            f"Time: {result.get('elapsed_s',0)}s"
        )
    else:
        print(f"❌  {demo_name}  →  FAILED")
        print(f"Reason : {result.get('reason', 'Unknown')}")
        if result.get("partial_result"):
            print(f"Partial: {result['partial_result']}")
    print("─" * 64)


def save_result(result: dict, demo_id: int):
    out = Path("demo_outputs")
    out.mkdir(exist_ok=True)
    fpath = out / f"demo_{demo_id}_result.json"
    fpath.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  💾  Saved → {fpath}")


# ─── Single demo runner ──────────────────────────────────────────────────────
async def run_demo(demo: dict, headless: bool = False, save: bool = True) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set the ANTHROPIC_API_KEY environment variable.")
        sys.exit(1)

    print_demo_header(demo)
    agent = WebPilotAgent(api_key=api_key, headless=headless, max_steps=25)

    try:
        await agent.start()
        result = await agent.run_task(demo["task"])
    finally:
        await agent.stop()

    print_result(result, demo["name"])
    if save:
        save_result(result, demo["id"])
    return result


# ─── All demos runner ────────────────────────────────────────────────────────
async def run_all_demos(headless: bool = True):
    print("\n" + "=" * 64)
    print("  WebPilot — Full Demo Suite")
    print("  5 scenarios showcasing autonomous browsing capabilities")
    print("=" * 64)

    results = []
    t0 = time.time()

    for demo in DEMOS:
        result = await run_demo(demo, headless=headless, save=True)
        results.append((demo, result))

    # Summary table
    total = time.time() - t0
    print("\n" + "=" * 64)
    print(f"  SUMMARY  (total time: {total:.1f}s)")
    print("=" * 64)
    print(f"  {'#':<4} {'Demo':<30} {'Status':<12} {'Steps'}")
    print("  " + "─" * 56)
    for demo, res in results:
        status = "✅ Success" if res.get("success") else "❌ Failed"
        steps = str(res.get("steps", "—"))
        print(f"  {demo['id']:<4} {demo['name']:<30} {status:<12} {steps}")
    print("=" * 64)
    print("  Results saved in ./demo_outputs/")


# ─── CLI entry-point ─────────────────────────────────────────────────────────
def interactive_menu():
    print("\n" + "=" * 64)
    print("  WebPilot Demo — Select a Scenario")
    print("=" * 64)
    for d in DEMOS:
        print(f"  {d['id']}. {d['name']}")
    print(f"  {len(DEMOS)+1}. Run ALL demos (headless)")
    print("=" * 64)

    raw = input("Enter choice: ").strip()
    if not raw.isdigit():
        print("Invalid input.")
        return

    choice = int(raw)
    if choice == len(DEMOS) + 1:
        asyncio.run(run_all_demos(headless=True))
    elif 1 <= choice <= len(DEMOS):
        show = input("Show browser window? [Y/n]: ").strip().lower()
        headless = show.startswith("n")
        asyncio.run(run_demo(DEMOS[choice - 1], headless=headless))
    else:
        print("Invalid choice.")


def main():
    parser = argparse.ArgumentParser(description="WebPilot Demo Runner")
    parser.add_argument("--all", action="store_true", help="Run all demos headless")
    parser.add_argument("--task", type=int, choices=range(1, len(DEMOS) + 1),
                        help="Run a specific demo by number")
    parser.add_argument("--headless", action="store_true", help="Run without visible browser")
    args = parser.parse_args()

    if args.all:
        asyncio.run(run_all_demos(headless=True))
    elif args.task:
        demo = next(d for d in DEMOS if d["id"] == args.task)
        asyncio.run(run_demo(demo, headless=args.headless))
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
