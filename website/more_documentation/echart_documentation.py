from nicegui import ui


def main_demo() -> None:
    chart = ui.echart({
        'xAxis': {'type': 'value'},
        'yAxis': {'type': 'value'},
        'series': [{'data': [[0, 0], [1, 1]], 'type': 'line'}],
    })

    def update():
        x = len(chart.options['series'][0]['data'])
        chart.options['series'][0]['data'].append([x, x**2])
        chart.update()

    ui.button('Update', on_click=update)
