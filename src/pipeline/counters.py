from pipeline.pipeline import PipelineStep, Head
from collections import Counter

class SimpleCounter(PipelineStep):
    """
    This step calculates the length of data if this is possible.
    """
    def __init__(self):
        super().__init__("simple_counter")

    def process(self, data, head=Head()):
        head.addInfo("simple_counter", "")
        assert hasattr(data, "__len__")
        return len(data), head

class MostCommonCounter(PipelineStep):
    """
    This step calculates the length of data if this is possible.
    """
    def __init__(self):
        super().__init__("simple_counter")

    def process(self, data, head=Head()):
        head.addInfo("simple_counter", "")
        assert hasattr(data, "__len__")
        counter = Counter(data)
        return counter, head