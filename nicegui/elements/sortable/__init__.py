from pathlib import Path

from ...dependencies import register_esm
from .sortable import Sortable

_dist = Path(__file__).parent / 'dist'
_max_time = max((p.stat().st_mtime for p in _dist.glob('*')), default=None)
register_esm('nicegui-sortable', _dist, max_time=_max_time)


__all__ = ['Sortable']
