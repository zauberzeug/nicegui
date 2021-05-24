import markdown2
from .html import Html
import re

class Markdown(Html):

    def __init__(self,
                 content: str = '',
                 ):
        """Markdown Element

        Renders markdown onto the page.

        :param content: the markdown content to be displayed
        """

        super().__init__(content)

    def set_content(self, content: str):

        html = markdown2.markdown(content, extras=['fenced-code-blocks'])
        # we need explicit markdown styling because tailwind css removes all default styles
        html = Markdown.apply_tailwind(html)
        super().set_content(html)

    @staticmethod
    def apply_tailwind(html: str):

        rep = {
            '<h1': '<h1 class="text-5xl mb-4 mt-6"',
            '<h2': '<h2 class="text-4xl mb-3 mt-5"',
            '<h3': '<h3 class="text-3xl mb-2 mt-4"',
            '<h4': '<h4 class="text-2xl mb-1 mt-3"',
            '<h5': '<h5 class="text-1xl mb-0.5 mt-2"',
            '<a': '<a class="underline text-blue-600 hover:text-blue-800 visited:text-purple-600"',
            '<ul': '<ul class="list-disc ml-6"',
            '<p>': '<p class="mb-2">',
            '<div\ class="codehilite">': '<div class=" codehilite mb-2 p-2" style="overflow: scroll">',
            '<code': '<code style="background-color: #f8f8f8"',
        }
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], html)
