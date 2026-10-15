# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS, WORD_WEIGHTS
#Improvements for def preprocess; to improve on emojis, remove punctuation, and normalize repeated characters
import re

EMOTICON_PATTERN = r"[:;=]-?[()dpo]|<3"          # :)  :-(  ;)  =D  :P  <3
EMOJI_PATTERN = r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"  # 🥲 😂 💀 etc.
TOKEN_RE = re.compile(
    rf"{EMOTICON_PATTERN}|{EMOJI_PATTERN}|[a-z0-9']+"
)
REPEAT_RE = re.compile(r"(.)\1{2,}")             # 3+ of the same char

# A negator before a word flips that word's weight, even with fillers in
# between ("not be happy", "wasn't really happy").
NEGATORS = {
    "not", "never", "no", "cannot", "ain't",
    "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't",
    "can't", "couldn't", "won't", "wouldn't", "shouldn't",
    "haven't", "hasn't", "hadn't",
    "dont", "doesnt", "didnt", "isnt", "arent", "wasnt", "cant", "wont",
}
NEGATION_FILLERS = {
    "be", "been", "being", "am", "is", "are", "was", "were", "to",
    "really", "so", "very", "too", "quite", "that",
}

# Suffixes tried (in order) so inflected forms match base-form weights:
# "loved"/"loving"/"loves" -> "love", "hated" -> "hate", "likes" -> "like".
INFLECTION_SUFFIXES = ("ing", "ed", "es", "d", "s")


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        # Weights: default +/-1 for every listed word, explicit weights override.
        self.weights = {w: 1 for w in self.positive_words}
        self.weights.update({w: -1 for w in self.negative_words})
        self.weights.update(WORD_WEIGHTS)


    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        #improved preprocessing to handle emojis, remove punctuation, and normalize repeated characters
        #tokens = cleaned.split()
        cleaned = text.strip().lower()
        
        # Normalize repeated characters: "soooo" -> "soo", "!!!!" -> "!!"
        cleaned = REPEAT_RE.sub(r"\1\1", cleaned)
        
        # Emoticons/emojis come out as their own tokens; words keep apostrophes
        # ("don't"); all other punctuation is dropped.
        return TOKEN_RE.findall(cleaned)

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _base_weight(self, token: str) -> int:
        """Weight of a token, also matching inflected forms ("loved", "hating")."""
        if token in self.weights:
            return self.weights[token]
        for suffix in INFLECTION_SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                stem = token[: -len(suffix)]
                for candidate in (stem, stem + "e"):
                    if candidate in self.weights:
                        return self.weights[candidate]
        return 0

    def _is_negated(self, tokens: List[str], i: int) -> bool:
        """True if a negator precedes tokens[i], allowing filler words between."""
        for j in range(i - 1, max(i - 4, -1), -1):
            if tokens[j] in NEGATORS:
                return True
            if tokens[j] not in NEGATION_FILLERS:
                return False
        return False

    def _weighted_tokens(self, text: str) -> List[Tuple[str, int]]:
        """(token, weight) pairs with negation already applied."""
        tokens = self.preprocess(text)
        pairs = []
        for i, token in enumerate(tokens):
            weight = self._base_weight(token)
            if weight and self._is_negated(tokens, i):
                weight = -weight
            pairs.append((token, weight))
        return pairs

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        return sum(weight for _, weight in self._weighted_tokens(text))

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """

        #Implement system to calculate negative and positive words separately for better results. 
        weights = [weight for _, weight in self._weighted_tokens(text)]
        pos = sum(w for w in weights if w > 0)
        neg = sum(w for w in weights if w < 0)

        if pos >= 2 and neg <= -1:
            return "mixed"
        elif pos + neg >= 2:
            return "positive"
        elif pos + neg <= -2:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
