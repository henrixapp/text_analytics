from pipeline.pipeline import PipelineStep, Head
import pandas as pd


class Dropper(PipelineStep):
    """
    drops data in a dataframe, if they are none for given columns.
    """
    def __init__(self, columns_causing_drop=[], inplace=True):
        super().__init__("dropper_")
        self._columns = columns_causing_drop
        assert hasattr(self._columns,
                       "__iter__"), "columns_causing_drop must be iterable!"
        self._inplace = inplace

    def process(self, data, head=Head()):
        assert isinstance(data, pd.DataFrame)
        head.addInfo(self.name, "-".join(self._columns))
        data.dropna(subset=self._columns, inplace=self._inplace)
        return data, head
