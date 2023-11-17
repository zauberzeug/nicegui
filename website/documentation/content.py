from .sections import (action_events, audiovisual_elements, binding_properties, configuration_deployment, controls,
                       data_elements, page_layout, styling_appearance, text_elements)
from .tools import heading


def create_full() -> None:
    heading('Text Elements')
    text_elements.content()

    heading('Controls')
    controls.content()

    heading('Audiovisual Elements')
    audiovisual_elements.content()

    heading('Data Elements')
    data_elements.content()

    heading('Binding Properties')
    binding_properties.content()

    heading('Page Layout')
    page_layout.content()

    heading('Styling and Appearance')
    styling_appearance.content()

    heading('Action Events')
    action_events.content()

    heading('Configuration and Deployment')
    configuration_deployment.content()
