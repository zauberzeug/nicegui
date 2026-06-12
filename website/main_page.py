from nicegui import ui

from .components import (
    about_section,
    cta_section,
    demos_section,
    examples_section,
    features_section,
    hero_section,
    installation_section,
    sponsors_section,
    why_section,
)


def create() -> None:
    """Create the content of the main page."""
    ui.run_javascript('''
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) entry.target.classList.add('visible');
            });
        }, { threshold: 0.1 });
        function observeAll() {
            document.querySelectorAll('.reveal').forEach((el) => {
                if (!el.dataset.moObserved) {
                    el.dataset.moObserved = '1';
                    observer.observe(el);
                }
            });
        }
        observeAll();
        new MutationObserver(observeAll).observe(document.body, { childList: true, subtree: true });
    ''')

    hero_section.create()
    about_section.create()
    installation_section.create()
    features_section.create()
    demos_section.create()
    cta_section.create()
    examples_section.create()
    sponsors_section.create()
    why_section.create()
