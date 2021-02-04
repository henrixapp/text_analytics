from pipeline.pipeline import Pipeline, PipelineStep, Head
import random
from tqdm import tqdm


class IterableApply(PipelineStep):
    """
    returns a list.
    No parallelization is done here!
    """
    def __init__(self, step, verbosity=False):
        super().__init__("iterable_apply")
        self._step = step
        self._verbosity = verbosity
        assert isinstance(self._step, PipelineStep)

    def process(self, data, head=Head()):
        assert hasattr(data, "__iter__")
        newdata = []
        head_i = []
        if self._verbosity:
            for i in tqdm(data):
                data_i, _ = self._step.process(i)
                newdata += [data_i]
        else:
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


class First(PipelineStep):
    """
    Returns the first `count` elements of an indexible object (list, dataframe, ...)
    """
    def __init__(self, count):
        super().__init__("first")
        self._count = count

    def process(self, data, head):
        head.addInfo(self.name, self._count)
        return data[:self._count], head


class Unique(PipelineStep):
    """
    Makes a unique list.
    """
    def __init__(self):
        super().__init__("unique")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return list(set(data)), head


class Flatten(PipelineStep):
    """
    Merges nested lists
    """
    def __init__(self):
        super().__init__("flatten")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return [d for t in data for d in t], head


class ZipList(PipelineStep):
    """
    Ziplists data
    """
    def __init__(self):
        super().__init__("ziplist")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return list(zip(*data)), head


class TransformList(PipelineStep):
    """
    Transforms list with given key and valuefunction.
    """
    def __init__(self, key, value):
        self.key = key
        self.valuefunc = value
        super().__init__("transform")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        values = set(map(self.key, data))
        return [[self.valuefunc(y) for y in data if self.key(y) == x]
                for x in values], head


class Lambda(PipelineStep):
    """
    Allows to apply arbitrary lambda functions on the data.
    """
    def __init__(self, l):
        self.func = l
        super().__init__("lambda")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        return self.func(data), head