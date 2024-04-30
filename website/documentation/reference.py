import inspect
from typing import Callable, Optional

from nicegui import binding, ui

from ..style import create_anchor_name, subheading


def generate_class_doc(class_obj: type, part_title: str) -> None:
    """Generate documentation for a class including all its methods and properties."""
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
    param_strings = []
    for param in inspect.signature(method).parameters.values():
        param_string = param.name
        if param_string == 'self':
            continue
        if param.annotation != inspect.Parameter.empty:
            param_type = inspect.formatannotation(param.annotation)
            param_string += f''': {param_type.strip("'")}'''
        if param.default != inspect.Parameter.empty:
            param_string += ' = [...]' if callable(param.default) else f' = {param.default!r}'
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


def _render_docstring(doc: str) -> ui.restructured_text:
    doc = _remove_indentation_from_docstring(doc)
    return ui.restructured_text(doc).classes('bold-links arrow-links rst-param-tables')


def _remove_indentation_from_docstring(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    indentation = min(len(line) - len(line.lstrip()) for line in lines[1:] if line.strip())
    return lines[0] + '\n' + '\n'.join(line[indentation:] for line in lines[1:])
