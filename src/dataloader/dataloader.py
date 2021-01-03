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

        self.dataset_loaders = {
            "eightportions": self.__load_eightportions,
            "epirecipes": self.__load_epirecipes,
            "food-com": self.__load_food_com,
            "recipenlg": self.__load_recipenlg,
            "recipes1m": self.__load_recipi1m,
            "recipes1m-nutritional": self.__load_recipi1m_nutritional,
            "whats-cooking": self.__load_whats_cooking,
        }

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
        if key not in self.dataset_loaders.keys():
            raise NotImplementedError(
                f"'{key}' is not a valid dataset! Possible are {self.dataset_loaders.keys()}"
            )

        return self.dataset_loaders[key]()

    def __load_recipi1m(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "recipe1m/layer1.json"))
        return dataframe

    def __load_recipi1m_nutritional(self):
        dataframe = pd.read_json(
            join(self.dataframe_path,
                 "recipe1m/recipes_with_nutritional_info.json"))
        return dataframe

    def __load_epirecipes(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "epirecipes/full_format_recipes.json"))
        return dataframe

    def __load_food_com(self):
        dataframe = pd.read_csv(
            join(self.dataframe_path, "food-com/RAW_recipes.csv"))
        return dataframe

    def __load_recipenlg(self):
        dataframe = pd.read_csv(join(self.dataframe_path,
                                     "recipenlg/full_dataset.csv"),
                                index_col=0)
        return dataframe

    def __load_whats_cooking(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "whats-cooking/train.json"))
        return dataframe

    def __load_eightportions(self):
        dataframe = pd.read_json(
            join(self.dataframe_path,
                 "eightportions/recipes_raw_nosource_ar.json"), "index")
        return dataframe

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
