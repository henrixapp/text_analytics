from pipeline.pipeline import InvalidPipelineStepError, PipelineStep, Head
import pandas as pd
import spacy
from spacy.lang.en import English
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from num2words import num2words
import json


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
    This is a common Spacy-Step.
    @input string
    @returns array of words 
    """
    def __init__(self, model="en_core_web_sm", disable=[]):
        self._nlp = spacy.load(model, disable=disable)
        self._disabled = disable
        super().__init__("spacy")

    def process(self, data, head=Head()):
        head.addInfo("spacy_", "-".join(self._disabled))

        return self._nlp(data), head


class NLTKPorterStemmer(PipelineStep):
    """
    Wraps a stemmer.
    @input single string!
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
    Replaces all occurances of the dict  in the string.
    """
    def __init__(self, rules):
        self._rules = rules
        super().__init__("replacer")

    def process(self, data, head=Head()):
        for old, new in self._rules.items():
            head.addInfo(self.name, old + "_" + new)
            data = data.replace(old, new)
        return data, head


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
    def __init__(self):
        super().__init__("ApplyJSON")

    def process(self, data, head=Head()):
        '''
        converts string of json object to json object or empty list if none
        '''
        head.addInfo("ApplyJSON", "")
        result = json.loads(data)
        if result:
            return result, head
        return [], head
