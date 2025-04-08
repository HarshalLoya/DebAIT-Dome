import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Agent(BaseModel):
    name: str
    role: str  # e.g., "Debater" or "Moderator"
    current_argument: Optional[str] = Field(
        default=None, description="The argument generated in the current round"
    )
    argument_history: List[str] = Field(
        default_factory=list, description="History of all arguments made by the agent"
    )
    score: float = Field(default=0.0, description="Cumulative score for the agent")

    def update_argument(self, new_argument: str) -> None:
        """
        Updates the current argument and appends it to the argument history.
        """
        self.current_argument = new_argument
        self.argument_history.append(new_argument)

    def update_score(self, points: float) -> None:
        """
        Adds points to the agent's score.
        """
        self.score += points


class Debater(Agent):
    debate_side: str = Field(
        ..., description="Side of the debate, e.g., 'Pro' or 'Con'"
    )


class Moderator(Agent):
    rule_set: str = Field(
        default="Default Debate Rules",
        description="Debate rules defined by the moderator",
    )
    rounds: int = Field(default=0, description="The current round number of the debate")

    def start_debate(self) -> None:
        """
        Initializes the debate by resetting the round count.
        """
        self.rounds = 1
        print(f"Debate started with rules: {self.rule_set}")

    def next_round(self) -> None:
        """
        Increments the round count.
        """
        self.rounds += 1
        print(f"Starting round {self.rounds}...")


def query_llm(prompt: str) -> str:
    """
    Queries the Llama-3.3-70B-Versatile model via its API using a role-content
    structure and returns the generated text.
    """
    api_key = os.getenv("GROQ_LLAMA_70B_VERSATILE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set the 'GROQ_API_KEY' environment variable."
        )

    # NOTE: If you receive a 404 error,
    # please verify the API endpoint URL in your Groq docs.
    # Example alternative endpoint might be:
    # "https://api.groq.com/v1/engines/llama-3.3-70b-versatile/chat/completions"
    api_url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        # Assuming the API returns:
        # { "choices": [ { "message": { "content": "..." } } ] }
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "No content found in API response."
    else:
        return f"Error: {response.status_code} - {response.text}"


# Testing integration along with the agent models
if __name__ == "__main__":
    # Create debaters and moderator
    debater_a = Debater(name="Debater A", role="Debater", debate_side="Pro")
    debater_b = Debater(name="Debater B", role="Debater", debate_side="Con")
    moderator = Moderator(name="Moderator", role="Moderator")

    # Start the debate
    moderator.start_debate()

    # Define the debate topic
    debate_topic = "Artificial intelligence should be regulated."

    # Generate opening argument for Debater A (Pro)
    prompt_a = (
        f"Debate Topic: {debate_topic}\n"
        f"Role: Pro Debater\n"
        "Generate a well-reasoned argument in favor of the topic."
    )
    argument_a = query_llm(prompt_a)
    debater_a.update_argument(argument_a)
    print("\nDebater A's Opening Argument:")
    print(argument_a)

    # Generate opening argument for Debater B (Con)
    prompt_b = (
        f"Debate Topic: {debate_topic}\n"
        f"Role: Con Debater\n"
        "Generate a well-reasoned argument against the topic."
    )
    argument_b = query_llm(prompt_b)
    debater_b.update_argument(argument_b)
    print("\nDebater B's Opening Argument:")
    print(argument_b)

    # Display the current state of each agent using model_dump_json (Pydantic V2+)
    print("\nCurrent status of the debate:")
    print("Debater A:")
    print(debater_a.model_dump_json(indent=2))
    print("\nDebater B:")
    print(debater_b.model_dump_json(indent=2))
    print("\nModerator:")
    print(moderator.model_dump_json(indent=2))
