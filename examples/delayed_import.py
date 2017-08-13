from static_variables import resolve_static


@resolve_static(static_variables={'expensive_module': None})
def f(value):
    if expensive_module is None:
        import expensive_module

    return expensive_module.function(value)
