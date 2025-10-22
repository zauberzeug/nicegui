from dataclasses import dataclass

from nicegui import ui
from nicegui.elements.select import Option


@dataclass
class Person(Option[str, int]):
    """A person option, containing everything that's needed to render the option."""
    icon: str
    caption: str


if __name__ in {'__main__', '__mp_main__'}:

    @ui.page('/')
    def page():
        s = ui.select(
            options=[1,2,3],
            value=None,
            on_change=lambda e: print(e.value, e.previous_value),
        )
        s.value

        s2 = ui.select(
            options=[1,2,3],
            value=(1,),
            on_change=lambda e: print(e.value, e.previous_value),
        )
        s2.value

        select_people = (
            ui.select(
                options=[
                    Person(label='Joe', value=0, icon='person-outline', caption='Company: Trilliant Health'),
                    Person(label='Falko', value=1, icon='person-outline', caption='Company: Trilliant Health'),
                    Person(label='Zauberzeug', value=2, icon='people-outline', caption='Company'),
                ],
                on_change=lambda e: print(e.value),
                value=(),
            )
            .props('use-chips')
            .classes('w-64')
        )
        select_people.add_slot(
            'option',
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


    ui.run()
