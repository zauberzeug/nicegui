from nicegui import app, ui
from datetime import datetime

def format_date(date_str):
    # Parse the date string and format it consistently
    parsed_date = datetime.fromisoformat(date_str)
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')




ui.add_head_html("<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>")
options = {
    "initialView": 'timeGridWeek',
    "slotMinTime": "05:00:00",
    "slotMaxTime": "22:00:00",
    "allDaySlot": False,
    "timeZone": 'local',
    "height": 'auto', "events": []
    }


title= None
fullcal = None
def func(e):
    
    global fullcal, title, card
    title = None
    # print(e)
    try:
        start = format_date(e.args['info']['event']['start'])
        end = format_date(e.args['info']['event']['end'])
        title2 = e.args['info']['event']['title']
    except:
        title2 = None

    if title2:
        card = ui.card().style("background-color: #f0f0f0; position: absolute; z-index: 10000; top: 50%; left: 50%; transform: translate(-50%, -50%);")
        with card:
            ui.label(title2)
            ui.button("Click me to remove the event!", on_click=lambda : (fullcal.remove_event(title=title2.strip(), start=(start), end=(end)), card.delete()))
            ui.button("Close", on_click=lambda e: card.delete())


fullcal = ui.fullcalendar(options,  on_click=lambda e: func(e))


def add_event():
    global fullcal
    fullcal.addevent("Math 1b03", format_date("2023-11-18 09:30:00"), format_date("2023-11-18 10:20:00"), color="red")
    


def remove_event():
    global fullcal
    fullcal.remove_event("Math 1b03", format_date("2023-11-18 09:30:00"), format_date("2023-11-18 10:20:00"))

ui.button("click me to add event", on_click=add_event)
ui.run()


