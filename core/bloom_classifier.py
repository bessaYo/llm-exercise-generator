import nltk


class BloomClassifier:
    """
    Classifies a given learning objective into a Bloom's Taxonomy level based on keywords used in the sentence.
    """

    bloom_levels = {
        "create": [
            "design",
            "formulate",
            "build",
            "invent",
            "create",
            "compose",
            "generate",
            "derive",
            "modify",
            "develop",
        ],
        "evaluate": [
            "choose",
            "support",
            "relate",
            "determine",
            "defend",
            "judge",
            "grade",
            "compare",
            "contrast",
            "argue",
            "justify",
            "convince",
            "select",
            "evaluate",
        ],
        "analyze": [
            "classify",
            "categorize",
            "analyze",
            "diagram",
            "illustrate",
            "criticize",
            "simplify",
            "associate",
            "differentiate",
        ],
        "apply": [
            "calculate",
            "predict",
            "apply",
            "solve",
            "illustrate",
            "use",
            "demonstrate",
            "determine",
            "model",
            "perform",
            "present",
        ],
        "understand": [
            "describe",
            "explain",
            "paraphrase",
            "restate",
            "summarize",
            "contrast",
            "interpret",
            "discuss",
        ],
        "remember": [
            "list",
            "recite",
            "outline",
            "define",
            "name",
            "match",
            "quote",
            "recall",
            "identify",
            "label",
            "recognize",
        ],
    }

    def __init__(self):
        self.name = "bloom_classifier"
        self.stemmer = nltk.PorterStemmer()

    def classify(self, learning_objective):
        """Determines the Bloom's Taxonomy level of a given learning objective."""
        # Tokenization & POS-Tagging
        tokens = nltk.word_tokenize(learning_objective)
        tagged = nltk.pos_tag(tokens)

        # Extract verbs
        verbs = [word for word, tag in tagged if tag.startswith("VB")]

        # Stem verbs
        stems = [self.stemmer.stem(verb) for verb in verbs]

        # Get bloom levels
        matched_levels = set()
        for level, verbs in self.bloom_levels.items():
            stemmed_verbs = [self.stemmer.stem(v) for v in verbs]
            if any(stem in stemmed_verbs for stem in stems):
                matched_levels.add(level)

        return list(matched_levels) if matched_levels else ["No match found"]
