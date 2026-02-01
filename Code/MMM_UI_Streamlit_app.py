# -------------------------------------------------------
# Import required libraries
# -------------------------------------------------------

import streamlit as st

# Import chatbot logic functions
# chatbot_response → handles intent + MMM logic
# call_gemini → converts MMM insights into business language
from Chatbot_Analysis import chatbot_response, call_gemini


# -------------------------------------------------------
# Page configuration
# -------------------------------------------------------

# Sets the page title and layout of the Streamlit app
st.set_page_config(
    page_title="GenAI Powered MMM Assistant",
    layout="centered"
)


# -------------------------------------------------------
# App title and description
# -------------------------------------------------------

# Main title displayed at the top of the app
st.title("📊 GenAI-Powered Marketing Mix Modeling Assistant")

# Short description below the title
st.caption(
    "Ask business questions about marketing performance, channel efficiency, and budget scenarios"
)


# -------------------------------------------------------
# User input section (Streamlit 1.12 compatible)
# -------------------------------------------------------

# Text input box for user to type their question
# (chat_input is NOT supported in Streamlit 1.12)
user_query = st.text_input("Ask a question:")


# -------------------------------------------------------
# Submit button logic
# -------------------------------------------------------

# Button triggers the analysis when clicked
if st.button("Submit Query"):

    # Validate empty input
    if user_query.strip() == "":
        st.warning("Please enter a question to continue.")

    else:
        # ---------------------------------------------------
        # Step 1: Pass user query to chatbot controller
        # ---------------------------------------------------
        # This function:
        # - Detects user intent (summary / ranking / what-if / channel detail)
        # - Executes MMM logic
        # - Builds a Gemini-ready prompt
        prompt = chatbot_response(user_query)

        # ---------------------------------------------------
        # Step 2: Send prompt to Gemini
        # ---------------------------------------------------
        # Gemini converts structured MMM output into
        # easy-to-understand business language
        answer = call_gemini(prompt)

        # ---------------------------------------------------
        # Step 3: Display the response
        # ---------------------------------------------------
        st.subheader("📌 Business Insight")
        st.write(answer)
