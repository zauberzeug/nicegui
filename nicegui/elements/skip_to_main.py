from ..context import context
from .mixins.text_element import TextElement


class SkipToMain(TextElement, default_classes='nicegui-skip-to-main'):

    def __init__(self) -> None:
        """Skip to main content

        An accessibility button that is hidden until focused via keyboard (Tab).
        It allows keyboard users to skip navigation and jump directly to the main content.

        Optionally, use it as a context manager to customize text and styling.

        Note: The skip button is automatically placed before other layout elements in the DOM,
        with the exception of other skip buttons, which are placed in-order-of-creation.
        """
        with context.client.layout:
            super().__init__(tag='button', text='Skip to main content')

        assert self.parent_slot is not None
        for i, element in enumerate(self.parent_slot.children):
            if not isinstance(element, SkipToMain):
                self.move(target_index=i)
                break

        self.on('click', js_handler='''(e) => {
            const el = document.getElementById('c' + e.target.dataset.target);
            el.setAttribute('tabindex', '-1');
            el.focus();
        }''')
        self._props['data-target'] = self.client.next_element_id

    def __exit__(self, *_):
        self.text = ''
        self._props['data-target'] = self.client.next_element_id
        return super().__exit__(*_)
