from pipeline.pipeline import Pipeline
from pipeline.generics import IterableApply, Sample
from pipeline.counters import SimpleCounter


def test_iterable_apply_in_pipeline():
    pipeline = Pipeline("test", steps=[IterableApply(SimpleCounter())])
    data, head = pipeline.process([[1, 2, 3], [4, 5, 6]])
    assert len(data) == 2
    assert data[0] == 3


def test_sample():
    data = [1, 2, 3, 4, 5, 6, 7]
    pipeline = Pipeline("test", steps=[Sample(5)])
    result, _ = pipeline.process(data)
    assert sorted(result) == sorted([7, 4, 6, 1, 2])
