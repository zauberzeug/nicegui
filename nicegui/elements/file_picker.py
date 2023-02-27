from ..dependencies import register_component
from ..element import Element

register_component("file_picker", __file__, "file_picker.js")


class FilePicker(Element):
    def __init__(self, label="File...", multiple=False, accept_types=[""]) -> None:
        """File Picker

        A component which handles the user interaction for picking file

        :param label: A text label that will “float” up above the input field, once the field gets focus
        :param multiple: Whether or not to allow multiple files to be selected
        :param accept_types: A list of file types to accept

        API to get information from the selected file:

        :event file_pick: Triggered when the user selects a file
        :return: List of dicitionaries with the following keys: name, size, type, url, last_modified
        :save: This list is saved in file property of the component
        """
        super().__init__("file_picker")

        self._props["label"] = label
        self._props["multiple"] = multiple
        self._props["accept"] = ", ".join(accept_types)

        self.file = {"name": "", "size": "", "type": "", "url": "", "last_modified": ""}
        self.on("file_pick", self.handle_file_pick)

    def handle_file_pick(self, data) -> None:
        self.file = data["args"]
