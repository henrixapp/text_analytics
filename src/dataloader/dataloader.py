"""
Module to abstract away the diffrent types of datasets and how they have to be loaded
"""
from os.path import join, isdir
import os
import pandas as pd


class DataLoader:
    """description"""
    def __init__(self, pickle_path="__pickle__"):
        self.dataframe_path = os.environ.get('RECIPE_DATASET_PATH',
                                             "../../datasets")
        if not isdir(self.dataframe_path):
            raise NotADirectoryError(
                f"Given Path '{self.dataframe_path}' in 'RECIPE_DATASET_PATH' is not a Directory"
            )

        self.pickle_path = join(self.dataframe_path, pickle_path)
        if not isdir(self.pickle_path):
            print(f"Creating the {self.pickle_path=} for you!")
            os.mkdir(self.pickle_path)

        self.implemented_datasets = [
            "epirecipes", "recipes1m", "food-com", "recipenlg", "whats-cooking"
        ]

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
        if key not in self.implemented_datasets:
            raise NotImplementedError(
                f"'{key}' is not a valid dataset! Possible are {self.implemented_datasets}"
            )

        df = ""
        if key == "recipi1m":
            df = pd.read_json(join(self.dataframe_path,
                                   "recipe1m/layer1.json"))
        elif key == "recipi1m_nutritional":
            df = pd.read_json(
                join(self.dataframe_path,
                     "recipe1m/recipes_with_nutritional_info.json"))
        elif key == "epirecipes":
            df = pd.read_json(
                join(self.dataframe_path,
                     "epirecipes/full_format_recipes.json"))
        elif key == "food-com":
            df = pd.read_csv(
                join(self.dataframe_path, "food-com/RAW_recipes.csv"))
        elif key == "recipenlg":
            df = pd.read_csv(join(self.dataframe_path,
                                  "recipenlg/full_dataset.csv"),
                             index_col=0)
        elif key == "whats-cooking":
            df = pd.read_json(
                join(self.dataframe_path, "whats-cooking/train.json"))
        elif key == "eigntportions":
            df = pd.read_json(
                join(self.dataframe_path,
                     "eightportions/recipes_raw_nosource_ar.json"), "index")

        return df

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
    print(d["epirecipes"].head())
    print(d.__dict__)


if __name__ == "__main__":
    main()
