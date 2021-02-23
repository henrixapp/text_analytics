import string


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

    def visualize(self):
        """
        Returns a graphviz string
        """
        id_ = str(id(self))
        return id_ + ' [ label="' + self.name + '"]\n'

    def visualize_digraph(self):
        return """digraph G {{
{2}
start -> {0}
{1}->end""".format(self.begin_viz(), self.end_viz(), self.visualize()) + "\n}"

    def begin_viz(self):
        """
        returns the node of the beginning
        """
        return str(id(self))

    def end_viz(self):
        """
        returns the node of the beginning
        """
        return str(id(self))


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

    def visualize(self):
        content = ""
        prev = None
        for step in self.steps:
            content += step.visualize()
            if prev != None:
                content += "{0}->{1}\n".format(prev.end_viz(),
                                               step.begin_viz())
            prev = step
        res = """subgraph cluster_{0} {{
style=filled;
label="{1}"
{2}
graph[style=dashed];
}}
""".format(str(id(self)), self.name, content)

        return res

    def begin_viz(self):
        """
        returns the node of the beginning
        """
        return self.steps[0].begin_viz()

    def end_viz(self):
        """
        returns the node of the beginning
        """
        return self.steps[len(self.steps) - 1].end_viz()


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

    def visualize(self):
        res = """subgraph cluster_{0} {{
            node [style=filled];
style=filled;
label="{1}";
    graph[style=dotted];
{2}
""".format(str(id(self)), self.name,
           str(id(self)) + ' [label="split",shape=diamond]')
        id_ = str(id(self)) + "2"
        res += id_ + ' [ label="union" shape=diamond]\n'
        for step in self.steps:
            res = res + step.visualize()
            res += self.begin_viz() + "->" + step.begin_viz() + "\n"
            res += step.end_viz() + "->" + self.end_viz() + "\n"
        res += "\n}\n"
        return res

    def end_viz(self):
        return str(id(self)) + "2"


class Pass(PipelineStep):
    """
    
    """
    def __init__(self):
        super().__init__("pass")

    def process(self, data, head=Head()):
        # We do not need to create a new head, if we are in a downstream pipeline.
        return data, head