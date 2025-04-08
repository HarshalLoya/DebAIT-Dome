from agents.models import Debater, Moderator
from llm.query import query_llm


def simulate_multi_round_debate(debate_topic: str, num_rounds: int = 3):
    """
    Simulate a multi-round debate between Pro and Con debaters.

    - Round 1: Opening arguments.
    - Rounds 2 to num_rounds: Rebuttals where each debater
      addresses their opponent's latest argument.

    Each argument is required to be concise – no more than six sentences – and must
    follow the debate rules provided by the moderator.
    """
    # Create agents
    debater_a = Debater(name="Debater A", role="Debater", debate_side="Pro")
    debater_b = Debater(name="Debater B", role="Debater", debate_side="Con")
    moderator = Moderator(name="Moderator", role="Moderator")

    moderator.start_debate()

    # Round 1: Opening arguments for both sides.
    prompt_a = (
        f"Debate Topic: {debate_topic}\n"
        f"Debate Rules: {moderator.rule_set}\n"
        "When making your argument, please limit your response to no more than 6 sentences.\n"
        "Role: Pro Debater\n"
        "Generate a well-reasoned opening argument in favor of the topic."
    )
    argument_a = query_llm(prompt_a)
    debater_a.update_argument(argument_a)

    prompt_b = (
        f"Debate Topic: {debate_topic}\n"
        f"Debate Rules: {moderator.rule_set}\n"
        "When making your argument, please limit your response to no more than 6 sentences.\n"
        "Role: Con Debater\n"
        "Generate a well-reasoned opening argument against the topic."
    )
    argument_b = query_llm(prompt_b)
    debater_b.update_argument(argument_b)

    # Rounds 2...num_rounds: Rebuttals.
    for round_num in range(2, num_rounds + 1):
        moderator.next_round()
        # Pro's rebuttal to Con's most recent argument.
        pro_rebuttal_prompt = (
            f"Debate Topic: {debate_topic}\n"
            f"Debate Rules: {moderator.rule_set}\n"
            "When making your argument, please limit your response to no more than 6 sentences.\n"
            "Role: Pro Debater\n"
            f'Your opponent previously argued: "{debater_b.argument_history[-1]}"\n'
            "Provide a concise rebuttal addressing the opponent's points."
        )
        rebuttal_a = query_llm(pro_rebuttal_prompt)
        debater_a.update_argument(rebuttal_a)

        # Con's rebuttal to Pro's latest argument.
        con_rebuttal_prompt = (
            f"Debate Topic: {debate_topic}\n"
            f"Debate Rules: {moderator.rule_set}\n"
            "When making your argument, please limit your response to no more than 6 sentences.\n"
            "Role: Con Debater\n"
            f'Your opponent previously argued: "{debater_a.argument_history[-1]}"\n'
            "Provide a concise rebuttal addressing the opponent's points."
        )
        rebuttal_b = query_llm(con_rebuttal_prompt)
        debater_b.update_argument(rebuttal_b)

    return {
        "debater_a": debater_a,
        "debater_b": debater_b,
        "moderator": moderator,
    }


if __name__ == "__main__":
    topic = "It would be better to be able to fly than to be able to turn invisible"
    states = simulate_multi_round_debate(topic, num_rounds=3)
    print("Debater A State:", states["debater_a"].model_dump())
    print("\nDebater B State:", states["debater_b"].model_dump())
    print("\nModerator State:", states["moderator"].model_dump())
