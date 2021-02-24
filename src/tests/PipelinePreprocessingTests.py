from pipeline.preprocessing import AlphaNumericalizer, CuisineSetSplit, Dropper, Lower, Numbers2Words, SentenceSplitter, StopWordsRemoval, SpacyStep, NLTKPorterStemmer, Replacer, ExtractSentenceParts, OneHotEnc
from pipeline.pipeline import Pipeline
from pipeline.counters import SimpleCounter
import pandas as pd
import numpy as np
import pytest


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


def test_non_alphanumerical_input():
    pipe = Pipeline("alphanum", steps=[AlphaNumericalizer()])

    text = "This, is. a strange Text with # and other ^ characters"
    expected_result = "This is a strange Text with  and other  characters"
    result, _ = pipe.process(text)
    assert result == expected_result


def test_alphanumerical_input():
    pipe = Pipeline("alphanum", steps=[AlphaNumericalizer()])

    text = "this is a normal text with 100 words"
    expected_result = "this is a normal text with 100 words"
    result, _ = pipe.process(text)
    assert result == expected_result


def test_onehotenc_numpy():
    pipe = Pipeline("OneHot", steps=[OneHotEnc()])

    input = np.array(["Eins", "Zwei", "Drei", "Zwei", "Drei", "Drei"])
    one_hot = np.array([1, 2, 0, 2, 0, 0])
    enc = (np.array(["Drei", "Eins", "Zwei"]))
    (result1, result2), _ = pipe.process(input)
    assert (result1 == one_hot).all()
    assert (result2 == enc).all()


def test_onehotenc_pdseries():
    pipe = Pipeline("OneHot", steps=[OneHotEnc()])

    d = {1: "Eins", 2: "Zwei", 3: "Drei"}
    input = pd.core.series.Series(data=d, index=[1, 2, 3, 2, 3, 3])
    one_hot = np.array([1, 2, 0, 2, 0, 0])
    enc = (np.array(["Drei", "Eins", "Zwei"]))
    (result1, result2), _ = pipe.process(input)
    assert (result1 == one_hot).all()
    assert (result2 == enc).all()


def test_CuisineSplitSet():
    pipe = Pipeline("CuisineSplitSet",
                    steps=[CuisineSetSplit(training=50, rand_perm=False)])

    w2v_1 = np.array([0, 0.5, -0.5, 1, -1], dtype=np.float32)
    w2v_2 = np.array([-1, 0.4, -0.6, 0, 1], dtype=np.float32)
    onehot = np.array([0, 1])
    cuisine = np.array(['test1', 'test2'], dtype=np.object)
    names = pd.core.series.Series({0: 10, 1: 11})

    names_list = names.tolist()

    input = [[[w2v_1, w2v_2]], (onehot, cuisine), names]
    output_train = [[w2v_1], (), names]
    output_test = [[w2v_2], (), names]
    output = [output_train, output_test]

    (result_train, result_test), _ = pipe.process(input)
    train_w2v, (train_onehot, train_cuisine), train_names = result_train
    test_w2v, (test_onehot, test_cuisine), test_names = result_test

    assert (train_w2v == w2v_1).all()
    assert (test_w2v == w2v_2).all()
    assert (train_onehot == onehot[0:1]).all()
    assert (test_onehot == onehot[1:1]).all()
    assert (train_cuisine == cuisine).all()
    assert (test_cuisine == cuisine).all()
    assert (train_names == [names_list[0]])
    assert (test_names == [names_list[1]])