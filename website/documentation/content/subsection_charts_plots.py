from nicegui import optional_features

from . import (
    altair_documentation,
    anywidget_documentation,
    doc,
    echart_documentation,
    highchart_documentation,
    line_plot_documentation,
    matplotlib_documentation,
    plotly_documentation,
    pyplot_documentation,
)

doc.title('Charts')

if optional_features.has('highcharts'):
    doc.intro(highchart_documentation)
doc.intro(echart_documentation)
if optional_features.has('matplotlib'):
    doc.intro(pyplot_documentation)
    doc.intro(matplotlib_documentation)
    doc.intro(line_plot_documentation)
if optional_features.has('plotly'):
    doc.intro(plotly_documentation)
if optional_features.has('altair'):
    doc.intro(altair_documentation)
if optional_features.has('anywidget'):
    doc.intro(anywidget_documentation)
