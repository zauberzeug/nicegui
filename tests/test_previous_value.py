"""previous_value must report the immediate prior Python value, not the
frontend model value (#6499)."""

from nicegui import ui


def test_radio_dict_backed_previous_value():
    changes = []
    radio = ui.radio({101: 'Alice', 205: 'Bob'}, value=101,
                     on_change=lambda e: changes.append((e.value, e.previous_value)))
    radio.set_value(205)
    assert changes == [(205, 101)]


def test_checkbox_previous_value():
    changes = []
    box = ui.checkbox('checked', value=True, on_change=lambda e: changes.append((e.value, e.previous_value)))
    box.set_value(False)
    assert changes == [(False, True)]


def test_input_previous_value():
    changes = []
    box = ui.input(value='first', on_change=lambda e: changes.append((e.value, e.previous_value)))
    box.set_value('second')
    assert changes == [('second', 'first')]


def test_binding_propagation_reports_assignment_order():
    # The binding example from #6499: assignments first -> second -> third.
    # The maintainer's expected events: ('third', 'second') then ('second', 'first')
    # - each event's previous_value is the immediate prior Python assignment.
    events = []
    source = ui.input(value='first', on_change=lambda e: events.append((e.value, e.previous_value)))
    target = ui.input(value='first')
    source.bind_value_to(target)

    def change_source(e):
        if e.value == 'second':
            source.set_value('third')
    target.on_value_change(change_source)
    source.set_value('second')
    assert events == [('second', 'first'), ('third', 'second')]
