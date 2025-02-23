import asyncio

import pytest

from nicegui import ui
from nicegui.testing import Screen

# pylint: disable=missing-docstring


def test_routing_url(screen: Screen):
    @ui.content('/', on_navigate=lambda _: '/main')
    def layout():
        ui.label('main layout')
        yield

    @layout.content('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == ''  # just the content should have changed, not the url


def test_routing_url_using_navigate(screen: Screen):
    def handle_navigate(url: str):
        if url == '/':
            ui.navigate.to('/main')
            return None  # prevent providing new content, forward to the new url
        return url

    @ui.content('/', on_navigate=handle_navigate)
    def layout():
        ui.label('main layout')
        yield

    @layout.content('/main')
    def main_content():
        ui.label('main content')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('main content')
    assert screen.selenium.current_url.split('/')[-1] == 'main'  # just the content should have changed, not the url


def test_passing_objects_via_yield(screen: Screen):
    @ui.content('/')
    def layout():
        title = ui.label('original title')
        yield {'title': title}

    @layout.content('/')
    def main_content(title: ui.label):
        title.set_text('changed title')

    screen.open('/')
    screen.should_contain('changed title')


def test_async_outlet(screen: Screen):
    @ui.content('/')
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


def test_preserving_query_parameters(screen: Screen):
    received_params = {}

    @ui.content('/')
    def layout():
        ui.label('layout')
        yield

    @layout.content('/')
    def index():
        ui.label('index')
        ui.link('Go to page with params', '/page?param1=value1&param2=value2')

    @layout.content('/page')
    def page(param1: str = '', param2: str = ''):
        # Store the raw values for assertion
        received_params.clear()  # Clear previous values to avoid state issues
        received_params['param1'] = param1
        received_params['param2'] = param2
        ui.label(f'params: {param1}, {param2}')
        ui.link('Go to other', '/other')

    @layout.content('/other')
    def other():
        ui.label('other page')

    # Navigate to index
    screen.open('/')
    screen.should_contain('index')

    # Click link to page with parameters
    screen.click('Go to page with params')
    screen.should_contain('params: value1, value2')
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
    assert 'param1=value1' in screen.selenium.current_url
    assert 'param2=value2' in screen.selenium.current_url


def test_outlet_with_async_sub_outlet(screen: Screen):
    @ui.content('/')
    def layout():
        ui.label('main')
        yield

    @layout.content('/')
    async def main_content():
        await asyncio.sleep(0.2)
        ui.label('sub')
        yield

    screen.open('/')
    screen.should_contain('main')
    screen.should_contain('sub')


def test_path_conflict(screen: Screen):
    """Test that a page and an outlet can share a root path"""
    @ui.page('/mytestpage')
    def page():
        ui.label('Test Page')

    @ui.content('/')
    def layout():
        ui.label('main layout')
        yield

    @layout.content('/')
    def main_content():
        ui.label('main content')

    screen.open('/mytestpage')
    screen.should_contain('Test Page')
    screen.open('/')
    screen.should_contain('main layout')
    screen.should_contain('main content')


def test_excluded_paths(screen: Screen):
    """Test that paths defined elsewhere are automatically excluded from the outlet"""
    @ui.page('/excluded')
    def excluded_page():
        ui.label('Excluded Page')
        ui.label('No outlet content')  # Add this to make it clearer this is the page content

    @ui.content('/')
    def layout():
        ui.label('main layout')
        ui.link('Go to excluded', '/excluded')
        ui.link('Go to allowed', '/allowed')
        yield

    @layout.content('/allowed')
    def allowed_page():
        ui.label('Allowed Page')

    # Test initial page
    screen.open('/')
    screen.should_contain('main layout')

    # Test navigation to excluded path
    screen.open('/excluded')
    screen.should_contain('Excluded Page')
    screen.should_not_contain('main layout')  # Verify outlet content is not present

    # Test navigation to allowed path
    screen.open('/allowed')
    screen.wait(1.0)  # wait for navigation
    screen.should_contain('Allowed Page')
    screen.should_contain('main layout')  # Verify outlet content is present

    # Test navigation to excluded path via click
    screen.click('Go to excluded')
    screen.wait(1.0)  # wait for navigation
    screen.should_contain('Excluded Page')
    screen.should_not_contain('main layout')  # Verify outlet content is not present


def test_sub_outlet_layout_calls(screen: Screen):
    """Test that the main layout builder is not called when switching pages in a sub outlet"""
    main_layout_calls = 0
    sub_layout_calls = 0

    @ui.content('/')
    def main_layout():
        nonlocal main_layout_calls
        main_layout_calls += 1
        ui.label('main layout')
        ui.link('Go to Page 1', '/sub/page1')  # Add link in root layout
        yield

    @main_layout.content('/sub')
    def sub_layout():
        nonlocal sub_layout_calls
        sub_layout_calls += 1
        ui.label('sub layout')
        yield

    @sub_layout.content('/page1')
    def page1():
        ui.label('Page 1')
        ui.link('Go to Page 2', '/sub/page2')

    @sub_layout.content('/page2')
    def page2():
        ui.label('Page 2')
        ui.link('Back to Page 1', '/sub/page1')

    @main_layout.content('/')
    def root_view():
        ui.label('Root Page')

    screen.open('/')
    screen.wait(1.0)
    screen.should_contain('main layout')
    screen.should_contain('Root Page')
    assert main_layout_calls == 1
    assert sub_layout_calls == 0

    screen.click('Go to Page 1')
    screen.wait(0.5)
    screen.should_contain('Page 1')
    assert main_layout_calls == 1  # Should still be 1
    assert sub_layout_calls == 1

    screen.click('Go to Page 2')
    screen.wait(0.5)
    screen.should_contain('Page 2')
    assert main_layout_calls == 1  # Should still be 1
    assert sub_layout_calls == 1  # Should still be 1

    screen.click('Back to Page 1')
    screen.wait(0.5)
    screen.should_contain('Page 1')
    assert main_layout_calls == 1  # Should still be 1
    assert sub_layout_calls == 1  # Should still be 1


@pytest.mark.parametrize('navigation_strategy', ['backend', 'frontend'])
def test_navigating_in_outlet_hierarchy(screen: Screen, navigation_strategy: str):
    """Test that navigation works correctly when an outlet path appears to be contained within another."""
    @ui.content('/mail')
    def mail_layout():
        ui.label('Mail Layout')
        yield

    @mail_layout.content('/index')
    def mail_index():
        ui.label('Mail Index')
        ui.button('Navigate to root via backend', on_click=lambda: ui.navigate.to('/'))
        ui.link('Navigate to root via frontend', '/')

    # Then define the root outlet and its view - order matters for reproducing the bug
    @ui.content('/')
    def root_layout():
        ui.label('Root Layout')
        yield

    @root_layout.content('/')
    def root_index():
        ui.label('Root Index')
        ui.button('Navigate to mail via backend', on_click=lambda: ui.navigate.to('/mail/index'))
        ui.link('Navigate to mail via frontend', '/mail/index')

    # Start at mail/index
    screen.open('/mail/index')
    screen.should_contain('Mail Layout')
    screen.should_contain('Mail Index')
    screen.should_not_contain('Root Layout')

    screen.click(f'Navigate to root via {navigation_strategy}')
    screen.wait(0.5)
    screen.should_contain('Root Layout')
    screen.should_contain('Root Index')
    screen.should_not_contain('Mail Layout')

    screen.click(f'Navigate to mail via {navigation_strategy}')
    screen.wait(0.5)
    screen.should_contain('Mail Layout')
    screen.should_contain('Mail Index')
    screen.should_not_contain('Root Layout')
    assert '/mail/index' in screen.selenium.current_url


def test_nested_outlets_with_yield(screen: Screen):
    # First level outlet
    @ui.content('/')
    def root_layout():
        counter = ui.label('0')
        ui.button('Increment', on_click=lambda: counter.set_text(str(int(counter.text) + 1)))
        yield {'counter': counter}

    # Second level outlet
    @root_layout.content('/section/{section_id}')
    def section_layout(counter: ui.label, section_id: str):
        ui.label(f'Section {section_id}')
        section_counter = ui.label('0')
        ui.button('Add to root', on_click=lambda: counter.set_text(str(int(counter.text) + int(section_counter.text))))
        yield {'section_counter': section_counter}

    # Third level outlet
    @section_layout.content('/subsection/{subsection_id}')
    def subsection_layout(section_counter: ui.label, subsection_id: str):
        ui.label(f'Subsection {subsection_id}')
        ui.button('Add to section', on_click=lambda: section_counter.set_text(str(int(section_counter.text) + 1)))
        yield

    # Views for each level
    @root_layout.content('/')
    def root_index(counter: ui.label):
        ui.label('Root Index')
        ui.link('Go to Section 1', '/section/1')

    @section_layout.content('/')
    def section_index(section_id: str, section_counter: ui.label):
        ui.label(f'Section {section_id} Index')
        ui.link('Go to Subsection A', f'/section/{section_id}/subsection/A')

    @subsection_layout.content('/')
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
    screen.click('Add to section')
    screen.click('Add to root')
    screen.should_contain('1')

    # Test direct root counter increment
    screen.click('Increment')
    screen.should_contain('2')


def test_same_page_navigation(screen: Screen):
    """Test that navigating to the same page doesn't rebuild it."""
    build_count = 0

    @ui.content('/')
    def layout():
        ui.label('layout')
        yield

    @layout.content('/page')
    def page():
        nonlocal build_count
        build_count += 1
        ui.label(f'Page built {build_count} times')
        ui.link('Self link', '/page')
        ui.button('Self navigate', on_click=lambda: ui.navigate.to('/page'))

    # Initial navigation
    screen.open('/page')
    screen.should_contain('Page built 1 times')
    assert build_count == 1

    # Navigate to same page via link
    screen.click('Self link')
    screen.wait(0.5)
    screen.should_contain('Page built 1 times')
    assert build_count == 1  # Should not have rebuilt

    # Navigate to same page via ui.navigate
    screen.click('Self navigate')
    screen.wait(0.5)
    screen.should_contain('Page built 1 times')
    assert build_count == 1  # Should not have rebuilt

    # Add another view and verify build counter increases when switching views
    @layout.content('/other')
    def other_page():
        nonlocal build_count
        build_count += 1
        ui.label(f'Other page built {build_count} times')
        ui.link('Go to first page', '/page')

    # Navigate to different page
    screen.open('/other')
    screen.wait(0.5)
    screen.should_contain('Other page built 2 times')
    assert build_count == 2  # Should have rebuilt for new view

    # Navigate back to first page
    screen.click('Go to first page')
    screen.wait(0.5)
    screen.should_contain('Page built 3 times')
    assert build_count == 3  # Should have rebuilt for view switch


def test_outlet_without_yield(screen: Screen):
    @ui.content('/')
    def main():
        ui.label('main content without yield')

    screen.open('/')
    screen.should_contain('main content without yield')


def test_async_outlet_without_yield(screen: Screen):
    @ui.content('/')
    async def main():
        await asyncio.sleep(0.2)
        ui.label('main content without yield')

    screen.open('/')
    screen.should_contain('main content without yield')
