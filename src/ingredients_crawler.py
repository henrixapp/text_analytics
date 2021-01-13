import pandas as pd
import json

from pipeline.pipeline import Pipeline
from pipeline.data_access import DataSetSource, JSONSink, PDReduce
from pipeline.generics import Flatten, IterableApply, Unique
from pipeline.preprocessing import ApplyJSON, Lower


def pipeline():
    p = Pipeline("recipennlg",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     IterableApply(ApplyJSON()),
                     Flatten(),
                     IterableApply(Lower()),
                     Unique(),
                     JSONSink("whats-cooking.json")
                 ],
                 verbosity=True)
    p.process("")


if __name__ == "__main__":
    '''
    Gets ingredients of whats cooking and recipenlg datasets and dumps them into json files.
    Does the same with the combined list from both datasets.
    '''
    pipeline()