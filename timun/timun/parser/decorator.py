def parser(name: str):
    def decorator(func):
        setattr(func, "__PARSER__", name)
        return func

    return decorator
