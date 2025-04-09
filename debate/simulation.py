import time
from datetime import datetime
from agents.models import Debater, Moderator
from llm.query import query_llm
from debate.evaluation import score_argument


def stream_message(message: str, delay: float = 0.5):
    sentences = [s.strip() for s in message.split(".") if s.strip()]
    segments = [s + "." for s in sentences]
    for segment in segments:
        yield segment
        time.sleep(delay)


def stream_multi_round_debate(
    debate_topic: str, num_rounds: int = 3, tone: str = "Formal", max_sentences: int = 6
):
    debater_a = Debater(name="Debater A", role="Debater", debate_side="Pro")
    debater_b = Debater(name="Debater B", role="Debater", debate_side="Con")
    moderator = Moderator(name="Moderator", role="Moderator")
    moderator.start_debate()

    # Round 1: Opening arguments for both sides
    prompt_a = (
        f"Debate Topic: {debate_topic}\n"
        f"Debate Rules: {moderator.rule_set}\n"
        "When making your argument, please limit your response to no more than 6 sentences.\n"
        "Tone: " + tone + "\n"
        "Role: Pro Debater\n"
        "Generate a well-reasoned opening argument in favor of the topic."
    )
    message_a = query_llm(prompt_a)
    score_a = score_argument(message_a, debate_topic)
    debater_a.update_argument(message_a)
    debater_a.update_score(score_a)
    # Stream Debater A's message segments
    for segment in stream_message(message_a):
        yield {
            "round": 1,
            "debater": "Debater A",
            "text": segment,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "score": debater_a.score,
        }

    prompt_b = (
        f"Debate Topic: {debate_topic}\n"
        f"Debate Rules: {moderator.rule_set}\n"
        "When making your argument, please limit your response to no more than 6 sentences.\n"
        "Tone: " + tone + "\n"
        "Role: Con Debater\n"
        "Generate a well-reasoned opening argument against the topic."
    )
    message_b = query_llm(prompt_b)
    score_b = score_argument(message_b, debate_topic)
    debater_b.update_argument(message_b)
    debater_b.update_score(score_b)
    # Stream Debater B's message segments
    for segment in stream_message(message_b):
        yield {
            "round": 1,
            "debater": "Debater B",
            "text": segment,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "score": debater_b.score,
        }

    # Rounds 2 ... num_rounds: Rebuttals
    for round_num in range(2, num_rounds + 1):
        moderator.next_round()
        # Pro's rebuttal to Con's last argument
        pro_rebuttal_prompt = (
            f"Debate Topic: {debate_topic}\n"
            f"Debate Rules: {moderator.rule_set}\n"
            "When making your argument, please limit your response to no more than 6 sentences.\n"
            "Tone: " + tone + "\n"
            "Role: Pro Debater\n"
            f'Your opponent previously argued: "{debater_b.argument_history[-1]}"\n'
            "Provide a concise rebuttal addressing the opponent's points."
        )
        message_a_rebuttal = query_llm(pro_rebuttal_prompt)
        score_a_rebuttal = score_argument(message_a_rebuttal, debate_topic)
        debater_a.update_argument(message_a_rebuttal)
        debater_a.update_score(score_a_rebuttal)
        for segment in stream_message(message_a_rebuttal):
            yield {
                "round": round_num,
                "debater": "Debater A",
                "text": segment,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "score": debater_a.score,
            }

        # Con's rebuttal to Pro's last argument
        con_rebuttal_prompt = (
            f"Debate Topic: {debate_topic}\n"
            f"Debate Rules: {moderator.rule_set}\n"
            "When making your argument, please limit your response to no more than 6 sentences.\n"
            "Tone: " + tone + "\n"
            "Role: Con Debater\n"
            f'Your opponent previously argued: "{debater_a.argument_history[-1]}"\n'
            "Provide a concise rebuttal addressing the opponent's points."
        )
        message_b_rebuttal = query_llm(con_rebuttal_prompt)
        score_b_rebuttal = score_argument(message_b_rebuttal, debate_topic)
        debater_b.update_argument(message_b_rebuttal)
        debater_b.update_score(score_b_rebuttal)
        for segment in stream_message(message_b_rebuttal):
            yield {
                "round": round_num,
                "debater": "Debater B",
                "text": segment,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "score": debater_b.score,
            }
