import os
import unittest
import pandas

from dataloader.dataloader import DataLoader
import gc


class TestDataLoader(unittest.TestCase):
    def test_creation_wrong_path(self):
        cache_env = os.environ["RECIPE_DATASET_PATH"]
        os.environ["RECIPE_DATASET_PATH"] = "/dev/null"
        with self.assertRaises(NotADirectoryError) as ctx:
            DataLoader()
        self.assertTrue("not a Directory" in str(ctx.exception))
        os.environ["RECIPE_DATASET_PATH"] = cache_env

    def dataset_interface(self, dataset_name):
        dataset = DataLoader()[dataset_name]

        needed_cols = set(["ingredients", "steps", "name"]) - set(exclude)
        self.assertTrue(set(needed_cols) <= set(dataset.columns))

        self.assertTrue(isinstance(dataset["steps"], pandas.Series),
                        dataset_name)
        self.assertTrue(isinstance(dataset["steps"][0], list), dataset_name)
        self.assertTrue(isinstance(dataset["steps"][0][0], str), dataset_name)

        self.assertTrue(isinstance(dataset["name"], pandas.Series),
                        dataset_name)
        self.assertTrue(isinstance(dataset["name"][0], str), dataset_name)

    def test_datasets_eight(self):
        self.dataset_interface("eightportions")

    def test_datasets_epi(self):
        self.dataset_interface("epirecipes")

    def test_datasets_food(self):
        self.dataset_interface("food-com")

    def test_datasets_lg(self):
        self.dataset_interface("recipenlg")

    def test_datasets_1m(self):
        self.dataset_interface("recipes1m")

    def test_datasets_1mnut(self):
        self.dataset_interface("recipes1m-nutritional")

    def test_datasets_whats(self):
        self.dataset_interface("whats-cooking")