from ...model import SectionDocumentation
from ...more.label_documentation import LabelDocumentation


class TextElementsDocumentation(SectionDocumentation, title='Text Elements', name='text_elements'):

    def content(self) -> None:
        self.add_element_intro(LabelDocumentation())
