from pipeline.pipeline import PipelineStep, Head
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
def hash(astring):
    return ord(astring[0])

class TFIDFStep(PipelineStep):
    """
    TODO Which data preprocessing has to be done before?
    """
    def __init__(self):
        super().__init__("tfidf")

    def process(self, data, head=Head()):
        transformer = TfidfTransformer().fit_transform(data)
        head.addInfo("tfidf")
        tfidf = np.mean(
            transformer, axis=0
        )  ### Don't forget that you need the tfidf values for a single word averaged across documents ####
        return tfidf, head


class PhraserStep(PipelineStep):
    """
    Generates a phrased version of the inputted text., input is flattened
    expects str step data [[str]]
    """
    def __init__(self, min_count=5):
        super().__init__("phraser")
        self._mincount = min_count

    def process(self, data, head=Head()):
        head.addInfo(self.name, str(self._mincount))
        new_lines = [[w for w in sent] for sent in data]
        phrases = Phrases(new_lines, min_count=self._mincount)
        return [phrases[[w for w in sent]] for sent in data], head


class W2VStep(PipelineStep):
    """
    This step returns a W2V instance of the inputed data
    """
    def __init__(self):
        super().__init__("w2v")

    def process(self, data, head=Head()):
        head.addInfo(self.name,"")
        w2v = Word2Vec(
            data,
            hashfxn=hash,
            workers=1,
            size=100,
            negative=20,
            min_count=2,
            window=3,
            sample=6e-5,
            alpha=0.03,
            min_alpha=0.0001,
            iter=0  # in newer versions the iter keyword changed to epoch
        )
        w2v.build_vocab(data, update=True) ### your code ### # maybe use vocab here?
        w2v.train(data, total_examples=w2v.corpus_count,epochs=100)
        w2v.init_sims(replace=True)
        return w2v, head
