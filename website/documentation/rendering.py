import asyncio
from typing import List

from fastapi import Request, Response

from nicegui import Client, app, ui
from nicegui.logging import log
from nicegui.page import page
from nicegui.storage import RequestTrackingMiddleware

from ..header import add_head_html, add_header
from ..style import section_heading, subheading
from .content import DocumentationPage, registry
from .custom_restructured_text import CustomRestructuredText as custom_restructured_text
from .demo import demo
from .reference import generate_class_doc
from .tree import nodes


def render_page(documentation: DocumentationPage, *, with_menu: bool = True) -> None:
    """Render the documentation."""

    # menu
    if with_menu:
        with ui.left_drawer() \
                .classes('column no-wrap gap-1 bg-[#eee] dark:bg-[#1b1b1b] mt-[-20px] px-8 py-20') \
                .style('height: calc(100% + 20px) !important') as menu:
            tree = ui.tree(nodes, label_key='title').classes('w-full').props('accordion no-connectors')
            tree.add_slot('default-header', '''
                <a :href="'/documentation/' + props.node.id" onclick="event.stopPropagation()">{{ props.node.title }}</a>
            ''')
            tree.expand(_ancestor_nodes(documentation.name))
            ui.run_javascript(f'''
                Array.from(getHtmlElement({tree.id}).getElementsByTagName("a"))
                    .find(el => el.innerText.trim() === "{(documentation.parts[0].title or '').replace('*', '')}")
                    .scrollIntoView({{block: "center"}});
            ''')
    else:
        menu = None

    # header
    add_head_html()
    add_header(menu)
    ui.add_css('html {scroll-behavior: auto}')
    title = (documentation.title or '').replace('*', '')
    ui.page_title('NiceGUI' if not title else title if title.split()[0] == 'NiceGUI' else f'{title} | NiceGUI')

    # content
    def render_content():
        section_heading(documentation.subtitle or '', documentation.heading)
        for part in documentation.parts:
            if part.title:
                if part.link_target:
                    ui.link_target(part.link_target)
                subheading(part.title, link=part.link, major=part.reference is not None)
            if part.description:
                if part.description_format == 'rst':
                    element = custom_restructured_text(part.description.replace(':param ', ':'))
                else:
                    element = ui.markdown(part.description)
                element.classes('bold-links arrow-links')
                if ':param' in part.description:
                    element.classes('rst-param-tables')
            if part.ui:
                part.ui()
            if part.demo:
                demo(part.demo.function, lazy=part.demo.lazy, tab=part.demo.tab)
            if part.reference:
                generate_class_doc(part.reference, part.title)
            if part.link:
                ui.markdown(f'See [more...]({part.link})').classes('bold-links arrow-links')
    with ui.column().classes('w-full p-8 lg:p-16 max-w-[1250px] mx-auto'):
        if documentation.extra_column:
            with ui.grid().classes('grid-cols-[2fr_1fr] max-[600px]:grid-cols-[1fr] gap-x-8 gap-y-16'):
                with ui.column().classes('w-full'):
                    render_content()
                with ui.column():
                    documentation.extra_column()
        else:
            render_content()
    with ui.column().classes('w-full p-4 items-end'):
        ui.link('Imprint & Privacy', '/imprint_privacy').classes('text-sm')


def _ancestor_nodes(node_id: str) -> List[str]:
    parent = next((node for node in nodes if any(child['id'] == node_id for child in node.get('children', []))), None)
    return [node_id] + (_ancestor_nodes(parent['id']) if parent else [])


async def preload_pages() -> None:
    """Execute demo functions once to register all page routes.

    This ensures all @ui.page routes defined within demo functions
    are available immediately on server startup, preventing 404s
    in multi-server deployments."""

    async def call_next(_):
        return Response(status_code=200)

    request = Request(scope={'type': 'http', 'method': 'GET', 'path': '/', 'session': {}})
    await RequestTrackingMiddleware(app).dispatch(request, call_next)
    with Client(page(''), request=request) as client:
        client.tab_id = 'page_preload_client'
        await app.storage._create_tab_storage(client.tab_id)  # pylint: disable=protected-access
        for documentation in registry.values():
            for part in documentation.parts:
                if part.demo is not None:
                    with ui.element() as container:
                        try:
                            result = part.demo.function()
                            if asyncio.iscoroutine(result):
                                # NOTE: we are not using helpers.wait_for because it messes up the context and does not need to be cancelled
                                await asyncio.wait_for(result, timeout=1)
                        except TimeoutError:
                            pass
                        except Exception:
                            log.exception('Error in demo function %s in "%s"', part.demo.function.__name__, part.title)
                        container.delete()
