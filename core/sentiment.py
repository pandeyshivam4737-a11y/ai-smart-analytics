"""
Sentiment & Emotion Analysis Engine
Implements Rule-Based Lexicon Analysis with:
- Negation handling (e.g., "not good" -> negative)
- Intensity boosters/dampeners (e.g., "very", "extremely", "slightly")
- Polarity score: [-1.0 (very negative) to +1.0 (very positive)]
- Subjectivity score: [0.0 (objective) to 1.0 (highly subjective)]
"""

import re

# Curated Sentiment Lexicons
POSITIVE_WORDS = {
    "great": 2.0, "excellent": 2.5, "awesome": 2.5, "amazing": 2.5, "good": 1.2,
    "best": 2.5, "love": 2.0, "happy": 1.5, "fast": 1.0, "powerful": 1.8,
    "impressive": 2.0, "superior": 1.8, "effective": 1.5, "reliable": 1.5,
    "efficient": 1.5, "clean": 1.0, "brilliant": 2.2, "smart": 1.4, "innovative": 1.8,
    "accurate": 1.6, "success": 2.0, "successful": 2.0, "breakthrough": 2.2,
    "perfect": 2.5, "valuable": 1.6, "helpful": 1.4, "seamless": 1.6
}

NEGATIVE_WORDS = {
    "bad": -1.5, "terrible": -2.5, "horrible": -2.5, "poor": -1.5, "slow": -1.2,
    "buggy": -2.0, "broken": -2.0, "failed": -2.2, "failure": -2.2, "error": -1.4,
    "crash": -2.0, "crashes": -2.0, "difficult": -1.2, "complicated": -1.2,
    "worst": -2.5, "hate": -2.0, "useless": -2.2, "expensive": -1.2, "disappointing": -2.0,
    "laggy": -1.8, "unreliable": -2.0, "inaccurate": -1.8, "flawed": -1.6
}

BOOSTERS = {
    "very": 1.5, "extremely": 2.0, "super": 1.8, "incredibly": 2.0,
    "highly": 1.6, "totally": 1.5, "completely": 1.6
}

NEGATIONS = {
    "not", "never", "no", "hardly", "barely", "scarcely", "without", "isnt", "arent", "wasnt", "werent"
}

class SentimentEngine:
    def __init__(self):
        self.positive_lexicon = POSITIVE_WORDS
        self.negative_lexicon = NEGATIVE_WORDS

    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of a given text.
        Returns a dictionary with polarity, sentiment label, subjectivity, and key emotional triggers.
        """
        words = re.findall(r"\b[a-zA-Z']+\b", text.lower())
        if not words:
            return {
                "polarity": 0.0,
                "label": "Neutral",
                "subjectivity": 0.0,
                "confidence": 0.0,
                "positive_matches": [],
                "negative_matches": []
            }

        score = 0.0
        subjective_words_count = 0
        pos_matches = []
        neg_matches = []

        for i, word in enumerate(words):
            word_score = 0.0
            is_subjective = False

            if word in self.positive_lexicon:
                word_score = self.positive_lexicon[word]
                is_subjective = True
                pos_matches.append(word)
            elif word in self.negative_lexicon:
                word_score = self.negative_lexicon[word]
                is_subjective = True
                neg_matches.append(word)

            if is_subjective:
                subjective_words_count += 1

                # Check preceding 2 words for negation or booster
                multiplier = 1.0
                for lookback in range(1, 3):
                    if i - lookback >= 0:
                        prev = words[i - lookback]
                        if prev in NEGATIONS:
                            multiplier *= -0.8
                        elif prev in BOOSTERS:
                            multiplier *= BOOSTERS[prev]

                score += word_score * multiplier

        # Normalize polarity to range [-1.0, 1.0]
        max_possible = max(len(words) * 0.5, 1.0)
        polarity = max(-1.0, min(1.0, score / max_possible))
        subjectivity = min(1.0, subjective_words_count / max(len(words) * 0.25, 1.0))

        if polarity > 0.15:
            label = "Positive"
        elif polarity < -0.15:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "polarity": round(polarity, 3),
            "label": label,
            "subjectivity": round(subjectivity, 3),
            "confidence": round(abs(polarity), 2),
            "positive_matches": list(set(pos_matches)),
            "negative_matches": list(set(neg_matches))
        }
