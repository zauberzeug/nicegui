from . import (
    chat_message_documentation,
    doc,
    element_documentation,
    html_documentation,
    label_documentation,
    link_documentation,
    markdown_documentation,
    mermaid_documentation,
    restructured_text_documentation,
)
from .html_documentation import other_html_elements_description, other_html_elements_title, other_html_elements

doc.title('*Text* Elements')

doc.intro(label_documentation)
doc.intro(link_documentation)
doc.intro(chat_message_documentation)
doc.intro(element_documentation)
doc.intro(markdown_documentation)
doc.intro(restructured_text_documentation)
doc.intro(mermaid_documentation)
doc.intro(html_documentation)
doc.demo(other_html_elements_title, other_html_elements_description)(other_html_elements)
