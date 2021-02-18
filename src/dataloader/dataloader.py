"""
Module to abstract away the diffrent types of datasets and how they have to be loaded
"""
from os.path import join, isdir
import os
import ast
import pandas as pd


class DataLoader:
    """
    Class that handels the loading of datasets from raw data (json/csv) and returns pandas dataframes with a specific interface that allows easy accessibility.
    The datasets are expected to be layed out like this:
    $RECIPE_DATASET_PATH
    ├── eightportions
    │   └── ...
    ├── epirecipes
    │   └── ...
    ├── food-com
    │   └── ...
    ├── recipe1m
    │   └── ...
    └── recipenlg
        └── full_dataset.csv
    """

    # Dataset Names as constants
    EIGHT_PORTIONS = "eightportions"
    EPIRECIPES = "epirecipes"
    FOOD_COM = "food-com"
    RECIPENLG = "recipenlg"
    RECIPES1M = "recipes1m"
    RECIPES1M_NUTRITIONAL = "recipes1m-nutritional"
    WHATS_COOKING = "whats-cooking"

    This is the DataLoader Class which abstracts away the access and norming of
    our datasets.

    
    def __init__(self,
                 pickle_path="__pickle__",
                 dataframe_path=os.environ.get('RECIPE_DATASET_PATH',
                                               '../../datasets')):
        """
        Args:
            pickle_path: Optional; name of the folder where the pickle files are saved
            dataframe_path: Optional; place where the datasets are stored

        Raises:
            NotADirectoryError: the provided dataframe_path is not a dir
        """
        self.dataframe_path = dataframe_path
        if not isdir(self.dataframe_path):
            raise NotADirectoryError(
                f"Given Path '{self.dataframe_path}' in 'RECIPE_DATASET_PATH' is not a Directory"
            )

        self.pickle_path = join(self.dataframe_path, pickle_path)
        if not isdir(self.pickle_path):
            print(f"Creating the {self.pickle_path} for you!")
            os.mkdir(self.pickle_path)

        self.dataset_loaders = {
            self.EIGHT_PORTIONS: self.__load_eightportions,
            self.EPIRECIPES: self.__load_epirecipes,
            self.FOOD_COM: self.__load_food_com,
            self.RECIPENLG: self.__load_recipenlg,
            self.RECIPES1M: self.__load_recipi1m,
            self.RECIPES1M_NUTRITIONAL: self.__load_recipi1m_nutritional,
            self.WHATS_COOKING: self.__load_whats_cooking,
        }
        self.datasets = self.dataset_loaders.keys()

    def __getitem__(self, key):
        """
        Loads a pandas dataframe from a single dataset or pickle file if
        present
        if not already existent creates a pickle file for the dataset

        Args:
            key: A string-like object, key must be in self.dataset_loaders

        Returns:
            A pandas dataframe with normed names for the relevant columns

        Raises:
            NotImplementedError: When no loader is found for the key
        """
        if key not in self.dataset_loaders.keys():
            raise NotImplementedError(
                f"'{key}' is not a valid dataset! Possible are {list(self.dataset_loaders.keys())}!"
            )

        dataframe = self.dataset_loaders[key]()
        return dataframe

    def __load_recipi1m(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "recipe1m/layer1.json"))

        dataframe = dataframe.rename(columns={
            "instructions": "steps",
            "title": "name"
        })

        rm_dict = lambda x: [el["text"] for el in x]
        dataframe["ingredients"] = dataframe["ingredients"].apply(rm_dict)
        dataframe["steps"] = dataframe["steps"].apply(rm_dict)

        return dataframe

    def __load_recipi1m_nutritional(self):
        dataframe = pd.read_json(
            join(self.dataframe_path,
                 "recipe1m/recipes_with_nutritional_info.json"))

        dataframe = dataframe.rename(columns={
            "instructions": "steps",
            "title": "name"
        })

        rm_dict = lambda x: [el["text"] for el in x]
        dataframe["ingredients"] = dataframe["ingredients"].apply(rm_dict)
        dataframe["steps"] = dataframe["steps"].apply(rm_dict)

        return dataframe

    def __load_epirecipes(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "epirecipes/full_format_recipes.json"))
        dataframe = dataframe.rename(columns={
            "directions": "steps",
            "title": "name"
        })
        return dataframe

    def __load_food_com(self):
        dataframe = pd.read_csv(
            join(self.dataframe_path, "food-com/RAW_recipes.csv"))

        dataframe["ingredients"] = dataframe["ingredients"].apply(
            ast.literal_eval)
        dataframe["steps"] = dataframe["steps"].apply(ast.literal_eval)
        return dataframe

    def __load_recipenlg(self):
        dataframe = pd.read_csv(join(self.dataframe_path,
                                     "recipenlg/full_dataset.csv"),
                                engine="python")

        dataframe = dataframe.rename(columns={
            "directions": "steps",
            "title": "name"
        })

        dataframe["ingredients"] = dataframe["ingredients"].apply(
            ast.literal_eval)

        dataframe["steps"] = dataframe["steps"].apply(ast.literal_eval)
        return dataframe

    def __load_whats_cooking(self):
        dataframe = pd.read_json(
            join(self.dataframe_path, "whats-cooking/train.json"))
        dataframe = dataframe.rename(columns={"id": "name"})

        dataframe["name"] = dataframe["name"].apply(str)
        return dataframe

    def __load_eightportions(self):
        dataframe = pd.read_json(
            join(self.dataframe_path,
                 "eightportions/recipes_raw_nosource_ar.json"), "index")
        dataframe = dataframe.rename(columns={
            "instructions": "steps",
            "title": "name"
        })
        dataframe["steps"] = dataframe["steps"].str.split(".")
        return dataframe

    def get_multiple(self, keys):
        """
        Loads a pandas dataframe from multiple datasets of pickle file if
        present
        if not already existent creates a pickle file for the dataset
        combination
        """
        dataframe = pd.DataFrame()
        for key in keys:
            dataframe = dataframe.append(self[key])

        return dataframe


def main():
    d = DataLoader()
    for i in d["recipes1m"]["ingredients"].head():

        # i = ast.literal_eval(i)
        print(type(i), i)
        # print(type(i), json.loads(i))


if __name__ == "__main__":
    main()
