from nicegui import ui

from ..example import example


def more_examples():
    @example('''#### Table with expandable rows

Scoped slots can be used to insert buttons that toggle the expand state of a table row.
See the [Quasar documentation](https://quasar.dev/vue-components/table#expanding-rows) for more information.
''', None)
    def table_with_expandable_rows():
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'age', 'label': 'Age', 'field': 'age'},
        ]
        rows = [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol'},
        ]

        with ui.table(columns=columns, rows=rows, row_key='name').classes('w-72') as table:
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
                    <q-td auto-width>
                        <q-btn size="sm" color="accent" round dense
                            @click="props.expand = !props.expand"
                            :icon="props.expand ? 'remove' : 'add'" />
                    </q-td>
                    <q-td v-for="col in props.cols" :key="col.name" :props="props">
                        {{ col.value }}
                    </q-td>
                </q-tr>
                <q-tr v-show="props.expand" :props="props">
                    <q-td colspan="100%">
                        <div class="text-left">This is {{ props.row.name }}.</div>
                    </q-td>
                </q-tr>
            ''')
