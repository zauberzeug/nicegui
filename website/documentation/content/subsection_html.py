from . import (
    doc,
    element_documentation,
    html_documentation,
)
from .html_documentation import other_html_elements, other_html_elements_description, other_html_elements_title

doc.title('HTML')

doc.intro(element_documentation)
doc.intro(html_documentation)

doc.demo(other_html_elements_title, other_html_elements_description)(other_html_elements)
