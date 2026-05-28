"""
WebPilot Configuration
All tuneable parameters in one place.
"""

from dataclasses import dataclass, field


@dataclass
class WebPilotConfig:
    # ── Mock Engine ──────────────────────────────────────────────────────────
    model: str = "local-deterministic-mock"

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
        # Always valid now since we don't require an external API key
        return self


# Singleton default config
DEFAULT_CONFIG = WebPilotConfig()