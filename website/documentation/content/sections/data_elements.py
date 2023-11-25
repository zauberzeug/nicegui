from nicegui import optional_features

from ...model import SectionDocumentation
from ..more.aggrid_documentation import AgGridDocumentation
from ..more.circular_progress_documentation import CircularProgressDocumentation
from ..more.code_documentation import CodeDocumentation
from ..more.echart_documentation import EChartDocumentation
from ..more.editor_documentation import EditorDocumentation
from ..more.highchart_documentation import HighchartDocumentation
from ..more.json_editor_documentation import JsonEditorDocumentation
from ..more.line_plot_documentation import LinePlotDocumentation
from ..more.linear_progress_documentation import LinearProgressDocumentation
from ..more.log_documentation import LogDocumentation
from ..more.plotly_documentation import PlotlyDocumentation
from ..more.pyplot_documentation import PyplotDocumentation
from ..more.scene_documentation import SceneDocumentation
from ..more.spinner_documentation import SpinnerDocumentation
from ..more.table_documentation import TableDocumentation
from ..more.tree_documentation import TreeDocumentation


class DataElementsDocumentation(SectionDocumentation, title='*Data* elements', name='data_elements'):

    def content(self) -> None:
        self.intro(TableDocumentation())
        self.intro(AgGridDocumentation())
        if optional_features.has('highcharts'):
            self.intro(HighchartDocumentation())
        self.intro(EChartDocumentation())
        if optional_features.has('matplotlib'):
            self.intro(PyplotDocumentation())
            self.intro(LinePlotDocumentation())
        if optional_features.has('plotly'):
            self.intro(PlotlyDocumentation())
        self.intro(LinearProgressDocumentation())
        self.intro(CircularProgressDocumentation())
        self.intro(SpinnerDocumentation())
        self.intro(SceneDocumentation())
        self.intro(TreeDocumentation())
        self.intro(LogDocumentation())
        self.intro(EditorDocumentation())
        self.intro(CodeDocumentation())
        self.intro(JsonEditorDocumentation())
