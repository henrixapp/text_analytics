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

    def process(self, data, head):
        """
        This is the abstract PipelineStep to be implemented. Make something useful.
        @returns data, head
        """
        raise NotImplementedError

    def toInfo(self):
        """
        generate the used parameters for the head
        """
        raise NotImplementedError


class InvalidPipelineStepError(Exception):
    def __init__(self, step):
        pass


class Pipeline(PipelineStep):
    """
    aggregate several steps into a processing pipeline
    """
    def __init__(self, name, steps=[]):
        super(name)
        self.steps = steps
        for step in self.steps:
            if not isinstance(step, PipelineStep):
                raise InvalidPipelineStepError(step)

    def process(self, data, head=Head()):
        # We do not need to create a new head, if we are in a downstream pipeline.
        for step in self.steps:
            data, head = step.process(data, head)
        return data, head
