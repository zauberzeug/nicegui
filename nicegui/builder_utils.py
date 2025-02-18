import inspect
from typing import Any, get_origin, get_args

def run_safe(builder, type_check: bool = True, **kwargs) -> Any:
    """Run a builder function but only pass the keyword arguments which are expected by the builder function

    :param builder: The builder function
    :param type_check: Optional flag to enable or disable the type checking of the keyword arguments.
        Default is True.
    :param kwargs: The keyword arguments to pass to the builder function
    """
    sig = inspect.signature(builder)
    args = sig.parameters.keys()
    has_kwargs = any([param.kind == inspect.Parameter.VAR_KEYWORD for param in
                      inspect.signature(builder).parameters.values()])
    if type_check:
        for func_param_name, func_param_info in sig.parameters.items():
            if func_param_name in kwargs:
                if func_param_info.annotation is inspect.Parameter.empty:
                    continue
                expected_type = func_param_info.annotation
                value = kwargs[func_param_name]
                origin_type = get_origin(expected_type)

                if origin_type is not None:
                    # Handle parameterized generics like list[int], dict[str, int], etc.
                    if origin_type == list:
                        if not isinstance(value, list):
                            raise ValueError(f'Invalid type for parameter {func_param_name}, expected a list')
                        element_type = get_args(expected_type)[0]
                        if not all(isinstance(item, element_type) for item in value):
                            raise ValueError(
                                f'Elements of parameter {func_param_name} must be of type {element_type}')
                    elif origin_type == dict:
                        if not isinstance(value, dict):
                            raise ValueError(f'Invalid type for parameter {func_param_name}, expected a dict')
                        key_type, val_type = get_args(expected_type)
                        if not all(isinstance(k, key_type) and isinstance(v, val_type) for k, v in value.items()):
                            raise ValueError(
                                f'Keys and values of parameter {func_param_name} must be of types {key_type} and {val_type}'
                            )
                    else:
                        # Add handling for other generic types if needed
                        raise TypeError(
                            f'Unsupported type annotation {expected_type} for parameter {func_param_name}')
                else:
                    # Non-generic types
                    if not isinstance(value, expected_type):
                        raise ValueError(f'Invalid type for parameter {func_param_name}, expected {expected_type}')
    filtered = {k: v for k, v in kwargs.items() if k in args} if not has_kwargs else kwargs
    return builder(**filtered)
