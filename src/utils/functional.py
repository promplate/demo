def compose(f1, f2):
    return lambda *args, **kwargs: f2(f1(*args, **kwargs))
