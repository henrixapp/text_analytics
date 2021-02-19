from pipeline.pipeline import Head, PipelineStep
from dataloader.dataloader import DataLoader
import json
import pickle


class DataSetSource(PipelineStep):
    """
    Accesses the given datasets and returns a pandas dataframe
    """
    def __init__(self, datasets=[]):
        super().__init__("Source" + "_".join(datasets))
        self._datasets = datasets

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        loader = DataLoader()
        dataset = loader.get_multiple(self._datasets)
        return dataset, head


class JSONSink(PipelineStep):
    """
    Dumps current data into a json file.
    """
    def __init__(self, filename):
        super().__init__("TOJSON")
        self._filename = filename

    def process(self, data, head=Head()):
        head.addInfo(self.name, self._filename)
        with open(self._filename, 'w') as outfile:
            json.dump(data, outfile)
        return data, head


class PDReduce(PipelineStep):
    """
    Accesses the given field(s) of a pandas dataframe.
    """
    def __init__(self, field):
        super().__init__("PDReduce")
        self._field = field

    def process(self, data, head=Head()):
        head.addInfo(self.name, self._field)
        return data[self._field], head


class PickleDump(PipelineStep):
    """
    Saves the data under the given filename
    Returns the data
    """
    def __init__(self, filename):
        super().__init__("PickleDump")
        self.filename = filename

    def process(self, data, head=Head()):
        head.addInfo(self.name, self.filename)
        pickle.dump(data, open(self.filename, "wb"))
        return data, head


class PickleLoad(PipelineStep):
    """
    Loads the data under the given filename
    Returns the data
    """
    def __init__(self, filename):
        super().__init__("PickleLoad")
        self.filename = filename

    def process(self, data, head=Head()):
        head.addInfo(self.name, self.filename)
        data = pickle.load(open(self.filename, "rb"))
        return data, head