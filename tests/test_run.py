import unittest.mock

import pytest

from src.routes.run import Model


def test_model_class():
    # Create an instance of the Model class with the new model option
    model_instance = Model("gpt-4-1106-preview")

    # Assert that the instance behaves as expected
    assert model_instance.model == "gpt-4-1106-preview"
