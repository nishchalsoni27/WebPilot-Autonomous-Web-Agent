# app.py
import streamlit as st
import asyncio
from webpilot import WebPilotAgent

st.title("🤖 WebPilot Autonomous Agent")
st.caption("Microsoft Build AI Hackathon 2026 — Local Sandbox Mode")

# User input text box
task = st.text_input("Enter your automation task:", "Go to news.ycombinator.com and list top stories")

if st.button("Launch Agent"):
    if task:
        with st.spinner("Agent is executing browser steps locally..."):
            # Define an inner async function to run the agent loop
            async def run_agent():
                async with WebPilotAgent(headless=True) as agent:
                    return await agent.run_task(task)
            
            # Execute the async loop inside Streamlit
            result = asyncio.run(run_agent())
            
            # Display the outcomes on the webpage
            if result["success"]:
                st.success("Task Completed Successfully!")
                st.subheader("Summary")
                st.write(result["summary"])
                st.subheader("Extracted Data")
                st.code(result["result"])
            else:
                st.error(f"Task Failed: {result.get('reason', 'Unknown error')}")