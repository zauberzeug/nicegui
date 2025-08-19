from typing import Literal

MaskImage = Literal[
    'none',
    'circle',
    'ellipse',
    'radial-closest-corner',
    'radial-closest-side',
    'radial-farthest-corner',
    'radial-farthest-side',
    'radial-at-top-left',
    'radial-at-top',
    'radial-at-top-right',
    'radial-at-left',
    'radial-at-center',
    'radial-at-right',
    'radial-at-bottom-left',
    'radial-at-bottom',
    'radial-at-bottom-right',
]
