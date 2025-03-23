import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import logging

logging.basicConfig(level=logging.DEBUG)

st.title("AI-Powered Code Development Pipeline 🚀")
st.caption("Collaborate with AI agents to develop, test, and deploy Python code.")

# User input for feature request
feature_request = st.text_area("Enter your feature request:")
Google_api_key = st.sidebar.text_input("Enter GEMINI API Key", type="password")

if st.button("Generate Code"):
    if not Google_api_key:
        st.warning("Please enter the required API key.")
    else:
        with st.spinner("Processing your request..."):
            try:
                # Initialize GEMINI model
                model = Gemini(id="gemini-1.5-flash", api_key=Google_api_key)

                # Python Developer Agent
                developer_agent = Agent(
                    name="Python Developer",
                    role="Writes Python code based on user requirements",
                    model=model,
                    instructions=["Generate clean and well-documented Python code for the given task."],
                    markdown=True,
                )

                # Python Tester Agent
                tester_agent = Agent(
                    name="Python Tester",
                    role="Tests and debugs Python code",
                    model=model,
                    instructions=["Analyze the provided code, write test cases, and identify potential bugs."],
                    markdown=True,
                )

                # Production Team Agent
                production_agent = Agent(
                    name="Production Team",
                    role="Optimizes and prepares code for deployment",
                    model=model,
                    instructions=["Improve performance, fix issues, and make the code deployment-ready."],
                    markdown=True,
                )

                # Multi-agent workflow
                agent_team = Agent(
                    team=[developer_agent, tester_agent, production_agent],
                    instructions=[
                        "First, the Python Developer generates the required code.",
                        "Then, the Python Tester reviews the code, writes test cases, and finds bugs.",
                        "Finally, the Production Team optimizes and prepares the code for deployment.",
                        "Deliver a clean, tested, and optimized version of the final code in a report format."
                    ],
                    markdown=True,
                )

                # Step 1: Generate code
                dev_response = developer_agent.run(f"Write Python code for: {feature_request}")
                generated_code = dev_response.content
                
                # Step 2: Test the code
                test_response = tester_agent.run(f"Test the following Python code:\n{generated_code}")
                test_results = test_response.content
                
                # Step 3: Optimize for production
                prod_response = production_agent.run(f"Optimize and finalize the following Python code:\n{generated_code}\n\nTest Results:\n{test_results}")
                final_code = prod_response.content

                st.subheader("Final Optimized Code")
                st.code(final_code, language='python')
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Enter a feature request and API key, then click 'Generate Code' to start.")
