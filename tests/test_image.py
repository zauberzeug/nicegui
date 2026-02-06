from pathlib import Path

from PIL import Image

from nicegui import app, ui
from nicegui.testing import SharedScreen

example_file = Path(__file__).parent / '../examples/slideshow/slides/slide1.jpg'
example_data = ('data:image/png;base64,'
                'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAEHElEQVRo'
                'ge2ZXUxbZRjHf6enH3QtBQ7paIFlMO2AMXTGqZE40bCpiRdzF06Nsu3O6G68MH5MnYkk3vhx4cWCJppF'
                'lvgZ74wXbsZdLCYaQMeWUWM30EJZgVM+WtpS2uNFoQzTU3pKu2O0v8v38//Pe57ned8cKFOmTBk9EVR7'
                'vrxsRlJ6gR7AfdMUrWcC6EcWTnK4fSnbAKPqVEl5C3ipRMLypR54GUkBeCXbAEOOyUdKoahAjqp15DKg'
                '12eTDZdaRy4DN43p+1s55HTwVF0Vk/taNM3V3UCDxUStSWQ4HKPDXsFwOK5pvm4GTILADquZbslGPKUA'
                'sNdRwXg8wQ6rOe911NPo2UvKplXmYOcWM957Par9wrnL6xv2786qVbcT8EUTSOdH+Co4T//kLE0Xfgfg'
                'wcFRpPMjea+jm4GkohBaTuKxmhlaiNFoMZFS4Jf5KKHlZN7rqBeyEvPF7kYO11UBsKdyLUuGH2jjNV+Q'
                't0en8lpHtxN41RfkyUt+APYPjfJNcJ7v5TB7f77KJxOhvNfRzcDVaPpqM51Ick6O4DQbuTC7yMBClMml'
                '5bzX0bUOdNgtXAzHAGi3WRiOaKsBoGMa1cy/LY0Wi7IBvfl/GhCAJ+qq+HbPdgL7Whi8+5YN59zjsOLr'
                '9ODr9PB6s7OQbbOiuRI7jAa+7tjGAcmeaQtukLdNgsBHbfWZW2atSdS6rSqaDAjAp7saOSDZSSoKpwOz'
                'nJmcw7uYO3+/uL2W2+wVm9GpiiYD3ZKNg85KAI57A3w4vnHJv9Vq5o1mJ9FUCqMgYBLUS08haIqBY+4a'
                'AK5E4lyJxDnV4ub0rgaOuasRswgTgL7WeqwGA73XpjIPl2Ki6QQ6q6wAbDUb+fHO5kwZP+qu5qDTwaGL'
                'f64bf8RdTbdkYzgc492xGU40FS94V9F0Ai5L2q9kEunzyxz3BhhYiALwmLOSh24IbKfZyHseFykFnh0J'
                'kFBKczPRZMBqSA//eCLE894Ap/wyDw+NsZhMAWTiA+B9Tx21JpG+cZmf5haLKHk9mgysCp1bTmXaZhJJ'
                'vIvpq3HTSpq83V7BM65qAHrc1chdrchdrdjE9HbPNUjIXa2bV49GA6tC22yWTJsoCLhXPq3ZRHKlbW1O'
                'pWigxihSYxQzMWMxCNQYi1MLNAXxZ9fnuKOygkckO0+7qjgrR3hhWy0uc3qZ72bCAPwWjmd9mPvv28kW'
                '0UDfuMyJP4JFkK/RwAd/zfD4Vgd3OaycaW9c1/dDKMLn1+eAtQf7P1kN41gqe38haPqE4imF7sFR3hmb'
                'ZiyWIKEo+KJL9F6b4tFfx1jeINMMLcQYWIjijyU2JfpG/tMvsokSSSkAYVytJ5eB/hIoKQxBUdWiHsSy'
                'cHLlz0gP6T8lepD+xTQjvKnT/mXKlCmzAX8Dl7JCqRHaepQAAAAASUVORK5CYII=')


def test_base64_image(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.image(example_data).style('width: 50px;')

    shared_screen.open('/')
    shared_screen.wait(0.2)
    image = shared_screen.find_by_class('q-img__image')
    assert 'data:image/png;base64,iVB' in image.get_attribute('src')


def test_setting_local_file(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.image(example_file)

    shared_screen.open('/')
    image = shared_screen.find_by_class('q-img__image')
    shared_screen.should_load_image(image)


def test_binding_local_file(shared_screen: SharedScreen):
    images = {'one': example_file}

    @ui.page('/')
    def page():
        ui.image().bind_source_from(images, 'one')

    shared_screen.open('/')
    image = shared_screen.find_by_class('q-img__image')
    shared_screen.should_load_image(image)


def test_set_source_with_local_file(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.image().set_source(example_file)

    shared_screen.open('/')
    image = shared_screen.find_by_class('q-img__image')
    shared_screen.should_load_image(image)


def test_removal_of_generated_routes(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        img = ui.image(example_file)
        ui.button('Slide 2', on_click=lambda: img.set_source(str(example_file).replace('slide1', 'slide2')))
        ui.button('Slide 3', on_click=lambda: img.set_source(str(example_file).replace('slide1', 'slide3')))

    shared_screen.open('/')
    number_of_routes = len(app.routes)

    shared_screen.click('Slide 2')
    shared_screen.wait(0.5)
    assert len(app.routes) == number_of_routes

    shared_screen.click('Slide 3')
    shared_screen.wait(0.5)
    assert len(app.routes) == number_of_routes


def test_force_reload(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        img1 = ui.image(example_file)
        img2 = ui.image(example_data)

        ui.button('Reload 1', on_click=img1.force_reload)
        ui.button('Reload 2', on_click=img2.force_reload)

    shared_screen.open('/')
    images = shared_screen.find_all_by_class('q-img__image')
    shared_screen.should_load_image(images[0])
    shared_screen.should_load_image(images[1])

    shared_screen.click('Reload 1')
    shared_screen.wait(0.5)
    assert not shared_screen.caplog.records

    shared_screen.click('Reload 2')
    shared_screen.wait(0.5)
    shared_screen.assert_py_logger('WARNING', 'ui.image: force_reload() only works with network sources (not data URIs)')


def test_pil_image_cleanup(shared_screen: SharedScreen):
    temp_path_str = ''

    @ui.page('/')
    def page():
        nonlocal temp_path_str
        pil_img = Image.new('RGB', (100, 100), color='red')
        image = ui.image(pil_img)
        temp_path_str = str(image._temp_path)  # pylint: disable=protected-access  # store string, not the _TempPath
        assert Path(temp_path_str).exists()
        ui.button('Delete', on_click=image.delete)

    shared_screen.open('/')
    image = shared_screen.find_by_class('q-img__image')
    shared_screen.should_load_image(image)

    shared_screen.click('Delete')
    shared_screen.wait_for(lambda: not Path(temp_path_str).exists())
