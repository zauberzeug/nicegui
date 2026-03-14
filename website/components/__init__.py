from . import (
    about,
    cta_banner,
    demos,
    examples_section,
    features,
    footer,
    hero,
    installation,
    sponsors_section,
    why_section,
)

__all__ = [
    'about',
    'cta_banner',
    'demos',
    'examples_section',
    'features',
    'footer',
    'hero',
    'installation',
    'sponsors_section',
    'why_section',
]

SCROLL_REVEAL_JS = '''
<script>
document.addEventListener('DOMContentLoaded', function() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('mo-visible');
    });
  }, { threshold: 0.1 });
  function observeAll() {
    document.querySelectorAll('.mo-reveal').forEach((el) => {
      if (!el.dataset.moObserved) {
        el.dataset.moObserved = '1';
        observer.observe(el);
      }
    });
  }
  observeAll();
  new MutationObserver(observeAll).observe(document.body, { childList: true, subtree: true });
});
</script>
'''
