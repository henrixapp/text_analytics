class Head:
    """
    Contains all the information about a processed pipeline.
    """
    def __init__(self):
        self._infos = []
        pass

    def addInfo(self, name, info):
        """
        Adds a hashable info to this head. Please make sure to use a unique name.
        info is for flags.
        """
        self._infos += [name, info]

    def hash(self):
        """
        Recursivly create hash for identification.
        """
        kurz = ""
        for info in self._infos:
            if info is Head:
                kurz += info.hash()
            else:
                kurz += str(info)
        return hash(kurz)


class PipelineStep:
    """
    Basic PipelineStep that can be executed via process.
    """
    def __init__(self, name):
        self.name = name
        pass

    def process(self, data, head=Head()):
        """
        This is the abstract PipelineStep to be implemented. Make something useful.
        @returns data, head
        """
        raise NotImplementedError


class InvalidPipelineStepError(Exception):
    def __init__(self, step):
        pass


class Pipeline(PipelineStep):
    """
    aggregate several steps into a processing pipeline
    """
    def __init__(self, name, steps=[], verbosity=False):
        super().__init__(name)
        self.steps = steps
        self._verbose = verbosity
        for step in self.steps:
            if not isinstance(step, PipelineStep):
                raise InvalidPipelineStepError(step)

    def process(self, data, head=Head()):
        # We do not need to create a new head, if we are in a downstream pipeline.
        for step in self.steps:
            if self._verbose:
                print(step.name)
            data, head = step.process(data, head)
        return data, head

class Fork(PipelineStep):
    """
    Runs several task with the same data in parallel
    """
    def __init__(self, name, steps=[], verbosity=False):
        super().__init__(name)
        self.steps = steps
        self._verbose = verbosity
        for step in self.steps:
            if not isinstance(step, PipelineStep):
                raise InvalidPipelineStepError(step)

    def process(self, data, head=Head()):
        # We do not need to create a new head, if we are in a downstream pipeline.
        res = []
        for step in self.steps:
            if self._verbose:
                print(step.name)
            data2, head = step.process(data, head)
            res += [data2]
        return res, head

class Pass(PipelineStep):
    """
    
    """
    def __init__(self):
        super().__init__("pass")

    def process(self, data, head=Head()):
        # We do not need to create a new head, if we are in a downstream pipeline.
        return data, head