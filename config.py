"""
WebPilot Configuration
All tuneable parameters in one place.
"""

import os
from dataclasses import dataclass, field


@dataclass
class WebPilotConfig:
    # ── API ──────────────────────────────────────────────────────────────────
    anthropic_api_key: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", "")
    )
    model: str = "claude-opus-4-5"
    max_tokens: int = 4096

    # ── Browser ──────────────────────────────────────────────────────────────
    headless: bool = False
    browser_type: str = "chromium"      # chromium | firefox | webkit
    viewport_width: int = 1280
    viewport_height: int = 720
    page_timeout_ms: int = 30_000

    # ── Agent ────────────────────────────────────────────────────────────────
    max_steps: int = 30
    retry_attempts: int = 3

    # ── Output ───────────────────────────────────────────────────────────────
    log_actions: bool = True
    output_dir: str = "webpilot_output"

    def validate(self) -> "WebPilotConfig":
        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. "
                "Export it or pass it to WebPilotAgent(api_key=...)."
            )
        return self


# Singleton default config
DEFAULT_CONFIG = WebPilotConfig()
