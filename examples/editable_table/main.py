#!/usr/bin/env python3
from nicegui import events, ui

columns = [
    {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left'},
    {'name': 'age', 'label': 'Age', 'field': 'age'},
]
rows = [
    {'id': 0, 'name': 'Alice', 'age': 18},
    {'id': 1, 'name': 'Bob', 'age': 21},
    {'id': 2, 'name': 'Carol', 'age': 20},
]


def add_row() -> None:
    """
    Add a new row to the table.

    This function generates a new ID for the row by finding the maximum ID value in the existing rows and incrementing it by 1.
    It then creates a new row dictionary with default values for 'name' and 'age' fields.
    The new row is appended to the 'rows' list.
    Finally, a notification is displayed with the ID of the newly added row and the table is updated.

    Returns:
        None
    """
    new_id = max((dx['id'] for dx in rows), default=-1) + 1
    rows.append({'id': new_id, 'name': 'New guy', 'age': 21})
    ui.notify(f'Added new row with ID {new_id}')
    table.update()


def rename(e: events.GenericEventArguments) -> None:
    """
    Updates the rows in the table with the provided event arguments.

    Args:
        e (events.GenericEventArguments): The event arguments containing the updated row data.

    Returns:
        None

    Raises:
        None

    Example:
        To update the rows in the table, call the rename function with the appropriate event arguments:

        ```
        event_args = events.GenericEventArguments(id=1, name='John Doe', age=30)
        rename(event_args)
        ```

    This function iterates over the rows in the table and updates the row that matches the provided 'id' in the event arguments.
    After updating the rows, it notifies the user with the updated rows and updates the table UI.
    """
    for row in rows:
        if row['id'] == e.args['id']:
            row.update(e.args)
    ui.notify(f'Updated rows to: {table.rows}')
    table.update()


def delete(e: events.GenericEventArguments) -> None:
    """
    Deletes a row from the table based on the provided ID.

    Args:
        e (events.GenericEventArguments): The event arguments containing the ID of the row to be deleted.

    Returns:
        None

    Raises:
        None

    Example:
        To delete a row with ID 5, you can call the delete function as follows:
        delete(events.GenericEventArguments(args={'id': 5}))
    """
    rows[:] = [row for row in rows if row['id'] != e.args['id']]
    ui.notify(f'Deleted row with ID {e.args["id"]}')
    table.update()


table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-60')
table.add_slot('header', r'''
    <q-tr :props="props">
        <q-th auto-width />
        <q-th v-for="col in props.cols" :key="col.name" :props="props">
            {{ col.label }}
        </q-th>
    </q-tr>
''')
table.add_slot('body', r'''
    <q-tr :props="props">
        <q-td auto-width >
            <q-btn size="sm" color="warning" round dense icon="delete"
                @click="() => $parent.$emit('delete', props.row)"
            />
        </q-td>
        <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit v-model="props.row.name" v-slot="scope"
                @update:model-value="() => $parent.$emit('rename', props.row)"
            >
                <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
        </q-td>
        <q-td key="age" :props="props">
            {{ props.row.age }}
            <q-popup-edit v-model="props.row.age" v-slot="scope" 
                @update:model-value="() => $parent.$emit('rename', props.row)"
            >
                <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
        </q-td>
    </q-tr>
''')
with table.add_slot('bottom-row'):
    with table.cell().props('colspan=3'):
        ui.button('Add row', icon='add', color='accent', on_click=add_row).classes('w-full')
table.on('rename', rename)
table.on('delete', delete)

ui.run()
