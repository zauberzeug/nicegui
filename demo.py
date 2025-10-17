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
        ui.add_head_html('<script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>')
        ui.add_head_html('<script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>')
        # ^ NOTE: scripts are added for custom icons

        select_people = (
            ui.select(
                options=[
                    Person(label="Joe", value=0, icon="person-outline", caption="Company: Trilliant Health"),
                    Person(label="Falko", value=1, icon="person-outline", caption="Company: Trilliant Health"),
                    Person(label="Zauberzeug", value=2, icon="people-outline", caption="Company"),
                ],
                multiple=True,
                on_change=lambda e: print(f"the values are: {e.value}"),
                # ^ NOTE: the type of e.value is tuple[Person, ...]
                new_value_mode="toggle",
                new_val_to_option=new_val_to_option,
            )
            .props("use-chips")
            .classes("w-64")
        )
        select_people.add_slot(
            "option",
            r'''
            <q-item
                v-bind="props.itemProps"
            >
                <q-item-section avatar>
                    <ion-icon :name="props.opt.icon" style="display: inherit !important;"></ion-icon>
                </q-item-section>
                <q-item-section>
                    <q-item-label>{{ props.opt.label }}</q-item-label>
                    <q-item-label caption>{{ props.opt.caption }}</q-item-label>
                </q-item-section>
            </q-item>
            '''
        )
        # ^ NOTE: since the we're letting the user's define the options and passing those to the component, they
        #       can easily access the values in custom Vue slots.

        s = ui.select(
            options=[ui.as_option(v) for v in ('a', 'b', 'c')],
            multiple=True,
            new_value_mode="toggle",
            new_val_to_option=lambda _, v: ui.as_option(v),
        )
        ui.label().bind_text_from(s, 'value', lambda v: f'value = {tuple(sorted(o.value for o in v))}')
        ui.label().bind_text_from(s, 'options', lambda v: f'options = {tuple(sorted(o.value for o in v))}')

        t = ui.toggle[Option[str, str]]([ui.as_option("A"), ui.as_option("B")], value=(ui.as_option("A"),))
        t.value
            

    ui.run()
