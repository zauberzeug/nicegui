import weakref

from ..context import context
from ..element import Element
from .mixins.text_element import TextElement


class SkipLink(TextElement, default_classes='nicegui-skip-link'):

    def __init__(self, text: str = 'Skip to main content', *, target: Element) -> None:
        """Skip link

        A keyboard-only "skip link" that is hidden until it receives focus via Tab
        and moves keyboard focus to ``target`` when activated.
        It lets keyboard users bypass repetitive navigation,
        satisfying `WCAG 2.4.1 "Bypass Blocks" <https://www.w3.org/WAI/WCAG21/Understanding/bypass-blocks.html>`_.

        Rendered as an ``<a href="#...">`` element so the browser handles fragment navigation natively;
        an additional click handler sets ``tabindex="-1"`` on the target
        so non-focusable elements (e.g. a ``<div>``) still receive focus.

        The link is automatically moved to the top of the page layout so it is the first element the keyboard reaches.
        Multiple skip links are kept in creation order.

        Pass ``text=''`` and use the element as a context manager
        to supply custom child content (e.g. an icon next to a label).

        The target is resolved by its ID captured at creation time,
        so ``target`` should be a stable container rather than transient content that is recreated
        (e.g. by a refreshable or a sub-page route change), otherwise the link silently does nothing.

        *Added in version 3.13.0*

        :param text: the link label (default: "Skip to main content")
        :param target: the element to move focus to when the link is activated
        """
        with context.client.layout:
            super().__init__(tag='a', text=text)
        # Move the link to the top of the layout so it is the first focusable element.
        # If the only siblings are other skip links, the link stays where ``super().__init__`` appended it
        # (last among skip links), which is the correct creation order.
        assert self.parent_slot is not None
        for index, child in enumerate(self.parent_slot.children):
            if not isinstance(child, SkipLink):
                self.move(target_index=index)
                break
        # canary in the calling context so the link is deleted when its parent is cleared
        # (e.g. a sub_pages route change), matching the lifecycle of ui.dialog
        canary = Element()
        canary.visible = False
        weakref.finalize(
            canary, lambda: self.delete() if not self.is_deleted and self._parent_slot and self._parent_slot() else None
        )
        self._props['href'] = f'#{target.html_id}'
        self.on('click', js_handler='''(e) => {
            const el = getHtmlElement(e.currentTarget.hash.slice(1));
            if (el === null) return;
            el.setAttribute('tabindex', '-1');
            el.focus();
        }''')
