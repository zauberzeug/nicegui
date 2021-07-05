import traceback

class EventArguments:

    def __init__(self, sender, **kwargs):

        self.sender = sender
        for key, value in kwargs.items():
            setattr(self, key, value)

def provide_arguments(func, *keys):
    def inner_function(sender, event):
        try:
            return func()
        except TypeError:
            return func(EventArguments(sender, **{key: event[key] for key in keys}))
    return inner_function

def handle_exceptions(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
    return inner_function
