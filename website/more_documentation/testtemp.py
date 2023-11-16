from nicegui import ui
import json

events = [{'title': 'MATH 1B03 - T06 - Linear Algebra I', 'start': '2023-10-11 09:30:00', 'end': '2023-10-11 10:20:00'}, {'title': 'MATH 1ZA3 - C01 - Engineering Mathematics I', 'start': '2023-10-11 11:30:00', 'end': '2023-10-11 12:20:00'}, {'title': 'COMPSCI 1MD3 - T05 - Introduction to Programming', 'start': '2023-10-11 12:30:00', 'end': '2023-10-11 13:20:00'}, {'title': 'MATH 1B03 - C02 - Linear Algebra I', 'start': '2023-10-11 14:30:00', 'end': '2023-10-11 15:20:00'}, {'title': 'FRENCH 1A06A - C04 - Introduction to French Studies: Advanced Level', 'start': '2023-10-11 20:00:00', 'end': '2023-10-11 22:00:00'}, {'title': 'COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', 'start': '2023-10-12 10:30:00', 'end': '2023-10-12 11:20:00'}, {'title': 'MATH 1ZA3 - C01 - Engineering Mathematics I', 'start': '2023-10-12 11:30:00', 'end': '2023-10-12 12:20:00'}, {'title': 'COMPSCI 1MD3 - C01 - Introduction to Programming', 'start': '2023-10-12 13:30:00', 'end': '2023-10-12 14:20:00'}, {'title': 'MATH 1B03 - C02 - Linear Algebra I', 'start': '2023-10-12 14:30:00', 'end': '2023-10-12 15:20:00'}, {'title': 'COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', 'start': '2023-10-13 10:30:00', 'end': '2023-10-13 11:20:00'}, {'title': 'COMPSCI 1JC3 - T01 - Introduction to Computational Thinking', 'start': '2023-10-13 11:30:00', 'end': '2023-10-13 13:20:00'}, {'title': 'MATH 1ZA3 - T02 - Engineering Mathematics I', 'start': '2023-10-13 14:30:00', 'end': '2023-10-13 15:20:00'}, {'title': 'MATH 1ZA3 - C01 - Engineering Mathematics I', 'start': '2023-10-16 11:30:00', 'end': '2023-10-16 12:20:00'}, {'title': 'COMPSCI 1MD3 - C01 - Introduction to Programming', 'start': '2023-10-16 13:30:00', 'end': '2023-10-16 14:20:00'}, {'title': 'MATH 1B03 - C02 - Linear Algebra I', 'start': '2023-10-16 14:30:00', 'end': '2023-10-16 15:20:00'}, {'title': 'FRENCH 1A06A - T07 - Introduction to French Studies: Advanced Level', 'start': '2023-10-16 17:30:00', 'end': '2023-10-16 18:20:00'}, {'title': 'FRENCH 1A06A - C04 - Introduction to French Studies: Advanced Level', 'start': '2023-10-16 19:00:00', 'end': '2023-10-16 20:00:00'}, {'title': 'COMPSCI 1JC3 - C01 - Introduction to Computational Thinking', 'start': '2023-10-17 10:30:00', 'end': '2023-10-17 11:20:00'}, {'title': 'COMPSCI 1MD3 - C01 - Introduction to Programming', 'start': '2023-10-17 14:30:00', 'end': '2023-10-17 15:20:00'}, {'title': 'MATH 1B03 - T06 - Linear Algebra I', 'start': '2023-10-18 09:30:00', 'end': '2023-10-18 10:20:00'}]
with ui.row():
    with ui.column().style("width: 90%; height: 100%;"):
        ui.element().classes('my-calendar').style("width: 100%; height: 600px;")

        ui.add_head_html('''
                <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>
                <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    var calendarEvents = {events_json};
                    window.calendarInstance = new FullCalendar.Calendar(document.querySelector('.my-calendar'), {{
                        initialView: 'timeGridWeek',
                        slotMinTime: "05:00:00",
                        slotMaxTime: "22:00:00",
                        allDaySlot: false,
                        timeZone: 'local',
                        height: 'auto',
                        events: 
                            calendarEvents,
                        eventClick: function(info) {{
                         alert('Event: ' + info.event.title);
                        }}
                      
                    }});
                    window.calendarInstance.render();
                }});
                </script>
            '''.format(events_json=json.dumps(events)))



ui.run()