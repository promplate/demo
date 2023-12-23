from traceback import print_exc
from typing import Any

from fastapi.concurrency import run_in_threadpool
from rich import print

from ...utils.load import load_template
from .base import AbstractTool


class CodeInterpreter(AbstractTool):
    """
    The CodeInterpreter class inherits from AbstractTool and implements
    methods for evaluating Python code within a specified namespace.

    Methods:
    - eval: A static method that evaluates given Python code and returns a
      dictionary of the local namespace with variable representations.
    - __call__: An async method that runs the eval method in a threadpool and
      handles any exceptions that occur during execution.
    """
    __doc__ = load_template("schema/code_interpreter").text

    name = "python"

    @staticmethod
    def eval(code: str):
        """
        Evaluate the given code string as Python code and return a dictionary
        representing the local namespace with variable names as keys and their
        string representations as values, excluding private variables (those
        starting with an underscore).

        Args:
            code (str): The Python code to evaluate.
        Returns:
            dict[str, str]: A dictionary with variable names and their
            string representations.
        """
        print(code)
        code = load_template("python").render({"code": code})
        namespace: dict[str, Any] = {}
        exec(code, namespace)
        return {k: repr(v) for k, v in namespace.items() if not k.startswith("_")}

    async def __call__(self, code: str):  # type: ignore
        """
        Asynchronously evaluate the given code string as Python code using
        the eval method. If an exception occurs during evaluation, it is
        caught and the exception's class and message are returned as a string.

        Args:
            code (str): The Python code to evaluate.
        Returns:
            Union[dict[str, str], str]: A dictionary with variable names and
            their string representations if successful, or an error string.
        """
        try:
            return await run_in_threadpool(self.eval, code)
        except Exception as e:
            print_exc()
            return f"{e.__class__.__qualname__}: {e}"
