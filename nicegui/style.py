class Style:
    """
    Represents the style properties for a UI element.

    Args:
        alignment (str): The alignment of the UI element.
        size (str): The size of the UI element.
        color (str): The color of the UI element.
        icon (str): The icon of the UI element.
        font (str): The font of the UI element.
        text_align (str): The text alignment of the UI element.
        gap (str): The gap between UI elements.

    Attributes:
        alignment (str): The alignment of the UI element.
        size (str): The size of the UI element.
        color (str): The color of the UI element.
        icon (str): The icon of the UI element.
        font (str): The font of the UI element.
        text_align (str): The text alignment of the UI element.
        gap (str): The gap between UI elements.
    """

    def __init__(
        self,
        alignment: str = None,
        size: str = None,
        bgcolor: str = None,
        text_color: str = None,
        # icon: str = None,
        font: str = None,
        text_align: str = None,
        gap: str = None,
    ):
        self.alignment = alignment
        self.size = size
        self.bgcolor = "background: " + bgcolor
        self.text_color = "color: " + text_color
        # self.icon = icon
        self.font = font
        self.text_align = text_align
        self.gap = gap

    def __repr__(self):
        return f"""
        {"; ".join(filter(None, [
                self.alignment,
                self.size,
                self.bgcolor,
                self.text_color,
                self.font,
                self.text_align,
                self.gap
                ]
            )
            )
        }
        """
