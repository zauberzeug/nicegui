from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    async def alert():
        await ui.run_javascript('alert("Hello!")', respond=False)

    async def get_date():
        time = await ui.run_javascript('Date()')
        ui.notify(f'Browser time: {time}')

    async def access_elements():
        await ui.run_javascript(f'getElement({label.id}).innerText += " Hello!"')

    ui.button('fire and forget', on_click=alert)
    ui.button('receive result', on_click=get_date)
    ui.button('access elements', on_click=access_elements)
    label = ui.label()


def more() -> None:
    @text_demo('Run async JavaScript', '''
        Using `run_javascript` you can also run asynchronous code in the browser.
        The following demo shows how to get the current location of the user.
    ''')
    def run_async_javascript():
        async def show_location():
            response = await ui.run_javascript('''
                return await new Promise((resolve, reject) => {
                    if (!navigator.geolocation) {
                        reject(new Error('Geolocation is not supported by your browser'));
                    } else {
                        navigator.geolocation.getCurrentPosition(
                            (position) => {
                                resolve({
                                    latitude: position.coords.latitude,
                                    longitude: position.coords.longitude,
                                });
                            },
                            () => {
                                reject(new Error('Unable to retrieve your location'));
                            }
                        );
                    }
                });
            ''', timeout=5.0)
            ui.notify(f'Your location is {response["latitude"]}, {response["longitude"]}')

        ui.button('Show location', on_click=show_location)
