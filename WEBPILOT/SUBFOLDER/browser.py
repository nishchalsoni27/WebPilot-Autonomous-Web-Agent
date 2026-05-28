"""
WebPilot Browser Controller
Playwright-based browser automation with resilient element interaction
"""

import asyncio
import base64
import json
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


class BrowserController:
    """Headless/headed browser controller wrapping Playwright."""

    def __init__(self, headless: bool = False, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    # ──────────────────────────── Lifecycle ────────────────────────────

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
        )
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        self.page = await self.context.new_page()
        # Hide webdriver flag
        await self.page.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    # ─────────────────────────── Navigation ────────────────────────────

    async def navigate(self, url: str) -> Dict[str, Any]:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            await self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout)
            await self.page.wait_for_timeout(1500)
            return {"success": True, "url": self.page.url, "title": await self.page.title()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def go_back(self) -> Dict[str, Any]:
        try:
            await self.page.go_back(timeout=10000)
            await self.page.wait_for_timeout(1200)
            return {"success": True, "url": self.page.url}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ─────────────────────────── Page Reading ──────────────────────────

    async def get_page_content(self) -> Dict[str, Any]:
        try:
            title = await self.page.title()
            url = self.page.url

            # Truncated visible text
            content = await self.page.evaluate("""
                () => {
                    document.querySelectorAll('script,style,noscript,svg').forEach(e => e.remove());
                    return (document.body ? document.body.innerText : '').substring(0, 6000);
                }
            """)

            # Interactive elements inventory
            elements = await self.page.evaluate("""
                () => {
                    const els = [];
                    document.querySelectorAll(
                        'a,button,input,select,textarea,[role="button"],[role="link"],[role="tab"]'
                    ).forEach((el, i) => {
                        const r = el.getBoundingClientRect();
                        if (r.width > 0 && r.height > 0) {
                            els.push({
                                index: i,
                                tag: el.tagName.toLowerCase(),
                                text: (el.textContent || el.value || el.placeholder || '')
                                        .trim().substring(0, 120),
                                type: el.type || '',
                                href: el.href || '',
                                id: el.id || '',
                                name: el.name || '',
                                placeholder: el.placeholder || ''
                            });
                        }
                    });
                    return els.slice(0, 60);
                }
            """)

            return {
                "success": True,
                "title": title,
                "url": url,
                "content": content,
                "interactive_elements": elements,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def screenshot(self) -> Dict[str, Any]:
        try:
            data = await self.page.screenshot(type="png", full_page=False)
            return {"success": True, "screenshot_b64": base64.b64encode(data).decode()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ─────────────────────────── Interaction ───────────────────────────

    async def click_element(
        self, description: str, selector: str = None
    ) -> Dict[str, Any]:
        """Multi-strategy click: CSS selector → exact text → partial text → role."""
        strategies = []

        if selector:
            strategies.append(("css_selector", lambda: self.page.click(selector, timeout=5000)))

        strategies += [
            ("exact_text",   lambda: self.page.click(f"text={description}", timeout=4000)),
            ("partial_text", lambda: self.page.locator(f"text={description}").first.click(timeout=4000)),
            ("get_by_text",  lambda: self.page.get_by_text(description, exact=False).first.click(timeout=4000)),
            ("role_button",  lambda: self.page.get_by_role("button", name=description).first.click(timeout=4000)),
            ("role_link",    lambda: self.page.get_by_role("link",   name=description).first.click(timeout=4000)),
        ]

        for name, action in strategies:
            try:
                await action()
                await self.page.wait_for_timeout(1000)
                return {"success": True, "method": name}
            except Exception:
                continue

        return {"success": False, "error": f"Could not find clickable element: '{description}'"}

    async def type_text(
        self, selector: str, text: str, clear_first: bool = True
    ) -> Dict[str, Any]:
        """Type text via CSS selector, placeholder, or label."""
        finders = [
            lambda: self.page.locator(selector).first,
            lambda: self.page.get_by_placeholder(selector).first,
            lambda: self.page.get_by_label(selector).first,
        ]

        for finder in finders:
            try:
                el = finder()
                await el.wait_for(timeout=4000)
                if clear_first:
                    await el.clear()
                await el.type(text, delay=40)
                await self.page.wait_for_timeout(400)
                return {"success": True}
            except Exception:
                continue

        return {"success": False, "error": f"Could not find input field: '{selector}'"}

    async def scroll(
        self, direction: str = "down", amount: int = 300
    ) -> Dict[str, Any]:
        move = {
            "down":   f"window.scrollBy(0,{amount})",
            "up":     f"window.scrollBy(0,-{amount})",
            "top":    "window.scrollTo(0,0)",
            "bottom": "window.scrollTo(0,document.body.scrollHeight)",
        }.get(direction)

        if not move:
            return {"success": False, "error": f"Unknown direction: {direction}"}

        try:
            await self.page.evaluate(move)
            await self.page.wait_for_timeout(400)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def press_key(self, key: str) -> Dict[str, Any]:
        try:
            await self.page.keyboard.press(key)
            await self.page.wait_for_timeout(500)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def select_option(self, selector: str, value: str) -> Dict[str, Any]:
        try:
            await self.page.select_option(selector, label=value, timeout=5000)
            return {"success": True}
        except Exception:
            try:
                await self.page.select_option(selector, value=value, timeout=5000)
                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def wait(self, milliseconds: int = 2000) -> Dict[str, Any]:
        await self.page.wait_for_timeout(milliseconds)
        return {"success": True, "waited_ms": milliseconds}
