Run any python code. If user queries questions about code, or his/her requests can be done with coding, you can actually run some code with me.

There is only 1 parameters:

- `code: str`: the python code to `exec()`

For example, if you want to calculate 0.409 \* 2023, you can make a call like this:

```json
{
  "name": "python",
  "body": {
    "code": "out = 0.409 * 2023"
  }
}
```

And I will return:

```json
{
  "out": "827.4069999999999"
}
```

This tool is basically implemented like this:

```py
def python(code: str) -> dict[str, str]:
    exec(code, namespace := {})
    return {k, repr(v) for k, v in namespace.items()}
```

You must assign values to variables, and I can just return the values that is defined in the namespace.

Notes:
If your scripts fail, exceptions will be returned to you. You can attempt another approach accordingly.
This is a synchronous code interpreter, so you can't use `await` inside.
The syntax and variables you can use is not restricted, so DO NOT make dangerous calls.
