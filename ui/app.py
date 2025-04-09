import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from debate.simulation import simulate_multi_round_debate

st.set_page_config(page_title="Multi-Agent AI Debate System", layout="wide")
st.title("Multi-Agent AI Debate System")
st.write(
    "Enter a debate topic below, choose the number of rounds, and watch the debate unfold with scoring and evaluation!"
)

# Input for the debate topic.
debate_topic = st.text_input(
    "Debate Topic", value="Artificial intelligence should be regulated."
)

# Slider to choose the number of rounds.
num_rounds = st.slider("Number of Rounds", min_value=1, max_value=5, value=3, step=1)

if st.button("Start Debate"):
    if not debate_topic:
        st.error("Please provide a debate topic.")
    else:
        with st.spinner("Generating multi-round debate..."):
            debate_states = simulate_multi_round_debate(
                debate_topic, num_rounds=num_rounds
            )

        st.subheader("Debate Transcript")

        st.write("### Debater A (Pro)'s Arguments:")
        for idx, arg in enumerate(debate_states["debater_a"].argument_history, start=1):
            st.markdown(f"**Round {idx}:** {arg}")
        st.markdown(
            f"**Final Score for Debater A:** {debate_states['debater_a'].score}"
        )

        st.write("### Debater B (Con)'s Arguments:")
        for idx, arg in enumerate(debate_states["debater_b"].argument_history, start=1):
            st.markdown(f"**Round {idx}:** {arg}")
        st.markdown(
            f"**Final Score for Debater B:** {debate_states['debater_b'].score}"
        )

        st.subheader("Moderator State")
        st.json(debate_states["moderator"].model_dump())
