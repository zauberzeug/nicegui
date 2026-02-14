import importlib.metadata

try:
    __version__: str = importlib.metadata.version('nicegui')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0'  # NOTE: fallback for Pyodide where package metadata may not be available
