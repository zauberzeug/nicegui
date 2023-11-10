from nicegui import ui

data = [
    {"id": 0, "name": "Alice", "age": 18},
    {"id": 1, "name": "Bob", "age": 21},
    {"id": 2, "name": "Carol", "age": 20},
]


def update_data_from_table_change(e):
    ui.notify(f"Update with {e.args['data'] }")
    uprow = e.args["data"]
    data[:] = [row | uprow if row["id"] == uprow["id"] else row for row in data]


table = ui.aggrid(
    {
        "columnDefs": [
            {"field": "name", "editable": True, "sortable": True},
            {"field": "age", "editable": True},
            {"field": "id"},
        ],
        "rowData": data,
        "rowSelection": "multiple",
        "stopEditingWhenCellsLoseFocus": True,
    }
).on("cellValueChanged", update_data_from_table_change)


async def delete_selected():
    result = [row["id"] for row in await table.get_selected_rows()]
    ui.notify(f"delete rows {result}")
    data[:] = [row for row in data if row["id"] not in result]
    table.update()


def new_row():
    newid = max(dx["id"] for dx in data) + 1
    ui.notify(f"new row with id {newid}")
    data.append({"id": newid, "name": "New name", "age": None})
    table.update()


ui.button("Delete selected", on_click=delete_selected)
ui.button("New row", on_click=new_row)
ui.label().classes("whitespace-pre font-mono").bind_text_from(
    globals(), "data", lambda x: "Data: \n{0}".format("\n".join([str(y) for y in x]))
)
ui.run()
