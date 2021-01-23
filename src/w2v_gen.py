from pipeline.pipeline import Pipeline

from pipeline.pipeline import Pipeline
from pipeline.data_access import DataSetSource, JSONSink, PDReduce
from pipeline.generics import First, Flatten, IterableApply, Sample, Unique
from pipeline.preprocessing import ApplyJSON, Lower
from pipeline.analysis import PhraserStep, W2VStep
def pipeline():
    p = Pipeline("recipennlg",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     IterableApply(ApplyJSON()),
                     IterableApply(IterableApply(Lower())),
                     PhraserStep(),
                     JSONSink("recipenlg-phrased.json")
                 ],
                 verbosity=True)
    p.process(True)
def pipeline2():
    p = Pipeline("word2vec", steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     First(500000),
                     IterableApply(ApplyJSON()),
                     IterableApply(IterableApply(Lower())),
                     PhraserStep(),
                     W2VStep(4)
                 ],
                 verbosity=True)
    return p.process(True)
if __name__ == "__main__":
    '''
    Gets ingredients of whats cooking and recipenlg datasets and dumps them into json files.
    Does the same with the combined list from both datasets.
    '''
    #pipeline()