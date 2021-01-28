import os
import unittest
import pandas

from dataloader.dataloader import DataLoader


class TestDataLoader(unittest.TestCase):
    def test_creation_wrong_path(self):
        cache_env = os.environ["RECIPE_DATASET_PATH"]
        os.environ["RECIPE_DATASET_PATH"] = "/dev/null"
        with self.assertRaises(NotADirectoryError) as ctx:
            DataLoader()
        self.assertTrue("not a Directory" in str(ctx.exception))
        os.environ["RECIPE_DATASET_PATH"] = cache_env

    def test_dataset_interface(self):
        dataloader = DataLoader()
        for dataset_name in dataloader.datasets:
            dataset = dataloader[dataset_name]

            self.assertTrue(isinstance(dataset["ingredients"], pandas.Series),
                            dataset_name)
            self.assertTrue(isinstance(dataset["ingredients"].dtype, list),
                            dataset_name)
            self.assertTrue(isinstance(dataset["ingredients"][0][0], str),
                            dataset_name)

            self.assertTrue(isinstance(dataset["steps"], pandas.Series),
                            dataset_name)
            self.assertTrue(isinstance(dataset["steps"].dtype, list),
                            dataset_name)
            self.assertTrue(isinstance(dataset["steps"][0][0], str),
                            dataset_name)

            self.assertTrue(isinstance(dataset["name"], pandas.Series),
                            dataset_name)
            self.assertTrue(isinstance(dataset["name"].dtype, str),
                            dataset_name)
