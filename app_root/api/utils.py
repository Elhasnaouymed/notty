from flask_restx import marshal_with


def marshal_return(r, fields: dict):
    """
    Instead of using marshal_with as a decorator on your resource endpoints,
    you can use this on the return statement (more control of what you want to return)
    """
    return marshal_with(fields)(lambda: r)()
