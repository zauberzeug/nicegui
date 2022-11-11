import justpy as jp


class CustomView(jp.JustpyBaseComponent):

    def __init__(self, vue_type, **options):
        self.vue_type = vue_type

        self.pages = {}
        self.classes = ''
        self.style = ''
        self.options = jp.Dict(**options)
        self.components = []

        super().__init__(temp=False)

    def react(self, _):
        pass

    def convert_object_to_dict(self):
        return {
            'vue_type': self.vue_type,
            'id': self.id,
            'show': True,
            'classes': self.classes,
            'style': self.style,
            'options': self.options,
        }
