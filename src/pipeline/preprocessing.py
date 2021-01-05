from pipeline.pipeline import PipelineStep, Head
import pandas as pd
import spacy
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


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
