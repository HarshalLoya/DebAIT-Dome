# ui/app.py

import os
import sys
import time

import streamlit as st

st.set_page_config(page_title="AI Debate Arena", layout="wide")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from debate.simulation import stream_multi_round_debate

css_file = os.path.join(os.path.dirname(__file__), "style.css")
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_score_widget(score_a, score_b):
    """
    Returns HTML for the fixed score board in the top-right corner.
    """
    return f"""
    <div style="position: fixed; top: 10px; right: 10px; background-color: #f0f0f0;
         padding: 10px; border-radius: 5px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
         <h4 style="margin: 0 0 5px 0;">Scores</h4>
         <div>Debater A: {score_a:.1f}</div>
         <div>Debater B: {score_b:.1f}</div>
    </div>
    """


st.title("AI Debate Arena")
st.write(
    "Watch two AI agents engage in a real-time debate with dynamic arguments and scoring."
)

st.sidebar.header("Debate Parameters")
debate_topic = st.sidebar.text_input(
    "Debate Topic", value="Artificial intelligence should be regulated."
)
num_rounds = st.sidebar.slider(
    "Number of Rounds", min_value=1, max_value=5, value=3, step=1
)
tone = st.sidebar.selectbox(
    "Tone", options=["Formal", "Informal", "Academic", "Casual"], index=0
)
max_response_length = st.sidebar.slider(
    "Max Sentences per Response", min_value=3, max_value=10, value=6, step=1
)

scoreboard_placeholder = st.empty()

last_round = 0

if st.sidebar.button("Start Debate", use_container_width=True):
    if not debate_topic.strip():
        st.error("Please provide a debate topic.")
    else:
        final_score_a = 0.0
        final_score_b = 0.0

        debate_stream = stream_multi_round_debate(
            debate_topic,
            num_rounds=num_rounds,
            tone=tone,
            max_sentences=max_response_length,
        )

        try:
            for msg in debate_stream:
                round_num = msg["round"]

                if round_num != last_round:
                    st.markdown(
                        f"<div class='round-header'>Round {round_num}</div>",
                        unsafe_allow_html=True,
                    )
                    last_round = round_num

                if msg["debater"] == "Debater A":
                    css_class = "pro"
                    badge_html = "<span class='badge pro-badge'>PRO</span>"
                    final_score_a = msg["score"]
                else:
                    css_class = "con"
                    badge_html = "<span class='badge con-badge'>CON</span>"
                    final_score_b = msg["score"]

                message_placeholder = st.empty()

                words = msg["text"].split()
                display_text = ""
                chunk_size = 3
                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i : i + chunk_size])
                    display_text += chunk + " "
                    rendered_message = (
                        f"<div class='{css_class}'>"
                        f"<b>{msg['debater']}</b> {badge_html} "
                        f"<small>{msg['timestamp']}</small><br>{display_text}"
                        f"</div>"
                    )
                    message_placeholder.markdown(
                        rendered_message, unsafe_allow_html=True
                    )
                    time.sleep(0.1)

                scoreboard_placeholder.markdown(
                    render_score_widget(final_score_a, final_score_b),
                    unsafe_allow_html=True,
                )

            st.success(
                f"Debate concluded! Final scores - Debater A: {final_score_a:.1f}, "
                f"Debater B: {final_score_b:.1f}"
            )

        except Exception as e:
            st.error(f"An error occurred during the debate: {e}")
else:
    st.info("Configure debate parameters and click 'Start Debate' to begin.")
