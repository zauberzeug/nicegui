from ..dependencies import register_component
from ..element import Element

register_component("html_table", __file__, "html_table.js")


def parser_style(table):
    m_style = ["<style>"]

    for key in table._style.keys():
        m_style.append(key + " {" + table._style[key] + "}")

    m_style.append("</style>")
    return "\n".join(m_style)


def parser_columns(table):
    m_thead = ["<thead><tr>"]

    for col in table._columns:
        m_thead.append(f"<th>{col}</th>")

    m_thead.append("</tr></thead>")
    return "\n".join(m_thead)


def parser_rows(table):
    m_tbody = ["<tbody>"]

    for row in table._rows:
        m_data = ["<tr>"]
        for col in row.keys():
            m_data.append(f"<td>{row[col]}</td>")
        m_data.append("</tr>")
        m_tbody.append("\n".join(m_data))

    m_tbody.append("</tbody>")
    return "\n".join(m_tbody)


class HTMLTable(Element):
    def __init__(self, columns=[], rows=[], style={}):
        """HTML Table

        A simple HTML table that can be used to display a table of data.

        :param columns: A list of column names. Exemple: ['Name', 'Age']
        :param rows: A list of dicionaries of data for each column. Exemple: [{'name': 'John', 'age': '30'}, {'name': 'Mary', 'age': '40'}]
        :param style: A dictionary of CSS styles. Exemple: {'table': 'width:100%', 'tr': 'background-color:red;'}

        API to update data:

        :method sync_config: passes the current columns, rows and style values ​​to the component and emits the update_dom event.
        """
        super().__init__("html_table")

        self._columns = columns
        self._rows = rows
        self._style = style

        self.sync_config()

    def sync_config(self):
        data = f"{parser_columns(self)} {parser_rows(self)} {parser_style(self)}"
        self._props["table_config"] = data
        self.update()
