from fastapi import Request, Response

from nicegui import Client, app, ui


@app.exception_handler(404)
async def exception_handler_404(request: Request, exception: Exception) -> Response:
    with Client(ui.page('')) as client:
        with ui.column().style('width: 100%; padding: 5rem 0; align-items: center; gap: 0'):
            ui.label('Sorry').style('font-size: 3.75rem; line-height: 1; padding: 1.25rem 0')
            ui.label('Something went wrong.').style('font-size: 1.25rem; line-height: 1.75rem; padding: 1.25rem 0')
            ui.label('Please contact the server administrator at change@this.com for additional support.').style(
                'font-size: 1.125rem; line-height: 1.75rem; color: rgb(107 114 128)')
    return client.build_response(request, 404)

ui.link('Go to nonexisting page', '/nonexisting')

ui.run()
