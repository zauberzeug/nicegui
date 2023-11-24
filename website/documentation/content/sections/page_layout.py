from nicegui import ui

from ...model import SectionDocumentation
from ...more.card_documentation import CardDocumentation
from ...more.carousel_documentation import CarouselDocumentation
from ...more.column_documentation import ColumnDocumentation
from ...more.context_menu_documentation import ContextMenuDocumentation
from ...more.dialog_documentation import DialogDocumentation
from ...more.expansion_documentation import ExpansionDocumentation
from ...more.grid_documentation import GridDocumentation
from ...more.menu_documentation import MenuDocumentation
from ...more.notify_documentation import NotifyDocumentation
from ...more.pagination_documentation import PaginationDocumentation
from ...more.row_documentation import RowDocumentation
from ...more.scroll_area_documentation import ScrollAreaDocumentation
from ...more.separator_documentation import SeparatorDocumentation
from ...more.splitter_documentation import SplitterDocumentation
from ...more.stepper_documentation import StepperDocumentation
from ...more.tabs_documentation import TabsDocumentation
from ...more.timeline_documentation import TimelineDocumentation


class PageLayoutDocumentation(SectionDocumentation, title='Page *Layout*', name='page_layout'):

    def content(self) -> None:
        @self.add_markdown_demo('Auto-context', '''
            In order to allow writing intuitive UI descriptions, NiceGUI automatically tracks the context in which elements are created.
            This means that there is no explicit `parent` parameter.
            Instead the parent context is defined using a `with` statement.
            It is also passed to event handlers and timers.

            In the demo, the label "Card content" is added to the card.
            And because the `ui.button` is also added to the card, the label "Click!" will also be created in this context.
            The label "Tick!", which is added once after one second, is also added to the card.

            This design decision allows for easily creating modular components that keep working after moving them around in the UI.
            For example, you can move label and button somewhere else, maybe wrap them in another container, and the code will still work.
        ''')
        def auto_context_demo():
            with ui.card():
                ui.label('Card content')
                ui.button('Add label', on_click=lambda: ui.label('Click!'))
                ui.timer(1.0, lambda: ui.label('Tick!'), once=True)

        self.add_element_intro(CardDocumentation())
        self.add_element_intro(ColumnDocumentation())
        self.add_element_intro(RowDocumentation())
        self.add_element_intro(GridDocumentation())

        @self.add_markdown_demo('Clear Containers', '''
            To remove all elements from a row, column or card container, use can call
            ```py
            container.clear()
            ```

            Alternatively, you can remove individual elements by calling
            
            - `container.remove(element: Element)`,
            - `container.remove(index: int)`, or
            - `element.delete()`.
        ''')
        def clear_containers_demo():
            container = ui.row()

            def add_face():
                with container:
                    ui.icon('face')
            add_face()

            ui.button('Add', on_click=add_face)
            ui.button('Remove', on_click=lambda: container.remove(0) if list(container) else None)
            ui.button('Clear', on_click=container.clear)

        self.add_element_intro(ExpansionDocumentation())
        self.add_element_intro(ScrollAreaDocumentation())
        self.add_element_intro(SeparatorDocumentation())
        self.add_element_intro(SplitterDocumentation())
        self.add_element_intro(TabsDocumentation())
        self.add_element_intro(StepperDocumentation())
        self.add_element_intro(TimelineDocumentation())
        self.add_element_intro(CarouselDocumentation())
        self.add_element_intro(PaginationDocumentation())
        self.add_element_intro(MenuDocumentation())
        self.add_element_intro(ContextMenuDocumentation())

        @self.add_markdown_demo('Tooltips', '''
            Simply call the `tooltip(text:str)` method on UI elements to provide a tooltip.

            For more artistic control you can nest tooltip elements and apply props, classes and styles.
        ''')
        def tooltips_demo():
            ui.label('Tooltips...').tooltip('...are shown on mouse over')
            with ui.button(icon='thumb_up'):
                ui.tooltip('I like this').classes('bg-green')

        self.add_element_intro(NotifyDocumentation())
        self.add_element_intro(DialogDocumentation())
