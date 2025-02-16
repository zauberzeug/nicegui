import asyncio

from nicegui import ui
from nicegui.testing import Screen


# pylint: disable=missing-docstring


def test_routing_url(screen: Screen):
    @ui.outlet('/', on_navigate=lambda _: '/main')
    def layout():
        ui.label('main layout')
        yield

    @layout.view('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == ''  # just the content should have changed, not the url


def test_routing_url_w_forward(screen: Screen):
    def handle_navigate(url: str):
        if url == '/':
            ui.navigate.to('/main')
            return None  # prevent providing new content, forward to the new url
        return url

    @ui.outlet('/', on_navigate=handle_navigate)
    def layout():
        ui.label('main layout')
        yield

    @layout.view('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == 'main'  # just the content should have changed, not the url


def test_passing_objects_via_yield(screen: Screen):
    @ui.outlet('/')
    def layout():
        title = ui.label('original title')
        yield {'title': title}

    @layout.view('/')
    def main_content(title: ui.label):
        title.set_text('changed title')

    screen.open('/')
    screen.should_contain('changed title')


def test_async_outlet(screen: Screen):
    @ui.outlet('/')
    async def layout():
        ui.label('main layout')
        await asyncio.sleep(0.2)
        ui.label('delayed content')
        yield
        ui.label('after yield')

    screen.open('/')
    screen.should_contain('main layout')
    screen.should_contain('delayed content')
    screen.should_contain('after yield')


def test_query_parameters_persistence(screen: Screen):
    received_params = {}

    @ui.outlet('/')
    def layout():
        ui.label('layout')
        yield

    @layout.view('/')
    def index():
        ui.label('index')
        ui.link('Go to page with params', '/page?param1=value1&param2=value2')

    @layout.view('/page')
    def page(param1: str = '', param2: str = ''):
        # Store the raw values for assertion
        received_params.clear()  # Clear previous values to avoid state issues
        received_params['param1'] = param1
        received_params['param2'] = param2
        ui.label(f'params: {param1}, {param2}')
        ui.link('Go to other', '/other')

    @layout.view('/other')
    def other():
        ui.label('other page')

    # Navigate to index
    screen.open('/')
    screen.should_contain('index')

    # Click link to page with parameters
    screen.click('Go to page with params')
    screen.should_contain('params: value1, value2')
    assert received_params['param1'] == 'value1'
    assert received_params['param2'] == 'value2'
    assert 'param1=value1' in screen.selenium.current_url
    assert 'param2=value2' in screen.selenium.current_url

    # Navigate to other page
    screen.click('Go to other')
    screen.should_contain('other page')
    assert 'param1' not in screen.selenium.current_url
    assert 'param2' not in screen.selenium.current_url

    # Go back and verify parameters are preserved
    screen.selenium.back()
    screen.wait(0.5)  # wait for navigation to complete
    screen.should_contain('params: value1, value2')
    assert received_params['param1'] == 'value1'
    assert received_params['param2'] == 'value2'
    assert 'param1=value1' in screen.selenium.current_url
    assert 'param2=value2' in screen.selenium.current_url


def test_outlet_with_async_sub_outlet(screen: Screen):
    @ui.outlet('/')
    def layout():
        ui.label('main')
        yield

    @layout.outlet('/')
    async def main_content():
        await asyncio.sleep(0.2)
        ui.label('sub')
        yield

    screen.open('/')
    screen.should_contain('main')
    screen.should_contain('sub')


def test_nested_outlets_with_yield(screen: Screen):
    # First level outlet
    @ui.outlet('/')
    def root_layout():
        counter = ui.label('0')
        ui.button('Increment', on_click=lambda: counter.set_text(str(int(counter.text) + 1)))
        yield {'counter': counter}

    # Second level outlet
    @root_layout.outlet('/section/{section_id}')
    def section_layout(counter: ui.label, section_id: str):
        ui.label(f'Section {section_id}')
        section_counter = ui.label('0')
        ui.button('Add to root', on_click=lambda: counter.set_text(str(int(counter.text) + int(section_counter.text))))
        yield {'section_counter': section_counter}

    # Third level outlet
    @section_layout.outlet('/subsection/{subsection_id}')
    def subsection_layout(section_counter: ui.label, subsection_id: str):
        ui.label(f'Subsection {subsection_id}')
        ui.button('Add to section', on_click=lambda: section_counter.set_text(str(int(section_counter.text) + 1)))
        yield

    # Views for each level
    @root_layout.view('/')
    def root_index(counter: ui.label):
        ui.label('Root Index')
        ui.link('Go to Section 1', '/section/1')

    @section_layout.view('/')
    def section_index(section_id: str, section_counter: ui.label):
        ui.label(f'Section {section_id} Index')
        ui.link('Go to Subsection A', f'/section/{section_id}/subsection/A')

    @subsection_layout.view('/')
    def subsection_index(section_id: str, subsection_id: str):
        ui.label(f'Content of Subsection {subsection_id}')

    # Test the nested structure
    screen.open('/')
    screen.should_contain('Root Index')
    assert screen.selenium.current_url.endswith('/')

    # Navigate to section 1
    screen.click('Go to Section 1')
    screen.should_contain('Section 1 Index')
    assert '/section/1' in screen.selenium.current_url

    # Navigate to subsection A
    screen.click('Go to Subsection A')
    screen.should_contain('Content of Subsection A')
    assert '/section/1/subsection/A' in screen.selenium.current_url

    # Test counter propagation
    screen.click('Add to section')  # Increment subsection counter
    screen.click('Add to root')     # Add section counter to root counter
    screen.should_contain('1')      # Root counter should be 1

    # Test direct root counter increment
    screen.click('Increment')       # Increment root counter
    screen.should_contain('2')      # Root counter should be 2
