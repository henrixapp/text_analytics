import os


class DataLoader:
    """description"""
    def __init__(self, pickle_path="__pickle__"):
        self.dataframe_path = os.environ.get('RECIPE_DATASET_PATH',
                                             "../../datasets")
        if not os.path.isdir(self.dataframe_path):
            raise NotADirectoryError(
                f"Given Path '{self.dataframe_path}' in 'RECIPE_DATASET_PATH' is not a Directory"
            )

        self.pickle_path = os.path.join(self.dataframe_path, pickle_path)
        if not os.path.isdir(self.pickle_path):
            print(f"Creating the {self.pickle_path=} for you!")
            os.mkdir(self.pickle_path)

    def __normalize(self):
        """make the dataset conform to the schema"""
        pass

    def __checkSchema(self):
        """check whether the dataframe conforms the schema"""
        pass

    def __getitem__(self, key):
        """
        Loads a pandas dataframe from a single dataset or pickle file if
        present
        if not already existent creates a pickle file for the dataset
        """
        pass

    def getMultiple(self, keys):
        """
        Loads a pandas dataframe from multiple datasets of pickle file if
        present
        if not already existent creates a pickle file for the dataset
        combination
        """
        pass


def createDataLoaderPipelineStep(name, dataset_names):
    """create a pipline.PipelineStep for a given combination of datasets"""
    pass


def main():
    d = DataLoader()
    print(d.__dict__)


if __name__ == "__main__":
    main()
