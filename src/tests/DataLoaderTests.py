import pytest
import os
import unittest
from dataloader.dataloader import DataLoader


class TestDataLoader(unittest.TestCase):
    def test_creation_wrong_path(self):
        os.environ["RECIPE_DATASET_PATH"] = "/dev/null"
        with self.assertRaises(NotADirectoryError) as ctx:
            DataLoader()
        self.assertTrue("not a Directory" in str(ctx.exception))
