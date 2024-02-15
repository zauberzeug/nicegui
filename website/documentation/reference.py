import inspect
import re
from typing import Callable, Optional

import docutils.core

from nicegui import binding, ui

from ..style import create_anchor_name, subheading


def generate_class_doc(class_obj: type, part_title: str) -> None:
    """
    Generate documentation for a class including all its methods and properties.

    Args:
        class_obj (type): The class object for which to generate documentation.
        part_title (str): The title of the part of the documentation.

    Returns:
        None

    This function generates documentation for a class by inspecting its methods and properties.
    It organizes the documentation into sections for properties, methods, and inheritance.

    The generated documentation includes the following information for each property:
    - Property name
    - Property signature description
    - Property docstring (if available)

    The generated documentation includes the following information for each method:
    - Method name
    - Method signature description
    - Method docstring (if available)
    - Method decorator (if applicable)

    The generated documentation also includes a section for inheritance, listing the class's ancestors.

    Example usage:
    ```
    class MyClass:
        def my_method(self):
            pass

    generate_class_doc(MyClass, "MyClass Reference")
    ```

    Note: This function assumes that the class and its ancestors are defined within the 'nicegui' module.
    """
    mro = [base for base in class_obj.__mro__ if base.__module__.startswith('nicegui.')]
    ancestors = mro[1:]
    attributes = {}
    for base in reversed(mro):
        for name in dir(base):
            if not name.startswith('_') and _is_method_or_property(base, name):
                attributes[name] = getattr(base, name, None)
    properties = {name: attribute for name, attribute in attributes.items() if not callable(attribute)}
    methods = {name: attribute for name, attribute in attributes.items() if callable(attribute)}

    if properties:
        subheading('Properties', anchor_name=create_anchor_name(part_title.replace('Reference', 'Properties')))
        with ui.column().classes('gap-2'):
            for name, property_ in sorted(properties.items()):
                ui.markdown(f'**`{name}`**`{_generate_property_signature_description(property_)}`')
                if property_.__doc__:
                    _render_docstring(property_.__doc__).classes('ml-8')
    if methods:
        subheading('Methods', anchor_name=create_anchor_name(part_title.replace('Reference', 'Methods')))
        with ui.column().classes('gap-2'):
            for name, method in sorted(methods.items()):
                decorator = ''
                if isinstance(class_obj.__dict__.get(name), staticmethod):
                    decorator += '`@staticmethod`<br />'
                if isinstance(class_obj.__dict__.get(name), classmethod):
                    decorator += '`@classmethod`<br />'
                ui.markdown(f'{decorator}**`{name}`**`{_generate_method_signature_description(method)}`')
                if method.__doc__:
                    _render_docstring(method.__doc__).classes('ml-8')
    if ancestors:
        subheading('Inheritance', anchor_name=create_anchor_name(part_title.replace('Reference', 'Inheritance')))
        ui.markdown('\n'.join(f'- `{ancestor.__name__}`' for ancestor in ancestors))


def _is_method_or_property(cls: type, attribute_name: str) -> bool:
    """
    Check if the given attribute of a class is a method or property.

    Args:
        cls (type): The class to check the attribute against.
        attribute_name (str): The name of the attribute to check.

    Returns:
        bool: True if the attribute is a method or property, False otherwise.

    Notes:
        This function checks if the attribute is a function, method, staticmethod,
        classmethod, property, or a binding.BindableProperty.

    Example:
        class MyClass:
            def my_method(self):
                pass

            @property
            def my_property(self):
                return 42

        _is_method_or_property(MyClass, 'my_method')  # True
        _is_method_or_property(MyClass, 'my_property')  # True
        _is_method_or_property(MyClass, 'nonexistent')  # False
    """
    attribute = cls.__dict__.get(attribute_name, None)
    return (
        inspect.isfunction(attribute) or
        inspect.ismethod(attribute) or
        isinstance(attribute, (
            staticmethod,
            classmethod,
            property,
            binding.BindableProperty,
        ))
    )


