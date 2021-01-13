from pipeline.pipeline import Head, PipelineStep
from dataloader.dataloader import DataLoader
import json


class DataSetSource(PipelineStep):
    def __init__(self, datasets=[]):
        super().__init__("Source" + "_".join(datasets))
        self._datasets = datasets

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        dl = DataLoader()
        ds = dl.getMultiple(self._datasets)
        return ds, head


class JSONSink(PipelineStep):
    def __init__(self, filename):
        super().__init__("TOJSON")
        self._filename = filename

    def process(self, data, head=Head()):
        head.addInfo(self.name, self._filename)
        with open(self._filename, 'w') as outfile:
            json.dump(data, outfile)
        return data, head


class PDReduce(PipelineStep):
    def __init__(self, field):
        super().__init__("PDReduce")
        self._field = field

    def process(self, data, head=Head()):
        head.addInfo(self.name, self._field)
        return data[self._field], head
