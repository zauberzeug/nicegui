from nicegui import app, ui

calendarEvents = ui.calendar_event()
# calendarEvents.add_event('MATH 1B03 - T06 - Linear Algebra I', '2023-10-11 09:30:00', '2023-10-11 10:20:00')
# calendarEvents.add_event('MATH 1ZA3 - C01 - Engineering Mathematics I', '2023-10-11 11:30:00', '2023-10-11 12:20:00')
# calendarEvents.add_event('COMPSCI 1MD3 - T05 - Introduction to Programming', '2023-10-11 12:30:00', '2023-10-11 13:20:00')
# calendarEvents.add_event('MATH 1B03 - C02 - Linear Algebra I', '2023-10-11 14:30:00', '2023-10-11 15:20:00')
# calendarEvents.add_event('FRENCH 1A06A - C04 - Introduction to French Studies: Advanced Level', '2023-10-11 20:00:00', '2023-10-11 22:00:00')
# calendarEvents.add_event('COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', '2023-10-12 10:30:00', '2023-10-12 11:20:00')
# calendarEvents.add_event('MATH 1ZA3 - C01 - Engineering Mathematics I', '2023-10-12 11:30:00', '2023-10-12 12:20:00')
# calendarEvents.add_event('COMPSCI 1MD3 - C01 - Introduction to Programming', '2023-10-12 13:30:00', '2023-10-12 14:20:00')
# calendarEvents.add_event('MATH 1B03 - C02 - Linear Algebra I', '2023-10-12 14:30:00', '2023-10-12 15:20:00')
# calendarEvents.add_event('COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', '2023-10-13 10:30:00', '2023-10-13 11:20:00')
# calendarEvents.add_event('COMPSCI 1JC3 - T01 - Introduction to Computational Thinking', '2023-10-13 11:30:00', '2023-10-13 13:20:00')
# calendarEvents.add_event('MATH 1ZA3 - T02 - Engineering Mathematics I', '2023-10-13 14:30:00', '2023-10-13 15:20:00')
# calendarEvents.add_event('MATH 1ZA3 - C01 - Engineering Mathematics I', '2023-10-16 11:30:00', '2023-10-16 12:20:00')
# calendarEvents.add_event('COMPSCI 1MD3 - C01 - Introduction to Programming', '2023-10-16 13:30:00', '2023-10-16 14:20:00')
# calendarEvents.add_event('MATH 1B03 - C02 - Linear Algebra I', '2023-10-16 14:30:00', '2023-10-16 15:20:00')
# calendarEvents.add_event('FRENCH 1A06A - T07 - Introduction to French Studies: Advanced Level', '2023-10-16 17:30:00', '2023-10-16 18:20:00')
# calendarEvents.add_event('FRENCH 1A06A - C04 - Introduction to French Studies: Advanced Level', '2023-10-16 19:00:00', '2023-10-16 20:00:00')
# calendarEvents.add_event('COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', '2023-10-17 10:30:00', '2023-10-17 11:20:00')
# calendarEvents.add_event('COMPSCI 1MD3 - C01 - Introduction to Programming', '2023-10-17 14:30:00', '2023-10-17 15:20:00')
# calendarEvents.add_event('MATH 1B03 - T06 - Linear Algebra I', '2023-10-18 09:30:00', '2023-10-18 10:20:00')


# calendarEvents.remove_event('MATH 1B03 - T06 - Linear Algebra I', '2023-10-18 09:30:00', '2023-10-18 10:20:00')

ui.add_head_html("<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>")
options = {
    "initialView": 'timeGridWeek',
    "slotMinTime": "05:00:00",
    "slotMaxTime": "22:00:00",
    "allDaySlot": False,
    "timeZone": 'local',
    "height": 'auto', "events": calendarEvents.get_events()}



title= None
def func(e):
    global title, card
    title = None
    
    try:
        print(e.args['info']['event']['title'])
        title = e.args['info']['event']['title']
    except:
        pass

    if title:
        card = ui.card().style("background-color: #f0f0f0; position: absolute; z-index: 10000; top: 50%; left: 50%; transform: translate(-50%, -50%);")
        with card:
            ui.label(title)
            ui.button("Close", on_click=lambda e: card.delete())
fullcal = ui.fullcalendar(options,  on_click=lambda e: func(e))

def add_event():
    global fullcal, options
    # calendarEvents.add_event('MATH 1B03 - T06 - Linear Algebra I', '2023-11-18 09:30:00', '2023-11-18 10:20:00')
    # options['events'] = calendarEvents.get_events()
    # fullcal._props['options'] = options
    # fullcal.update()
    # fullcal.updatecal(options)
    fullcal.addevent({"title": "MATH 1B03 - T06 - Linear Algebra I", "start":"2023-11-18 09:30:00", "end":"2023-11-18 10:20:00"})
    
    print(fullcal._props)


ui.button("click me to add event", on_click=add_event)

ui.run()
















































 

