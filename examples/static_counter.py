import threading

from static_variables import resolve_static


@resolve_static(static_variables={'counter': -1})
def global_thread_safe_counter():
    with static(threading.Lock()):
        counter += 1
    return counter
