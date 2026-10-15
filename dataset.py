"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# Strong words get larger magnitudes; listed words not in this dict default to +/-1.
WORD_WEIGHTS = {
    # positive
    "love": 5, "amazing": 4, "awesome": 4, "excited": 3, "great": 3,
    "happy": 3, "proud": 3, "hopeful": 2, "fun": 2, "good": 2,
    "like": 2, "chill": 1, "relaxed": 1,
    ":)": 2, "😂": 2,
    # negative
    "hate": -5, "terrible": -4, "awful": -4, "angry": -3, "dislike": -2,
    "sad": -3, "upset": -3, "stressed": -2, "bad": -2, "tired": -1,
    "boring": -1, ":(": -2, "💀": -1,
    # slang (positive)
    "fire": 3, "sick": 3, "lit": 3, "goated": 4, "slaps": 3, "dope": 3,
    # slang (negative)
    "mid": -2, "cringe": -3, "trash": -3, "ugh": -2, "meh": -1,
}

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# Added posts using Claude: 5 straightforward, then 5 ambiguous edge cases.
SAMPLE_POSTS.extend([
    # Straightforward
    "No cap, this pizza is amazing 😂",
    "I hate waiting in long lines",
    "Just got the job offer, so happy right now :)",
    "Feeling really sad and alone tonight :(",
    "The meeting is at 3pm in room 204",
    # Edge cases
    "I absolutely love getting stuck in traffic",
    "Lowkey stressed but kind of proud of myself",
    "Great, another Monday 💀",
    "Passed the exam 🥲",
    "Well, that happened",
    #SLANG TERMS
    "This pizza is fire",
    "That game was so sick, I can't believe we won",
])

TRUE_LABELS.extend([
    # Straightforward
    "positive",  # "No cap, this pizza is amazing 😂"
    "negative",  # "I hate waiting in long lines"
    "positive",  # "Just got the job offer, so happy right now :)"
    "negative",  # "Feeling really sad and alone tonight :("
    "neutral",   # "The meeting is at 3pm in room 204"
    # Edge cases
    "negative",  # sarcasm: "love" is positive but the meaning is negative
    "mixed",     # slang + both stress and pride
    "negative",  # sarcastic "Great" plus 💀
    "mixed",     # 🥲 can mean relief, tears, or both
    "neutral",   # could be read as negative or neutral depending on tone
    "positive",  # slang: "fire" means good
    "positive",  # slang: "sick" means good

])


# Remember to keep them aligned:
len(SAMPLE_POSTS) == len(TRUE_LABELS)


