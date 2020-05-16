from flask import request


def get_query_string():
    """
    封装获得查询字符串的方法，以方便进行重定向。
    从而不必每个视图函数中都去写这些代码。使代码更精简。
    :return:
    """
    args = request.args.to_dict()
    query_string = '?'
    for key, value in args.items():
        query_string = query_string + "{key}={value}&".format(key=key, value=value)
    return query_string
