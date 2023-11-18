from nicegui import ui



def main_demo() -> None:
    from datetime import datetime
    def format_date(date_str):
        # Parse the date string and format it consistently
        parsed_date = datetime.fromisoformat(date_str)
        return parsed_date.strftime('%Y-%m-%d %H:%M:%S')

    def handle_calendar_click(event):
        try:
            start = format_date(event.args['info']['event']['start'])
            end = format_date(event.args['info']['event']['end'])
            title = event.args['info']['event']['title']
        except Exception as e:
            title = None

        if title:
            show_event_card(title, start, end)

    def show_event_card(title, start, end):
        card = ui.card().style("background-color: #f0f0f0; position: absolute; z-index: 10000; top: 50%; left: 50%; transform: translate(-50%, -50%);")
        with card:
            ui.label(title)
            ui.button("Click me to remove the event!", on_click=lambda: (fullcal.remove_event(title=title.strip(), start=start, end=end), card.delete()))
            ui.button("Close", on_click=lambda e: card.delete())

    def add_event(fullcal):
        fullcal.addevent("Math 1b03", format_date("2023-11-18 09:30:00"), format_date("2023-11-18 10:20:00"), color="red")

    ui.add_head_html("<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>")
    options = {
        "initialView": 'timeGridWeek',
        "slotMinTime": "05:00:00",
        "slotMaxTime": "22:00:00",
        "allDaySlot": False,
        "timeZone": 'local',
        "height": 'auto',
        "events": []
    }
    global fullcal
    fullcal = ui.fullcalendar(options, on_click=lambda e: handle_calendar_click(e))

    ui.button("Click me to add event", on_click=lambda: add_event(fullcal))
    ui.button("Print out all the events", on_click=lambda: print(fullcal.get_events()))

