from ..element import Element


class content:
    def __init__(self, parent):
        self.parent = parent

    def icon(self, icon: str):
        """[icon]: String

        Description: Icon name following Quasar convention; Make sure you have the icon library installed unless you are using 'img:' prefix; If 'none' (String) is used as value then no icon is rendered (but screen real estate will still be used for it)

        Examples: [map] [ion-add] [img:https://cdn.quasar.dev/logo-v2/svg/logo.svg] [img:path/to/some_image.png]
        """
        self.parent._props["icon"] = icon
        return self


class style:
    def __init__(self, parent):
        self.parent = parent

    def size(self, size: str):
        """[size]: String

        Description: Size in CSS units, including unit name or standard size name (xs|sm|md|lg|xl)

        Examples: [16px] [2rem] [xs] [md]"""
        self.parent._props["size"] = size
        return self

    def font_size(self, font_size: str):
        """[font-size]: String

        Description: The size in CSS units, including unit name, of the content (icon, text)

        Examples: [18px] [2rem]"""
        self.parent._props["font-size"] = font_size
        return self

    def color(self, color: str):
        """[color]: String

        Description: Color name for component from the Quasar Color Palette

        Examples: [primary] [teal-10]"""
        self.parent._props["color"] = color
        return self

    def text_color(self, text_color: str):
        """[text-color]: String

        Description: Overrides text color (if needed); Color name from the Quasar Color Palette

        Examples: [primary] [teal-10]"""
        self.parent._props["text-color"] = text_color
        return self

    def square(self, square: bool):
        """[square]: Boolean

        Description: Removes border-radius so borders are squared"""
        self.parent._props["square"] = square
        return self

    def rounded(self, rounded: bool):
        """[rounded]: Boolean

        Description: Applies a small standard border-radius for a squared shape of the component
        """
        self.parent._props["rounded"] = rounded
        return self


class Avatar(Element):
    def __init__(self, icon: str = "") -> None:
        """Avatar

        A avatar element wrapping Quasar's
        `QAvatar <https://quasar.dev/vue-components/avatar>`_ component.

        :param icon: the name of the icon or icon path (img:path/to/some_image.png)

        `Here <https://material.io/icons/>`_ is a reference of possible names.

        :param .qstyle: namespace with all styling functions.

        `Styles <https://quasar.dev/vue-components/avatar>`_ all styles available for editing the component.
        """
        super().__init__("q-avatar")
        self._props["icon"] = icon

        self.qcontent = content(self)
        self.qstyle = style(self)
