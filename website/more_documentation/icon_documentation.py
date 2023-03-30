from nicegui import ui
from website.documentation_tools import text_demo


def main_demo() -> None:
    ui.icon('thumb_up')


def more() -> None:
    ui.add_head_html('<script src="https://unpkg.com/eva-icons"></script>')

    @text_demo('Eva icons', '''
        You can use [Eva icons](https://akveo.github.io/eva-icons/#/) in your app.
    ''')
    async def eva_icons():
        from nicegui import Client

        # @ui.page('/')
        # async def main(client: Client):
        #     ui.add_head_html('<script src="https://unpkg.com/eva-icons"></script>')
        #     ui.element('i').props('data-eva="github"')
        #     await client.connected()
        #     await ui.run_javascript('eva.replace();', respond=False)
        # END OF DEMO
        ui.element('i').props('data-eva="github"')
        await ui.run_javascript('eva.replace();', respond=False)
