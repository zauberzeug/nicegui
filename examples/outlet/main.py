from nicegui import ui


@ui.outlet('/spa2')
def spa2():
    ui.label('spa2')
    yield


@ui.outlet('/')
def spa1():
    ui.label("spa1 header")
    yield
    ui.label("spa1 footer")


# SPA outlet routers can be defined side by side

# views are defined with relative path to their outlet
@spa1.view('/')
def spa1_index():
    ui.label('content of spa1')
    ui.link('more', '/more')
    ui.link('nested', nested_index)
    ui.link('Other outlet', '/spa2')
    ui.link("Click me", lambda: ui.notification("Hello!"))
    ui.button("Click me", on_click=lambda: ui.navigate.to('/nested/sub_page'))


@spa1.view('/more')
def spa1_more():
    ui.label('more content of spa1')
    ui.link('main', '/')
    ui.link('nested', '/nested')


@spa1.outlet('/nested')
def nested():
    ui.label('nested outlet')
    yield


@nested.view('/')
def nested_index():
    ui.label('content of nested')
    ui.link('nested other', '/nested/other')


@nested.view('/sub_page')
def nested_sub():
    ui.label('content of nested sub page')


@nested.view('/other')
def nested_other():
    ui.label('other nested')
    ui.link('nested index', '/nested')


'''
# the view is a function upon the decorated function of the outlet (same technique as "refreshable.refresh")
@spa2.view('/')
def spa2_index():
    ui.label('content of spa2')
    ui.link('more', '/more')


@spa2.view('/more')
def spa2_more():
    ui.label('more content of spa2')
    ui.link('main', '/')


# spa outlets can also be nested (by calling outlet function upon the decorated function of the outlet)
@spa2.outlet('/nested')
def nested():
    ui.label('nested outled')
    yield


@nested.view('/')
def nested_index():
    ui.label('content of nested')
    ui.link('main', '/')


# normal pages are still available
@ui.page('/')
def index():
    ui.link('spa1', '/spa1')
    ui.link('spa2', '/spa2')
    ui.link('nested', '/spa2/nested')
'''

ui.run(show=False)
