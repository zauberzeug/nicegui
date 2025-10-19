from nicegui import ui
from zen_api import quote_generator


#helper function to call on next quote button
def show_new_quote():
    quote_label.text = f'“{quote_generator()}”'


with ui.card().classes(
    'max-w-md mx-auto mt-20 p-6 bg-white rounded-2xl shadow-lg border border-gray-100 flex flex-col items-center'
):
    with ui.card_section():
        quote_label = ui.label(f'“{quote_generator()}”').classes(
            'text-gray-700 italic text-lg leading-relaxed text-center font-serif'
        )

    ui.button(
        'Next Quote',
        on_click=show_new_quote,
    ).classes(
        'mt-6 bg-gray-800 hover:bg-gray-900 text-white text-sm font-medium '
        'px-4 py-2 rounded-xl shadow-md transition duration-200'
    )

ui.run()
