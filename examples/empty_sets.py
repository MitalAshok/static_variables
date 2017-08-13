from static_variables import resolve_static


@resolve_static(empty_set_literal=True)
def f(value):
    my_set = static({})
    my_set.add(value)
    return my_set


@resolve_static
def g(value):
    my_dict = {}
    my_set = static(EMPTY_SET)
    my_dict['value'] = my_set
    return my_dict
