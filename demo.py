from dataclasses import dataclass

from nicegui import ui
from nicegui.elements.choice_element import Option
from nicegui.elements.select import Select


@dataclass
class Person(Option[str, int]):
    """A person option, containing everything that's needed to render the option."""
    icon: str
    caption: str


def new_val_to_option(s: Select[Person], v: str) -> Person | None:
    """
    Turns a string provided to the input into a Person option. This function can return None if the 
    option isn't valid, causing no option to be added.
    """
    for o in s.options:
        if o.label == v:
            return o
    return Person(label=v, value=len(s.options), icon="person-outline", caption="")


if __name__ in {"__main__", "__mp_main__"}:

    @ui.page("/")
    def page():

        options = [ui.option(v, v) for v in ("a", "b", "c")]
        ui.select(
            options,
            new_value_mode="toggle",
            new_val_to_option=lambda _, v: ui.option(label=v, value=v),
            multiple=True
        ).props("use-chips")
        o = [ui.as_option("A"), ui.as_option("B")]
        ui.toggle(o, value=(ui.as_option("A"),), on_change=lambda e: print(e.value, e.previous_value))
            

    ui.run()
