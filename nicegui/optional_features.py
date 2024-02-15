from typing import Literal, Set

_optional_features: Set[str] = set()

FEATURE = Literal[
    'highcharts',
    'matplotlib',
    'pandas',
    'pillow',
    'plotly',
    'pyecharts',
    'webview',
]


def register(feature: FEATURE) -> None:
    """
    Register an optional feature.

    This function adds the specified feature to the set of optional features.

    Parameters:
        feature (FEATURE): The feature to be registered.

    Returns:
        None
    """
    _optional_features.add(feature)


def has(feature: FEATURE) -> bool:
    """
    Check if an optional feature is registered.

    Parameters:
        feature (FEATURE): The feature to check.

    Returns:
        bool: True if the feature is registered, False otherwise.

    """
    return feature in _optional_features
