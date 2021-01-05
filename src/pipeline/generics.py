from pipeline.pipeline import PipelineStep, Head
import random


class IterableApply(PipelineStep):
    """
    returns a list.
    No parallelization is done here!
    """
    def __init__(self, step):
        super().__init__("iterable_apply")
        self._step = step
        assert isinstance(self._step, PipelineStep)

    def process(self, data, head=Head()):
        assert hasattr(data, "__iter__")
        newdata = []
        head_i = []
        for i in data:
            data_i, _ = self._step.process(i)
            newdata += [data_i]
        head.addInfo("iterable_apply", self._step.name)
        return newdata, head


class Sample(PipelineStep):
    """
    Samples number out of a list, based on the given seed. 
    """
    def __init__(self, number, seed=0):
        super().__init__("sample" + str(number) + "_s" + str(seed))
        self._seed = seed
        self._number = number

    def process(self, data, head=Head()):
        random.seed(self._seed)
        head.addInfo(self.name, "")
        return random.sample(data, self._number), head
