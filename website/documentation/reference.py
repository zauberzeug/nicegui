import inspect
from dataclasses import dataclass
from typing import Callable, Optional

from nicegui import binding, ui
from nicegui.dataclasses import KWONLY_SLOTS
from nicegui.elements.markdown import remove_indentation

from ..style import create_anchor_name, subheading
from .custom_restructured_text import CustomRestructuredText as custom_restructured_text


@dataclass(**KWONLY_SLOTS)
class Attribute:
    name: str
    obj: Optional[object]
    base: type


def generate_class_doc(class_obj: type, part_title: str) -> None:
    """Generate documentation for a class including all its methods and properties."""
    doc = class_obj.__doc__ or class_obj.__init__.__doc__
    if doc and ':param' in doc:
        subheading('Initializer', anchor_name=create_anchor_name(part_title.replace('Reference', 'Initializer')))
        description = remove_indentation(doc.split('\n', 1)[-1])
        lines = [line.replace(':param ', ':') for line in description.splitlines() if ':param' in line]
        custom_restructured_text('\n'.join(lines)).classes('bold-links arrow-links rst-param-tables')

    mro = [base for base in class_obj.__mro__ if base.__module__.startswith('nicegui.')]
    ancestors = mro[1:]
    attributes = sorted([
        Attribute(name=name, obj=getattr(base, name, None), base=base)
        for base in reversed(mro)
        for name in dir(base)
        if not name.startswith('_') and _is_method_or_property(base, name)
    ], key=lambda x: x.name)
    properties = [attribute for attribute in attributes if not callable(attribute.obj)]
    methods = [attribute for attribute in attributes if callable(attribute.obj)]

    if properties:
        subheading('Properties', anchor_name=create_anchor_name(part_title.replace('Reference', 'Properties')))
        _render_section(class_obj, properties, method_section=False)

    if methods:
        subheading('Methods', anchor_name=create_anchor_name(part_title.replace('Reference', 'Methods')))
        _render_section(class_obj, methods, method_section=True)

    if ancestors:
        subheading('Inheritance', anchor_name=create_anchor_name(part_title.replace('Reference', 'Inheritance')))
        ui.markdown('\n'.join(f'- `{ancestor.__name__}`' for ancestor in ancestors))


def _render_section(class_obj: type, attributes: list[Attribute], *, method_section: bool) -> None:
    native_attributes = [attribute for attribute in attributes if attribute.base is class_obj]
    if native_attributes:
        with ui.column().classes('gap-2 w-full overflow-x-auto'):
            for native_attribute in native_attributes:
                _render_attribute(native_attribute, method_section=method_section)

    inherited_attributes = [attribute for attribute in attributes if attribute.base is not class_obj]
    if inherited_attributes:
        with ui.expansion(f'Inherited {"methods" if method_section else "properties"}', icon='account_tree', value=True) \
                .classes('w-full border border-gray-200 dark:border-gray-800 rounded-md'):
            for attribute in inherited_attributes:
                _render_attribute(attribute, method_section=method_section)


def _render_attribute(item: Attribute, *, method_section: bool) -> None:
    if method_section:
        decorator = ''
        owner_attr = item.base.__dict__.get(item.name)
        if isinstance(owner_attr, staticmethod):
            decorator += '`@staticmethod`<br />'
        if isinstance(owner_attr, classmethod):
            decorator += '`@classmethod`<br />'
        ui.markdown(f'{decorator}**`{item.name}`**`{_generate_method_signature_description(item.obj)}`') \
            .classes('w-full overflow-x-auto')
    else:
        ui.markdown(f'**`{item.name}`**`{_generate_property_signature_description(item.obj)}`')
    docstring = getattr(item.obj, '__doc__', None)
    if item.obj is not None and docstring:
        _render_docstring(docstring).classes('ml-8')


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


def _render_docstring(doc: str) -> custom_restructured_text:
    doc = _remove_indentation_from_docstring(doc)
    return custom_restructured_text(doc).classes('bold-links arrow-links rst-param-tables')


def _remove_indentation_from_docstring(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    indentation = min(len(line) - len(line.lstrip()) for line in lines[1:] if line.strip())
    return lines[0] + '\n' + '\n'.join(line[indentation:] for line in lines[1:])
