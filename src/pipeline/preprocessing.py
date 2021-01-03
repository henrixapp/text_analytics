from pipeline.pipeline import PipelineStep, Head
import pandas as pd
import spacy
from nltk.corpus import stopwords


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

    Supports two ways: if tooling is spacy it will automatically tookenize and remove stop words.
    TODO: Remove tokenization, when spacy step is implemented.
    Otherwise it will check the already **tokenized** words in additional_stopwords.
    Returns list of spacy tokens or plain strings.
    """
    def __init__(self,
                 tooling="spacy",
                 additional_stopwords=[]):  # tooling = spacy, none
        super().__init__("stopwordsremoval")
        self._tooling = tooling
        self._additional_stopwords = additional_stopwords
        if tooling == "spacy":
            self.nlp = spacy.load("en_core_web_sm")

    def process(self, data, head=Head()):
        head.addInfo("stopwordsremoval",
                     self._tooling + "-".join(self._additional_stopwords))
        if self._tooling == "spacy":
            doc = self.nlp(data)
            words = []
            for word in doc:
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
