from ...model import SectionDocumentation
from ...more.badge_documentation import BadgeDocumentation
from ...more.button_documentation import ButtonDocumentation
from ...more.checkbox_documentation import CheckboxDocumentation
from ...more.color_input_documentation import ColorInputDocumentation
from ...more.color_picker_documentation import ColorPickerDocumentation
from ...more.date_documentation import DateDocumentation
from ...more.input_documentation import InputDocumentation
from ...more.joystick_documentation import JoystickDocumentation
from ...more.knob_documentation import KnobDocumentation
from ...more.number_documentation import NumberDocumentation
from ...more.radio_documentation import RadioDocumentation
from ...more.select_documentation import SelectDocumentation
from ...more.slider_documentation import SliderDocumentation
from ...more.switch_documentation import SwitchDocumentation
from ...more.textarea_documentation import TextareaDocumentation
from ...more.time_documentation import TimeDocumentation
from ...more.toggle_documentation import ToggleDocumentation
from ...more.upload_documentation import UploadDocumentation


class ControlsDocumentation(SectionDocumentation, title='*Controls*', name='controls'):

    def content(self) -> None:
        self.intro(ButtonDocumentation())
        self.intro(BadgeDocumentation())
        self.intro(ToggleDocumentation())
        self.intro(RadioDocumentation())
        self.intro(SelectDocumentation())
        self.intro(CheckboxDocumentation())
        self.intro(SwitchDocumentation())
        self.intro(SliderDocumentation())
        self.intro(JoystickDocumentation())
        self.intro(InputDocumentation())
        self.intro(TextareaDocumentation())
        self.intro(NumberDocumentation())
        self.intro(KnobDocumentation())
        self.intro(ColorInputDocumentation())
        self.intro(ColorPickerDocumentation())
        self.intro(DateDocumentation())
        self.intro(TimeDocumentation())
        self.intro(UploadDocumentation())
