from typing import List, Optional
from pydantic import BaseModel, Field


class Agent(BaseModel):
    name: str
    role: str  # "Debater" or "Moderator"
    current_argument: Optional[str] = Field(
        default=None, description="The argument for the current round."
    )
    argument_history: List[str] = Field(
        default_factory=list, description="History of all arguments made by the agent."
    )
    score: float = Field(default=0.0, description="Cumulative score for the agent.")

    def update_argument(self, new_argument: str) -> None:
        self.current_argument = new_argument
        self.argument_history.append(new_argument)

    def update_score(self, points: float) -> None:
        self.score += points


class Debater(Agent):
    debate_side: str = Field(
        ..., description="Side of the debate, e.g., 'Pro' or 'Con'"
    )


class Moderator(Agent):
    rule_set: str = Field(
        default="Default Debate Rules: Be concise, use logic and evidence, and limit each argument to no more than six sentences.",
        description="Debate rules defined by the moderator.",
    )
    rounds: int = Field(
        default=0, description="The current round number of the debate."
    )

    def start_debate(self) -> None:
        """Initialize the debate by resetting the round count."""
        self.rounds = 1
        print(f"Debate started with rules: {self.rule_set}")

    def next_round(self) -> None:
        """Increment the round count."""
        self.rounds += 1
        print(f"Starting round {self.rounds}...")
