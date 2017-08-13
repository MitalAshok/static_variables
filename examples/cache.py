from static_variables import resolve_static

@resolve_static
def f(value):
    cache = static({})
    try:
        return cache[value]
    except KeyError:
        cache[value] = ret = function(value)
        return ret
