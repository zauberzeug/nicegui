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
        self.add_element_intro(ButtonDocumentation())
        self.add_element_intro(BadgeDocumentation())
        self.add_element_intro(ToggleDocumentation())
        self.add_element_intro(RadioDocumentation())
        self.add_element_intro(SelectDocumentation())
        self.add_element_intro(CheckboxDocumentation())
        self.add_element_intro(SwitchDocumentation())
        self.add_element_intro(SliderDocumentation())
        self.add_element_intro(JoystickDocumentation())
        self.add_element_intro(InputDocumentation())
        self.add_element_intro(TextareaDocumentation())
        self.add_element_intro(NumberDocumentation())
        self.add_element_intro(KnobDocumentation())
        self.add_element_intro(ColorInputDocumentation())
        self.add_element_intro(ColorPickerDocumentation())
        self.add_element_intro(DateDocumentation())
        self.add_element_intro(TimeDocumentation())
        self.add_element_intro(UploadDocumentation())
