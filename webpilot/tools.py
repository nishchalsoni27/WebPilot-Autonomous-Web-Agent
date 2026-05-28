"""
WebPilot Tool Definitionstool-use schemas for all browser actions the agent can perform.
"""

BROWSER_TOOLS = [
    {
        "name": "navigate",
        "description": "Navigate the browser to a URL. Always include https://.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Full URL including https://"}
            },
            "required": ["url"],
        },
    },
    {
        "name": "get_page_content",
        "description": "Get the current page's title, URL, visible text content, and interactive elements.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "click_element",
        "description": "Click an element on the page. Provide its visible text or a CSS selector.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Visible text or label"},
                "selector": {"type": "string", "description": "Optional CSS selector"},
            },
            "required": ["description"],
        },
    },
    {
        "name": "type_text",
        "description": "Type text into a form field.",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string", "description": "Placeholder, label, or CSS selector"},
                "text": {"type": "string", "description": "Text to type"},
                "clear_first": {"type": "boolean", "description": "Clear field before typing"},
            },
            "required": ["selector", "text"],
        },
    },
    {
        "name": "press_key",
        "description": "Press a keyboard key (e.g. Enter, Tab, Escape).",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "Key name"}
            },
            "required": ["key"],
        },
    },
    {
        "name": "scroll",
        "description": "Scroll the page to reveal more content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "enum": ["up", "down", "top", "bottom"]},
                "amount": {"type": "integer"},
            },
        },
    },
    {
        "name": "go_back",
        "description": "Go back to the previous page in browser history.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "select_option",
        "description": "Select an option from a <select> dropdown.",
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["selector", "value"],
        },
    },
    {
        "name": "wait",
        "description": "Wait for a page to load or animation to complete.",
        "input_schema": {
            "type": "object",
            "properties": {
                "milliseconds": {"type": "integer"}
            },
        },
    },
    {
        "name": "screenshot",
        "description": "Capture a screenshot of the current page.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "task_complete",
        "description": "Signal successful task completion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "result": {"type": "string"},
            },
            "required": ["summary", "result"],
        },
    },
    {
        "name": "task_failed",
        "description": "Signal that the task cannot be completed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"},
                "partial_result": {"type": "string"},
            },
            "required": ["reason"],
        },
    },
]