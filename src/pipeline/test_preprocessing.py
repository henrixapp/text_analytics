from pipeline.preprocessing import Dropper
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
