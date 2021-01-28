import os
import unittest
import pandas

from dataloader.dataloader import DataLoader


def error_string(dataset_name, type_name, col):
    return f"dataset '{dataset_name}' wrong type '{type_name}' in {col}"


class TestDataLoader(unittest.TestCase):
    def test_creation_wrong_path(self):
        cache_env = os.environ["RECIPE_DATASET_PATH"]
        os.environ["RECIPE_DATASET_PATH"] = "/dev/null"
        with self.assertRaises(NotADirectoryError) as ctx:
            DataLoader()
        self.assertTrue("not a Directory" in str(ctx.exception))
        os.environ["RECIPE_DATASET_PATH"] = cache_env

    def dataset_interface(self, dataset_name, exclude=[]):
        dataset = DataLoader()[dataset_name]

        needed_cols = set(["ingredients", "steps", "name"]) - set(exclude)
        self.assertTrue(set(needed_cols) <= set(dataset.columns))

        if "ingredients" not in exclude:
            self.assertTrue(
                isinstance(dataset["ingredients"], pandas.Series),
                error_string(dataset_name, type(dataset["ingredients"]),
                             'dataset["ingredients"]'))
            self.assertTrue(
                isinstance(dataset["ingredients"][0], list),
                error_string(dataset_name, type(dataset["ingredients"][0]),
                             'dataset["ingredients"][0]'))
            self.assertTrue(
                isinstance(dataset["ingredients"][0][0], str),
                error_string(dataset_name, type(dataset["ingredients"][0][0]),
                             'dataset["ingredients"][0][0]'))

        if "steps" not in exclude:
            self.assertTrue(
                isinstance(dataset["steps"], pandas.Series),
                error_string(dataset_name, type(dataset["steps"]),
                             'dataset["steps"]'))
            self.assertTrue(
                isinstance(dataset["steps"][0], list),
                error_string(dataset_name, type(dataset["steps"][0]),
                             'dataset["steps"][0]'))
            self.assertTrue(
                isinstance(dataset["steps"][0][0], str),
                error_string(dataset_name, type(dataset["steps"][0][0]),
                             'dataset["steps"][0][0]'))

        if "name" not in exclude:
            self.assertTrue(
                isinstance(dataset["name"], pandas.Series),
                error_string(dataset_name, type(dataset["name"]),
                             'dataset["name"]'))
            self.assertTrue(
                isinstance(dataset["name"][0], str),
                error_string(dataset_name, type(dataset["name"][0]),
                             'dataset["name"][0]'))

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
        self.dataset_interface("whats-cooking", exclude=["steps"])


def main():
    recipenlg = DataLoader()["recipenlg"]
    print(type(recipenlg["ingredients"][0]), recipenlg["ingredients"][0])


if __name__ == "__main__":
    main()
