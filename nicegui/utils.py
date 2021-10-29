import asyncio
import traceback


class EventArguments:

    def __init__(self, sender, **kwargs):
        self.sender = sender
        for key, value in kwargs.items():
            setattr(self, key, value)

        if hasattr(self, 'key_data'):
            self.action = KeyboardAction(self.key_data)
            self.key = KeyboardKey(self.key_data)
            self.modifiers = KeyboardModifiers(self.key_data)


class KeyboardAction:

    def __init__(self, key_data):
        self.action = getattr(key_data, 'action', False)

    @property
    def keydown(self):
        return self.action and self.action == 'keydown'

    @property
    def keyup(self):
        return self.action and self.action == 'keyup'

    @property
    def keypress(self):
        return self.action and self.action == 'keypress'


class KeyboardKey:
    def __init__(self, key_data):
        self.key = getattr(key_data, 'key', False)
        self.keycode = getattr(key_data, 'code', '')
        self.repeat = getattr(key_data, 'repeat', False)

    def __eq__(self, other):
        return self.key == other

    def __repr__(self):
        return str(self.key)

    def __int__(self):
        return int(self.key)

    @property
    def code(self):
        return self.keycode

    @property
    def left(self):
        return self.key and self.key == 'ArrowLeft'

    @property
    def right(self):
        return self.key and self.key == 'ArrowRight'

    @property
    def up(self):
        return self.key and self.key == 'ArrowUp'

    @property
    def down(self):
        return self.key and self.key == 'ArrowDown'

    @property
    def shift(self):
        return self.key and self.key == 'Shift'

    @property
    def is_cursorkey(self):
        return self.key and (self.left or self.right or self.up or self.down)

    # Number key codes
    number_key_codes = {f'Digit{number}': number for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}

    @property
    def numberkey(self):
        """Returns number of a key as a string based on the key code, meaning ignoring modifiers."""
        return self.number_key_codes.get(self.keycode)


class KeyboardModifiers:
    def __init__(self, key_data):
        self.key_data = key_data

    @property
    def altkey(self):
        return getattr(self.key_data, 'shiftKey', False)

    @property
    def ctrlkey(self):
        return getattr(self.key_data, 'ctrlKey', False)

    @property
    def shiftkey(self):
        return getattr(self.key_data, 'shiftKey', False)

    @property
    def metakey(self):
        return getattr(self.key_data, 'metaKey', False)


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


def handle_awaitable(func):
    async def inner_function(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return inner_function


def async_provide_arguments(func, update_function, *keys):
    def inner_function(sender, event):
        async def execute_function():
            try:
                await func()
            except TypeError:
                await func(EventArguments(sender, **{key: event[key] for key in keys}))

            await update_function()

        asyncio.get_event_loop().create_task(execute_function())

    return inner_function
