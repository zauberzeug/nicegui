#!/usr/bin/env python3
from datetime import datetime, date

from fullcalendar import FullCalendar as fullcalendar

from nicegui import events, ui, app

mintime = '00:00:00'
maxtime = '23:59:00'
today = date.today().strftime("%Y-%m-%d")
nowhour = datetime.now().strftime("%H:%M")

def get_events():
    events = [
        {
            'title': 'Math',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 08:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
            'color': 'red',
        },
        {
            'title': 'Physics',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 10:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 12:00:00',
            'color': 'green',
        },
        {
            'title': 'Chemistry',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 13:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 15:00:00',
            'color': 'blue',
        },
        {
            'title': 'Biology',
            'start': datetime.now().strftime(r'%Y-%m-%d') + ' 15:00:00',
            'end': datetime.now().strftime(r'%Y-%m-%d') + ' 17:00:00',
            'color': 'orange',
        },
    ]
    return events


def add_event_to_db(data):
    ui.notify(f'title={data['event_title']}, \
    start= {datetime.combine(datetime.strptime(data['event_start_date'], "%Y-%m-%d"),\
            datetime.strptime(data['event_start_time'], "%H:%M").time())},\
    end="", \
    color= "white", \
    description= {data['event_description']}')

    

def handle_click(event: events.GenericEventArguments):
    if 'info' in event.args:
        if 'event' in event.args['info']:
            ui.notify(f'eventclick: {event.args['info']['event']}') #For event click
        else: 
            ui.notify(f'dateclick: {event.args['info']['date']}') #For Date click


@ui.refreshable
def create_calendar():
    options = {
        'locale': 'fr', #example with other locales can be found here https://fullcalendar.io/docs/locale-demo
        'initialView': 'dayGridMonth',
        'headerToolbar': {'left': 'today', 
                          'center':'title',
                          'right': 'multiMonthYear, dayGridMonth, timeGridWeek, timeGridDay, listWeek'
                          },
        'footerToolbar': {'right': 'prev,next'},
        'slotMinTime': mintime,
        'slotMaxTime': maxtime,
        'duration': '01:00:00',
        'allDaySlot': False,
        'timeZone': 'Europe/Paris', #Example with other Timezone available here https://fullcalendar.io/docs/timeZone-demo
        'height': 'auto',
        'selectable': True, #need to be activated in order to make dateClick available
        'weekNumbers': True, #to show weeknumbers in calendars
        'events': get_events(),
        }
    fullcalendar(options, on_click=handle_click) 


with ui.row():
    ui.page_title("Events")    
    create_calendar()
    with ui.dialog() as add_event, ui.card():
        data={}
        ui.label('Add Event')
        ui.input('Event Title', placeholder='Event Title').on_value_change(lambda e: data.update({'event_title': e.value}))
        checkbox = ui.checkbox('All Day', value=False).on_value_change(lambda e: data.update({'event_title': e.value}))
        with ui.grid(columns=2):
            with ui.column():
                ui.label('Start date')    
                with ui.input('Start Date').on_value_change(lambda e: data.update({'event_start_date': e.value})) as date:
                    with ui.menu().props('no-parent-event') as datemenu:
                        with ui.date(value=today).bind_value(date):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=datemenu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', datemenu.open).classes('cursor-pointer')
            with ui.column().bind_visibility_from(checkbox,'value', value=False): 
                ui.label('Start time')
                #ui.time(value=nowhour).on_value_change(lambda e: data.update({'event_start_time': e.value}))
                with ui.input('Start Time').on_value_change(lambda e: data.update({'event_start_time': e.value})) as time:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.time(value=nowhour).bind_value(time):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with time.add_slot('append'):
                        ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')
            with ui.column():
                ui.label('End date')    
                with ui.input('End Date').on_value_change(lambda e: data.update({'event_end_date': e.value})) as date:
                    with ui.menu().props('no-parent-event') as datemenu:
                        with ui.date(value=today).bind_value(date):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=datemenu.close).props('flat')
                    with date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', datemenu.open).classes('cursor-pointer')
            with ui.column().bind_visibility_from(checkbox,'value', value=False): 
                ui.label('End time')
                #ui.time(value=nowhour).on_value_change(lambda e: data.update({'event_start_time': e.value}))
                with ui.input('End Time').on_value_change(lambda e: data.update({'event_start_time': e.value})) as time:
                    with ui.menu().props('no-parent-event') as menu:
                        with ui.time(value=nowhour).bind_value(time):
                            with ui.row().classes('justify-end'):
                                ui.button('Close', on_click=menu.close).props('flat')
                    with time.add_slot('append'):
                        ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')
        ui.textarea('Event Description', placeholder='Event description').on_value_change(lambda e: data.update({'event_description': e.value})).classes('w-full')
        with ui.row():
            ui.button('Add Event', on_click=lambda: add_event_to_db(data), icon='add').classes('text-xs')
            ui.button('Cancel', icon='close', on_click=add_event.close).classes('text-xs')
    
    ui.button('Add Event', on_click=add_event.open).classes('text-xs')


ui.run(port=8085)
