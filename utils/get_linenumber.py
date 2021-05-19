from inspect import currentframe


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno
