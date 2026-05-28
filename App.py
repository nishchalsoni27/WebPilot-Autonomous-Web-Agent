import streamlit as st
import asyncio
import os
import sys
import subprocess
from pathlib import Path

# 1. Force Python path lookup adjustments
sys.path.insert(0, str(Path(__file__).parent))

# 2. Securely provision Playwright binaries inside Streamlit Cloud
@st.cache_resource
def ensure_playwright_browsers():
    try:
        # Check if chromium is already available
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Error initializing browser binaries: {e}")

ensure_playwright_browsers()

from webpilot import WebPilotAgent

# 3. Page Layout Configuration
st.set_page_config(page_title="WebPilot Dashboard", page_icon="🤖", layout="wide")

st.title("🤖 WebPilot Autonomous Browser Agent")
st.subheader("Microsoft Build AI Hackathon 2026 — Cloud Sandbox Workspace")
st.caption("Engineered by Nishchal Soni & Kuldeep Parmar")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🎛️ Settings Configuration")
    # Streamlit Cloud requires Headless mode (no visible window) to prevent crashing
    st.info("🌐 Running on Cloud Sandbox: Forced to Headless Mode.")
    
    st.markdown("### 🎯 Benchmark Scenarios")
    shortcuts = [
        "Search 'top AI breakthroughs 2026' on Google and summary metrics",
        "Go to https://news.ycombinator.com and extract top trending stories",
        "Search for 'Python 3.14 features' and list major adjustments"
    ]
    selected_shortcut = st.radio("Select a task shortcut:", shortcuts)

with col2:
    st.markdown("### 🚀 Launch Controls")
    custom_task = st.text_area("Refine your prompt objective:", value=selected_shortcut)
    
    status_box = st.empty()
    log_area = st.empty()

    if st.button("Execute Task Frame", type="primary"):
        log_content = []
        
        def ui_callback(label, detail):
            log_content.append(f"**[{label}]**: {detail}")
            log_area.markdown("\n".join(log_content))

        async def launch_agent_loop():
            # Cloud instances MUST run headless=True
            agent = WebPilotAgent(headless=True, on_step=ui_callback)
            await agent.start()
            try:
                res = await agent.run_task(custom_task)
                return res
            finally:
                await agent.stop()

        status_box.info("Initializing Playwright system layers dynamically...")
        
        # Safe async loop handling for Streamlit environments
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If an event loop is already running, schedule the task within it
            future = asyncio.run_coroutine_threadsafe(launch_agent_loop(), loop)
            output = future.result()
        else:
            output = asyncio.run(launch_agent_loop())
        
        status_box.success("Execution Complete!")
        st.balloons()
        
        st.markdown("### 📊 Extracted Target Payload Summary")
        st.success(f"**Summary:** {output['summary']}")
        st.code(output['result'], language="markdown")
