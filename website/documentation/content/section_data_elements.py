from nicegui import optional_features

from . import (aggrid_documentation, circular_progress_documentation, code_documentation, doc, echart_documentation,
               editor_documentation, fullcalendar_documentation, highchart_documentation, json_editor_documentation,
               leaflet_documentation, line_plot_documentation, linear_progress_documentation, log_documentation,
               plotly_documentation, pyplot_documentation, scene_documentation, spinner_documentation,
               table_documentation, tree_documentation)

doc.title('*Data* Elements')

doc.intro(table_documentation)
doc.intro(aggrid_documentation)
if optional_features.has('highcharts'):
    doc.intro(highchart_documentation)
doc.intro(echart_documentation)
if optional_features.has('matplotlib'):
    doc.intro(pyplot_documentation)
    doc.intro(line_plot_documentation)
if optional_features.has('plotly'):
    doc.intro(plotly_documentation)
doc.intro(linear_progress_documentation)
doc.intro(circular_progress_documentation)
doc.intro(spinner_documentation)
doc.intro(scene_documentation)
doc.intro(leaflet_documentation)
doc.intro(tree_documentation)
doc.intro(log_documentation)
doc.intro(editor_documentation)
doc.intro(code_documentation)
doc.intro(json_editor_documentation)
doc.intro(fullcalendar_documentation)
