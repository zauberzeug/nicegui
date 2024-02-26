
class Style:
    """
    Represents the style properties for a GUI element.

    Args:
        alignment (str): The alignment of the element.
        size (str): The size of the element.
        width (str): The width of the element.
        height (str): The height of the element.
        display (str): The display property of the element.
        position (str): The position property of the element.
        margin (str): The margin property of the element.
        padding (str): The padding property of the element.
        border (str): The border property of the element.
        border_radius (str): The border-radius property of the element.
        box_shadow (str): The box-shadow property of the element.
        bgcolor (str): The background color of the element.
        text_color (str): The text color of the element.
        font (str): The font property of the element.
        text_align (str): The text alignment of the element.
        gap (str): The gap property of the element.
    """

    def __init__(
        self,
        alignment: str = "",
        size: str = "",
        width: str = "",
        height: str = "",
        display: str = "",
        position: str = "",
        margin: str = "",
        padding: str = "",
        border: str = "",
        border_radius: str = "",
        box_shadow: str = "",
        bgcolor: str = "",
        text_color: str = "",
        font: str = "",
        text_align: str = "",
        gap: str = "",
    ):
        """
        Initializes a new instance of the Style class.

        Args:
            alignment (str): The alignment of the element.
            size (str): The size of the element.
            width (str): The width of the element.
            height (str): The height of the element.
            display (str): The display property of the element.
            position (str): The position property of the element.
            margin (str): The margin property of the element.
            padding (str): The padding property of the element.
            border (str): The border property of the element.
            border_radius (str): The border-radius property of the element.
            box_shadow (str): The box-shadow property of the element.
            bgcolor (str): The background color of the element.
            text_color (str): The text color of the element.
            font (str): The font property of the element.
            text_align (str): The text alignment of the element.
            gap (str): The gap property of the element.
        """
        self.alignment = alignment
        self.size = size
        self.width = "width: " + width if width and "width" not in width else ""
        self.height = "height: " + height if height and "height" not in height else ""
        self.display = "display: " + display if display and "display" not in display else ""
        self.position = "position: " + position if position and "position" not in position else ""
        self.margin = "margin: " + margin if margin and "margin" not in margin else ""
        self.padding = "padding: " + padding if padding and "padding" not in padding else ""
        self.border = "border: " + border if border and "border" not in border else ""
        self.border_radius = "border-radius: " + border_radius if border_radius and "border-radius" not in border_radius else ""
        self.box_shadow = "box-shadow: " + box_shadow if box_shadow and "box-shadow" not in box_shadow else ""
        self.bgcolor = "background: " + bgcolor if bgcolor and "background" not in bgcolor else ""
        self.text_color = "color: " + text_color if text_color and "color" not in text_color else ""
        self.font = "font: " + font if font and "font" not in font else ""
        self.text_align = "text-align: " + text_align if text_align and "text-align" not in text_align else ""
        self.gap = "gap: " + gap if gap and "gap" not in gap else ""

    def __repr__(self):
        """
        Returns a string representation of the Style object.

        Returns:
            str: The string representation of the Style object.
        """
        return f"""
        {"; ".join(filter(None, [
                self.alignment,
                self.size,
                self.width,
                self.height,
                self.display,
                self.position,
                self.margin,
                self.padding,
                self.border,
                self.border_radius,
                self.box_shadow,
                self.bgcolor,
                self.text_color,
                self.font,
                self.text_align,
                self.gap,
                ]
            )
            )
        }
        """
