from pipeline.preprocessing import Dropper, Lower, Numbers2Words, SentenceSplitter, StopWordsRemoval, SpacyStep, NLTKPorterStemmer, Replacer, ExtractSentenceParts
from pipeline.pipeline import Pipeline
from pipeline.counters import SimpleCounter
import pandas as pd


def test_dropper():
    df = pd.DataFrame(
        {
            'num_legs': [2, 4, 8, 0],
            'num_wings': [2, 0, None, 0],
            'num_specimen_seen': [10, 2, 1, 8]
        },
        index=['falcon', 'dog', 'spider', 'fish'])
    pipeline = Pipeline(
        "test",
        steps=[Dropper(columns_causing_drop=["num_wings"]),
               SimpleCounter()])
    data, head = pipeline.process(df)
    assert data == 3


def test_negation_dropper():
    df = pd.DataFrame(
        {
            'num_legs': [2, 4, 8, 0],
            'num_wings': [2, 0, 3, 0],
            'num_specimen_seen': [10, 2, 1, 8]
        },
        index=['falcon', 'dog', 'spider', 'fish'])
    pipeline = Pipeline(
        "test",
        steps=[Dropper(columns_causing_drop=["num_wings"]),
               SimpleCounter()])
    data, head = pipeline.process(df)
    assert data == 4


def test_stopword_removal_none():
    text = ["i", "have", "a", "dream"]
    pipeline = Pipeline("test",
                        steps=[
                            StopWordsRemoval(tooling="none",
                                             additional_stopwords=["i", "a"]),
                            SimpleCounter()
                        ])
    count, _ = pipeline.process(text)
    assert count == 2


def test_stopword_removal_spacy():
    text = "i have a dream"
    pipeline = Pipeline("test",
                        steps=[
                            SpacyStep(),
                            StopWordsRemoval(tooling="spacy"),
                            SimpleCounter()
                        ])
    count, _ = pipeline.process(text)
    assert count == 1


def test_nltk_stemmer():
    text = "cooking"
    pipeline = Pipeline("test", steps=[NLTKPorterStemmer()])
    data, head = pipeline.process(text)
    assert data == "cook"


def test_replacer():
    text = "old car is the new station"
    pipeline = Pipeline("test",
                        steps=[Replacer({
                            "old": "new",
                            "car": "train"
                        })])
    data, head = pipeline.process(text)
    assert data == "new train is the new station"


def test_extract_sentenceparts_verb():
    pipe = Pipeline("test",
                    steps=[
                        SpacyStep(),
                        ExtractSentenceParts(parts=["VERB"]),
                        SimpleCounter()
                    ])
    text = "I love programming text analytics"
    result, head = pipe.process(text)
    assert result == 1


def test_extract_sentenceparts_noun():
    pipe = Pipeline("test",
                    steps=[
                        SpacyStep(),
                        ExtractSentenceParts(parts=["NOUN"]),
                        SimpleCounter()
                    ])
    text = "I love programming text analytics"
    result, head = pipe.process(text)
    assert result == 3


def test_sentence_splitter():
    pipe = Pipeline("test", steps=[SentenceSplitter(), SimpleCounter()])
    text = "This is a sentence. This is another sentence."
    result, _ = pipe.process(text)
    assert result == 2


def test_sentence_splitter_content():
    pipe = Pipeline("test", steps=[SentenceSplitter()])
    text = "This is a sentence. This is another sentence."
    result, _ = pipe.process(text)
    assert result[0] == "This is a sentence."


def test_num2words():
    pipe = Pipeline("test", steps=[SpacyStep(), Numbers2Words()])
    text = "Take 3 eggs and 35 tablespoons of flour"
    expected_result = "Take three eggs and thirty-five tablespoons of flour"
    result, _ = pipe.process(text)
    assert result == expected_result.split()


def test_lower():
    pipe = Pipeline("test", steps=[Lower()])
    text = "Sometimes PEOPLE mark their Recipes in WEIRD casing LETTers"
    expected_result = "sometimes people mark their recipes in weird casing letters"
    result, _ = pipe.process(text)
    assert result == expected_result


def test_lower_multiple():
    pipe = Pipeline("test", steps=[Lower()])
    text = [
        "Sometimes PEOPLE mark their Recipes in WEIRD casing LETTers",
        "THIS is a Second recipe"
    ]
    expected_result = [
        "sometimes people mark their recipes in weird casing letters",
        "this is a second recipe"
    ]
    result, _ = pipe.process(text)
    assert result == expected_result
