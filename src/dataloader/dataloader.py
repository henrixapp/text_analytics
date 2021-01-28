"""
Module to abstract away the diffrent types of datasets and how they have to be loaded
"""
from os.path import join, isdir
import os
import pandas as pd
import faulthandler
import ast
import json


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
            print(f"Creating the {self.pickle_path} for you!")
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
        self.datasets = self.dataset_loaders.keys()

    def __getitem__(self, key):
        """
        Loads a pandas dataframe from a single dataset or pickle file if
        present
        if not already existent creates a pickle file for the dataset
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

    def getMultiple(self, keys):
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


def createDataLoaderPipelineStep(name, dataset_names):
    """create a pipline.PipelineStep for a given combination of datasets"""
    pass


def main():
    d = DataLoader()
    for i in d["recipes1m"]["ingredients"].head():

        # i = ast.literal_eval(i)
        print(type(i), i)
        # print(type(i), json.loads(i))


if __name__ == "__main__":
    main()
