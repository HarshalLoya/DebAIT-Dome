import re
import nltk

# nltk.download('stopwords')
from nltk.corpus import stopwords


def score_argument(argument: str, debate_topic: str) -> float:
    """
    Scores the given argument on several criteria:

    - Relevance: proportion of debate topic words that appear in the argument.
    - Coherence: based on sentence count (arguments should be brief and logical).
    - Factuality: counts the presence of key factual indicators.
    - Persuasiveness: counts persuasive phrases.

    Returns an overall score (0-10) rounded to two decimals.
    """
    stop_words = set(stopwords.words("english"))

    # 1. Relevance: Count how many words from the debate topic appear in the argument.
    topic_words = [
        word for word in debate_topic.lower().split() if word not in stop_words
    ]
    argument_words = [
        word for word in argument.lower().split() if word not in stop_words
    ]
    if argument_words:
        relevance_ratio = len(
            [word for word in argument_words if word in topic_words]
        ) / len(argument_words)
    else:
        relevance_ratio = 0
    # Map ratio to a 0-10 scale.
    relevance_score = min(relevance_ratio * 10, 10)

    # 2. Coherence: A concise argument will have no more than 6 sentences.
    sentences = re.split(r"(?<=[.!?])\s+", argument.strip())
    num_sentences = len(sentences)
    # If within acceptable range, assign high coherence; otherwise, penalize.
    if num_sentences <= 6:
        coherence_score = 10
    else:
        coherence_score = max(10 - (num_sentences - 6), 0)

    # 3. Factuality: Check for keywords that suggest evidence or data.
    factual_keywords = {"fact", "evidence", "research", "study", "data", "statistics"}
    factual_count = sum(
        1 for word in argument.lower().split() if word.strip(".,") in factual_keywords
    )
    factual_score = min(factual_count, 10)  # Each occurrence gives 1 point, maximum 10.

    # 4. Persuasiveness: Look for persuasive connectors.
    persuasive_keywords = {"therefore", "thus", "hence", "consequently", "so"}
    persuasive_count = sum(
        1
        for word in argument.lower().split()
        if word.strip(".,") in persuasive_keywords
    )
    persuasive_score = min(persuasive_count, 10)

    # Overall score is the average of the individual scores.
    overall_score = (
        relevance_score + coherence_score + factual_score + persuasive_score
    ) / 4
    return round(overall_score, 2)
