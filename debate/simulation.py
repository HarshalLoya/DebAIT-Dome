from agents.models import Debater, Moderator
from llm.query import query_llm


def simulate_debate(debate_topic: str):
    """
    Initializes agents, queries the LLM for opening arguments, and returns the updated agent states.
    """
    # Create agents.
    debater_a = Debater(name="Debater A", role="Debater", debate_side="Pro")
    debater_b = Debater(name="Debater B", role="Debater", debate_side="Con")
    moderator = Moderator(name="Moderator", role="Moderator")

    # Start the debate.
    moderator.start_debate()

    # Query the LLM for each opening argument.
    prompt_a = (
        f"Debate Topic: {debate_topic}\n"
        "Role: Pro Debater\n"
        "Generate a well-reasoned argument in favor of the topic."
    )
    argument_a = query_llm(prompt_a)
    debater_a.update_argument(argument_a)

    prompt_b = (
        f"Debate Topic: {debate_topic}\n"
        "Role: Con Debater\n"
        "Generate a well-reasoned argument against the topic."
    )
    argument_b = query_llm(prompt_b)
    debater_b.update_argument(argument_b)

    # Return the agent states for further use.
    return {
        "debater_a": debater_a,
        "debater_b": debater_b,
        "moderator": moderator,
    }


# For testing the simulation module separately.
if __name__ == "__main__":
    demo_topic = "Artificial intelligence should be regulated."
    states = simulate_debate(demo_topic)
    print("Debater A State:", states["debater_a"].model_dump())
    print("Debater B State:", states["debater_b"].model_dump())
    print("Moderator State:", states["moderator"].model_dump())
