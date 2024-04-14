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
    new_id = max((dx['id'] for dx in rows), default=-1) + 1
    rows.append({'id': new_id, 'name': 'New guy', 'age': 21})
    ui.notify(f'Added new row with ID {new_id}')
    table.update()


def rename(e: events.GenericEventArguments) -> None:
    for row in rows:
        if row['id'] == e.args['id']:
            row.update(e.args)
    ui.notify(f'Updated rows to: {table.rows}')
    table.update()


def delete(e: events.GenericEventArguments) -> None:
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
