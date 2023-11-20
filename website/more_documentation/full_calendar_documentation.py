from nicegui import ui



def main_demo() -> None:
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
        "height": 'auto',
        "width": 'auto',
        "events": []
    }
    global fullcal

    fullcal = ui.fullcalendar(options) # on_click=lambda e: handle_calendar_click(e)
    fullcal.addevent("Math 1b03", format_date(str(datetime.now())), format_date(str(datetime.now())), color="red")


main_demo()
ui.run()