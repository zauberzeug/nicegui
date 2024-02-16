from typing import Any, Callable, Dict, List, Optional, Union

from .mixins.value_element import ValueElement


class ChoiceElement(ValueElement):
    """
    Represents a choice element in a GUI, allowing the user to select from a list of options.

    Args:
        tag (str, optional): The tag associated with the element. Defaults to None.
        options (list or dict): The options available for selection. Can be a list of values or a dictionary
            mapping values to labels.
        value (any): The initial value of the choice element.
        on_change (callable, optional): A function to be called when the value of the choice element changes.
            Defaults to None.

    Attributes:
        - options (list or dict): The options available for selection.
        - _values (list): The values corresponding to the options.
        - _labels (list): The labels corresponding to the options.

    Methods:
        - _update_values_and_labels(): Updates the values and labels based on the options.
        - _update_options(): Updates the options based on the values and labels.
        - update(): Updates the choice element.
        - set_options(options, value=None): Sets the options of the choice element.

    """

    def __init__(self, *,
                     tag: Optional[str] = None,
                     options: Union[List, Dict],
                     value: Any,
                     on_change: Optional[Callable[..., Any]] = None,
                     ) -> None:
            """
            Choice Element

            Args:
                - tag (Optional[str]): An optional tag for the element.
                - options (Union[List, Dict]): The options for the choice element. It can be a list or a dictionary.
                - value (Any): The initial value for the choice element.
                - on_change (Optional[Callable[..., Any]]): An optional callback function to be called when the value of the
                    choice element changes.

            Raises:
                - TypeError: If the options parameter is not a list or a dictionary.

            """
            self.options = options
            self._values: List[str] = []
            self._labels: List[str] = []
            self._update_values_and_labels()
            super().__init__(tag=tag, value=value, on_value_change=on_change)
            self._update_options()

    def _update_values_and_labels(self) -> None:
        """
        Updates the values and labels based on the options.

        This method updates the internal values and labels of the ChoiceElement
        based on the provided options. If the options are a list, the values and
        labels are set to be the same as the options. If the options are a
        dictionary, the keys are used as values and the values are used as labels.

        This method should be called whenever the options of the ChoiceElement
        are modified to ensure that the values and labels are up to date.

        Returns:
            None
        """
        self._values = self.options if isinstance(self.options, list) else list(self.options.keys())
        self._labels = self.options if isinstance(self.options, list) else list(self.options.values())

    def _update_options(self) -> None:
        """
        Updates the options based on the values and labels.

        This method updates the options of the ChoiceElement based on the values and labels provided.
        It creates a list of dictionaries, where each dictionary represents an option with a value and a label.
        The value is the index of the option in the labels list, and the label is the corresponding label.

        The method also handles the preservation of the selected value before the options are updated.
        It stores the value before the update in the `before_value` variable.
        After updating the options, it sets the `options` property of the ChoiceElement to the new list of dictionaries.
        If the previous value was not a list, it converts it to the corresponding model value using the `_value_to_model_value` method.
        Finally, it sets the value of the ChoiceElement to the preserved value if it is still valid, otherwise it sets it to None.

        Usage:
        ```
        choice_element._update_options()
        ```

        :return: None
        """
        before_value = self.value
        self._props['options'] = [{'value': index, 'label': option} for index, option in enumerate(self._labels)]
        if not isinstance(before_value, list):
            self._props[self.VALUE_PROP] = self._value_to_model_value(before_value)
            self.value = before_value if before_value in self._values else None

    def update(self) -> None:
        """
        Updates the choice element.

        This method updates the choice element by performing the following steps:
        1. Updates the values and labels of the choice element.
        2. Updates the options of the choice element.
        3. Calls the base class's update method to perform any additional updates.

        This method should be called whenever the choice element needs to be updated with new values or options.

        :return: None
        """
        self._update_values_and_labels()
        self._update_options()
        super().update()

    def set_options(self, options: Union[List, Dict], *, value: Any = None) -> None:
        """
        Set the options of this choice element.

        This method allows you to update the options of a choice element. The options can be provided as a list or a dictionary.
        If a value is specified, it will also update the current value of the choice element.

        Args:
            options (list or dict): The new options for the choice element. If a list is provided, each item in the list will be treated as an option.
                                    If a dictionary is provided, the keys will be treated as option values and the values as option labels.
            value (any, optional): The new value for the choice element. If not given, the current value is kept.

        Returns:
            None

        Example usage:
            # Update options with a list
            set_options(['Option 1', 'Option 2', 'Option 3'])

            # Update options with a dictionary
            set_options({1: 'Option 1', 2: 'Option 2', 3: 'Option 3'}, value=2)
        """
        self.options = options
        if value is not None:
            self.value = value
        self.update()
