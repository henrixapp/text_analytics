from pipeline.pipeline import InvalidPipelineStepError, PipelineStep, Head
import pandas as pd
import spacy
import numpy as np
from spacy.lang.en import English
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from num2words import num2words
import json
import re
from math import ceil


class Dropper(PipelineStep):
    """
    drops data in a dataframe, if they are none for given columns.
    """
    def __init__(self, columns_causing_drop=[], inplace=True):
        super().__init__("dropper_")
        self._columns = columns_causing_drop
        assert hasattr(self._columns,
                       "__iter__"), "columns_causing_drop must be iterable!"
        self._inplace = inplace

    def process(self, data, head=Head()):
        assert isinstance(data, pd.DataFrame)
        head.addInfo(self.name, "-".join(self._columns))
        data.dropna(subset=self._columns, inplace=self._inplace)
        return data, head


class StopWordsRemoval(PipelineStep):
    """
    Removes stop words.

    Supports two ways: if tooling is spacy it will expect data from spacy step and remove stop words.
    Otherwise it will check the already **tokenized** words in additional_stopwords.
    Returns list of spacy tokens or plain strings.
    """
    def __init__(self,
                 tooling="spacy",
                 additional_stopwords=[]):  # tooling = spacy, none
        super().__init__("stopwordsremoval")
        self._tooling = tooling
        self._additional_stopwords = additional_stopwords

    def process(self, data, head=Head()):
        head.addInfo("stopwordsremoval",
                     self._tooling + "-".join(self._additional_stopwords))
        if self._tooling == "spacy":
            words = []
            for word in data:
                if not word.is_stop and not word.text in self._additional_stopwords:
                    words += [word]
            return words, head
        else:
            doc = data
            words = []
            for word in doc:
                if not word in self._additional_stopwords:
                    words += [word]
            return words, head


class SpacyStep(PipelineStep):
    """
    This is a common Spacy-Step. It allows disabling steps from Spacy for faster performance.
    @input string
    @returns array of words 
    """
    def __init__(self, model="en_core_web_sm", disable=[]):
        self._nlp = spacy.load(model, disable=disable)
        self._disabled = disable
        super().__init__("spacy")

    def process(self, data, head=Head()):
        head.addInfo("spacy_", "-".join(self._disabled))

        return self._nlp(str(data)), head


class NLTKPorterStemmer(PipelineStep):
    """
    Wraps an NLTK stemmer.
    @input **single** string! Must be without leading or trailing punctuation.
    @output stemmed string
    """
    def __init__(self):
        self._stemmer = PorterStemmer()
        super().__init__("nltk_porter")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return self._stemmer.stem(data), head


class Replacer(PipelineStep):
    """
    Replaces all occurrences of the dict in the string.
    """
    def __init__(self, rules):
        self._rules = rules
        super().__init__("replacer")

    def process(self, data, head=Head()):
        for old, new in self._rules.items():
            head.addInfo(self.name, old + "_" + new)
            data = data.replace(old, new)
        return data, head


class Split(PipelineStep):
    """
    Splits at rule which is a string.
    """
    def __init__(self, rule):
        self._rule = rule
        super().__init__("splitter")

    def process(self, data, head=Head()):

        return str(data).split(self._rule), head


class ExtractSentenceParts(PipelineStep):
    """
    Extracts all nouns if "NOUN" is in parts and/or all verbs if "VERB"
    @input expects an array of spacy items
    """
    def __init__(self, parts=["NOUN"]):
        super().__init__("extract_" + "-".join(parts))
        self._parts = parts

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")

        return [word for word in data if word.pos_ in self._parts], head


class SentenceSplitter(PipelineStep):
    """
    Splits a string into a list of substrings based on sentences.
    """
    def __init__(self):
        super().__init__("splitter")
        self._nlp = English()
        sentencizer = self._nlp.create_pipe("sentencizer")
        self._nlp.add_pipe(sentencizer)

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        assert isinstance(data, str), "data to split must be a string"
        doc = self._nlp(data)
        return [sent.text for sent in doc.sents], head


class Numbers2Words(PipelineStep):
    """
    Converts numbers (e.g. 2) into words (e.g. two).
    @input expects an array of spacy items
    """
    def __init__(self):
        super().__init__("num2word")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return [
            num2words(word.text) if word.like_num else word.text
            for word in data
        ], head