def _generate_property_signature_description(property_: Optional[property]) -> str:
    """
    Generate a description for a property's signature.

    This function takes a property object as input and generates a description
    for its signature. The description includes information about the return type,
    whether the property is settable or deletable, and whether it is a bindable property.

    Parameters:
        property_ (property): The property object for which to generate the description.

    Returns:
        str: The generated description for the property's signature.

    Example:
        >>> class MyClass:
        ...     @property
        ...     def my_property(self) -> int:
        ...         return self._my_property
        ...
        ...     @my_property.setter
        ...     def my_property(self, value: int):
        ...         self._my_property = value
        ...
        ...     @my_property.deleter
        ...     def my_property(self):
        ...         del self._my_property
        ...
        >>> prop = MyClass.my_property
        >>> _generate_property_signature_description(prop)
        ': int (settable) (deletable)'
    """
    description = ''
    if property_ is None:
        return ': BindableProperty'
    if property_.fget:
        return_annotation = inspect.signature(property_.fget).return_annotation
        if return_annotation != inspect.Parameter.empty:
            return_type = inspect.formatannotation(return_annotation)
            description += f': {return_type}'
    if property_.fset:
        description += ' (settable)'
    if property_.fdel:
        description += ' (deletable)'
    return description


def _generate_method_signature_description(method: Callable) -> str:
    """
    Generate a method signature description for the given method.

    This function takes a method as input and generates a string representation of its signature.
    The signature includes the method's parameters, their types, default values (if any), and the return type.

    Parameters:
        method (Callable): The method for which to generate the signature description.

    Returns:
        str: The generated method signature description.

    Example:
        >>> def add_numbers(a: int, b: int = 0) -> int:
        ...     return a + b
        ...
        >>> _generate_method_signature_description(add_numbers)
        '(a: int, b: int = 0) -> int'
    """
    param_strings = []
    for param in inspect.signature(method).parameters.values():
        param_string = param.name
        if param_string == 'self':
            continue
        if param.annotation != inspect.Parameter.empty:
            param_type = inspect.formatannotation(param.annotation)
            param_string += f''': {param_type.strip("'")}'''
        if param.default != inspect.Parameter.empty:
            param_string += ' = [...]' if callable(param.default) else f' = {repr(param.default)}'
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            param_string = f'*{param_string}'
        param_strings.append(param_string)
    method_signature = ', '.join(param_strings)
    description = f'({method_signature})'
    return_annotation = inspect.signature(method).return_annotation
    if return_annotation != inspect.Parameter.empty:
        return_type = inspect.formatannotation(return_annotation)
        description += f''' -> {return_type.strip("'").replace("typing_extensions.", "").replace("typing.", "")}'''
    return description


def _render_docstring(doc: str, with_params: bool = True) -> ui.html:
    """
    Renders the given docstring as HTML.

    Args:
        doc (str): The docstring to render.
        with_params (bool, optional): Whether to include parameter details in the rendered HTML. 
            Defaults to True.

    Returns:
        ui.html: The rendered HTML as a `ui.html` object.

    Notes:
        This function removes indentation from the docstring, replaces 'param ' with an empty string,
        and uses `docutils` to convert the docstring to HTML. If `with_params` is False, it removes
        the parameter details from the rendered HTML.

    Example:
        >>> docstring = '''
        ...     This is a sample docstring.
        ...
        ...     Parameters:
        ...         param1 (int): The first parameter.
        ...         param2 (str): The second parameter.
        ...     '''
        >>> _render_docstring(docstring)
        <ui.html object>

    """
    doc = _remove_indentation_from_docstring(doc)
    doc = doc.replace('param ', '')
    html = docutils.core.publish_parts(doc, writer_name='html5_polyglot')['html_body']
    if not with_params:
        html = re.sub(r'<dl class=".* simple">.*?</dl>', '', html, flags=re.DOTALL)
    return ui.html(html).classes('bold-links arrow-links nicegui-markdown')


def _remove_indentation_from_docstring(text: str) -> str:
    """
    Removes the common indentation from a multi-line docstring.

    This function takes a multi-line docstring as input and removes the common indentation
    from all lines except the first line. The common indentation is determined by finding
    the minimum indentation of all non-blank lines after the first line.

    Parameters:
        text (str): The multi-line docstring to remove indentation from.

    Returns:
        str: The docstring with common indentation removed.

    Example:
        >>> docstring = '''
        ...     This is a multi-line docstring.
        ...     It has some common indentation that needs to be removed.
        ...     '''
        >>> _remove_indentation_from_docstring(docstring)
        'This is a multi-line docstring.\nIt has some common indentation that needs to be removed.'
    """
    lines = text.splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    indentation = min(len(line) - len(line.lstrip()) for line in lines[1:] if line.strip())
    return lines[0] + '\n' + '\n'.join(line[indentation:] for line in lines[1:])
