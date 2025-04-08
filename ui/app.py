import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from debate.simulation import simulate_debate

st.set_page_config(page_title="Multi-Agent AI Debate System", layout="wide")
st.title("Multi-Agent AI Debate System")
st.write(
    "Enter a debate topic below and watch the debate unfold between two AI agents!"
)

# Input for debate topic.
debate_topic = st.text_input(
    "Debate Topic", value="Artificial intelligence should be regulated."
)

# Start Debate button.
if st.button("Start Debate"):
    if not debate_topic:
        st.error("Please provide a debate topic.")
    else:
        with st.spinner("Generating debate..."):
            debate_states = simulate_debate(debate_topic)

        # Display Debater A's and Debater B's opening arguments.
        st.subheader("Debater A (Pro)'s Opening Argument:")
        st.write(debate_states["debater_a"].current_argument)
        st.subheader("Debater B (Con)'s Opening Argument:")
        st.write(debate_states["debater_b"].current_argument)

        # Optionally, display the full internal state of each agent (for debugging or analysis).
        st.subheader("Debater A State:")
        st.json(debate_states["debater_a"].model_dump())
        st.subheader("Debater B State:")
        st.json(debate_states["debater_b"].model_dump())
        st.subheader("Moderator State:")
        st.json(debate_states["moderator"].model_dump())
