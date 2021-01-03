from pipeline.pipeline import Pipeline
from pipeline.generics import IterableApply
from pipeline.counters import SimpleCounter


def test_iterable_apply_in_pipeline():
    pipeline = Pipeline("test", steps=[IterableApply(SimpleCounter())])
    data, head = pipeline.process([[1, 2, 3], [4, 5, 6]])
    assert len(data) == 2
    assert data[0] == 3