class Lower(PipelineStep):
    """
    Converts string to lower-cased string
    @input expects an array of string or a string
    """
    def __init__(self):
        super().__init__("lower")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        if isinstance(data, list):
            newdata = []
            for item in data:
                assert isinstance(item, str), "Values in list must be strings"
                newdata += [item.lower()]
            return newdata, head
        elif isinstance(data, str):
            return data.lower(), head
        else:
            raise InvalidPipelineStepError


class ApplyJSON(PipelineStep):
    """
    Converts a string of json object to json object or empty list if none
    """
    def __init__(self):
        super().__init__("ApplyJSON")

    def process(self, data, head=Head()):

        head.addInfo("ApplyJSON", "")
        result = json.loads(data)
        if result:
            return result, head
        return [], head


class OutOfDistributionRemover(PipelineStep):
    """
    Removes recipes that are out of distribution, e.g. have a lot more steps or ingredients than usual.
    The limits can be adjusted by setting max_steps and max_ingredients.
    """
    def __init__(self, max_steps=15, max_ingredients=15):
        super().__init__("OutOfDistributionRemover")
        self.max_steps = max_steps
        self.max_ingredients = max_ingredients

    def process(self, data, head=Head()):

        head.addInfo(
            self.name,
            "Max steps to stay in set: {}, max ingredients {}.".format(
                self.max_steps, self.max_ingredients))
        data["n_steps"] = data["steps"].apply(len)
        data["n_ingredients"] = data["ingredients"].apply(len)
        return data[(data["n_steps"] <= self.max_steps)
                    & (data["n_ingredients"] <= self.max_ingredients)], head


class AlphaNumericalizer(PipelineStep):
    """
    Removes characters that are not within a-z, A-Z, 0-9 and spaces
    """
    def __init__(self):
        super().__init__("AlphaNumericalizer")

    def process(self, data, head=Head()):

        head.addInfo(self.name, "")
        return re.sub(r'[^0-9a-zA-Z ]', '', data), head



class OneHotEnc(PipelineStep):
    """
    OneHot encoding. expects 1-D numpy array or pandas.core.series.Series

    Output: data: vector of one hot encoding and vector with encoding
            head
    """
    def __init__(self):
        super().__init__("Onehot")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        if (type(data) == pd.core.series.Series): data = data.to_numpy()

        cuisines_unique = np.sort(np.unique(data))
        n_cuisines_unique = cuisines_unique.shape[0]

        targets = np.empty(data.shape,dtype=int)
        for index in range(n_cuisines_unique):
            added_targets = np.where(data == cuisines_unique[index])
            targets[added_targets] = index

        assert (cuisines_unique[targets] == data).all(), "Something went wrong inside the one hot encoding."
        data = targets, cuisines_unique
        return data, head

class CuisineSetSplit(PipelineStep):
    """
    Training and Testing Dataset Split for Cuisine Pipeline.

    Call Input: training split size in percent [Default: 80]

    Process:
        Input: w2v, cuisine (onehot, encoding), names
        Output: 2 times split input with training%, 1-training% split as tuple
    """
    def __init__(self, training = 80):
        super().__init__("CuisineSetSplit")
        self.training = training

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")

        w2v, cuisine, names = data
        names = names.tolist()
        onehot, encoding = cuisine
        n_set = onehot.shape[0]
        t_set = ceil(n_set*(self.training/100))

        permutation = list(np.random.permutation(n_set))
        print(f"Sizes: Dataset: {len(permutation)}, TrainingSet: {len(permutation[0:t_set])}, TestSet: {len(permutation[t_set:])}")

        trainings_w2v = [w2v[0][i] for i in permutation[0:t_set]]
        trainings_onehot = [onehot[i] for i in permutation[0:t_set]]
        trainings_names = [names[i] for i in permutation[0:t_set]]
        trainings_data = trainings_w2v, (trainings_onehot, encoding), trainings_names

        test_w2v = [w2v[0][i] for i in permutation[t_set:]]
        test_onehot = [onehot[i] for i in permutation[t_set:]]
        test_names = [names[i] for i in permutation[t_set:]]
        test_data = test_w2v, (test_onehot, encoding), test_names

        data = (trainings_data, test_data)
        return data, head

