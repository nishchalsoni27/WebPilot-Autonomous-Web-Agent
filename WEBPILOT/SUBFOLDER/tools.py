"""
WebPilot Tool Definitions
Claude tool-use schemas for all browser actions the agent can perform.
"""

BROWSER_TOOLS = [
    {
        "name": "navigate",
        "description": (
            "Navigate the browser to a URL. Always include https://. "
            "Use for opening websites, search engines, or specific pages."
        ),
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
        "description": (
            "Get the current page's title, URL, visible text content, "
            "and list of interactive elements (buttons, links, inputs). "
            "Always call this after navigation to understand the page."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "click_element",
        "description": (
            "Click an element on the page. Provide its visible text or a CSS selector. "
            "Try different descriptions if one fails."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Visible text or label of the element to click",
                },
                "selector": {
                    "type": "string",
                    "description": "Optional CSS/XPath selector as fallback",
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "type_text",
        "description": (
            "Type text into a form field. Identify it by placeholder text, "
            "label, or CSS selector."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "Placeholder text, label, or CSS selector of the input",
                },
                "text": {"type": "string", "description": "Text to type"},
                "clear_first": {
                    "type": "boolean",
                    "description": "Clear the field before typing (default true)",
                },
            },
            "required": ["selector", "text"],
        },
    },
    {
        "name": "press_key",
        "description": "Press a keyboard key (e.g. Enter, Tab, Escape, ArrowDown).",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "Key name: Enter, Tab, Escape, ArrowDown, ArrowUp, etc.",
                }
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
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "top", "bottom"],
                    "description": "Scroll direction",
                },
                "amount": {
                    "type": "integer",
                    "description": "Pixels to scroll (default 300)",
                },
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
                "selector": {"type": "string", "description": "CSS selector for the <select> element"},
                "value": {"type": "string", "description": "The option text or value to select"},
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
                "milliseconds": {
                    "type": "integer",
                    "description": "Wait time in ms (default 2000, max 8000)",
                }
            },
        },
    },
    {
        "name": "screenshot",
        "description": "Capture a screenshot of the current page for visual inspection.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "task_complete",
        "description": (
            "Signal successful task completion. "
            "Provide a human-readable summary and the key result/data extracted."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "What was accomplished step-by-step",
                },
                "result": {
                    "type": "string",
                    "description": "The final answer, data, or outcome",
                },
            },
            "required": ["summary", "result"],
        },
    },
    {
        "name": "task_failed",
        "description": "Signal that the task cannot be completed after exhausting options.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Why the task failed"},
                "partial_result": {
                    "type": "string",
                    "description": "Any useful partial data gathered",
                },
            },
            "required": ["reason"],
        },
    },
]
