from traceback import print_exc
from typing import Any

from fastapi.concurrency import run_in_threadpool
from rich import print

from ...utils.load import load_template
from .base import AbstractTool


class CodeInterpreter(AbstractTool):
    __doc__ = load_template("schema/code_interpreter").text

    name = "python"

    @staticmethod
    def eval(code: str):
        print(code)
        code = load_template("python").render({"code": code})
        namespace: dict[str, Any] = {}
        exec(code, namespace)
        return {k: repr(v) for k, v in namespace.items() if not k.startswith("_")}

    async def __call__(self, code: str):  # type: ignore
        try:
            return await run_in_threadpool(self.eval, code)
        except Exception as e:
            print_exc()
            return f"{e.__class__.__qualname__}: {e}"
