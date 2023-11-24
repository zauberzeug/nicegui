from ...model import SectionDocumentation
from ...more.chat_message_documentation import ChatMessageDocumentation
from ...more.element_documentation import ElementDocumentation
from ...more.html_documentation import HtmlDocumentation
from ...more.label_documentation import LabelDocumentation
from ...more.link_documentation import LinkDocumentation
from ...more.markdown_documentation import MarkdownDocumentation
from ...more.mermaid_documentation import MermaidDocumentation


class TextElementsDocumentation(SectionDocumentation, title='*Text* Elements', name='text_elements'):

    def content(self) -> None:
        self.add_element_intro(LabelDocumentation())
        self.add_element_intro(LinkDocumentation())
        self.add_element_intro(ChatMessageDocumentation())
        self.add_element_intro(ElementDocumentation())
        self.add_element_intro(MarkdownDocumentation())
        self.add_element_intro(MermaidDocumentation())
        self.add_element_intro(HtmlDocumentation())
