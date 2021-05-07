import traceback

def provide_sender(func, sender):
    def inner_function(*args, **kwargs):
        try:
            func()
        except TypeError:
            func(sender)
    return inner_function

def handle_exceptions(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
    return inner_function

