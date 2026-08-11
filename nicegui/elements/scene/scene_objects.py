"""Deprecated alias module — import scene objects from ``nicegui.elements.scene.objects`` instead."""
# DEPRECATED: remove this module in NiceGUI 4.0
from ...helpers import warn_once
from .objects.axes_helper import AxesHelper
from .objects.box import Box
from .objects.curve import Curve
from .objects.cylinder import Cylinder
from .objects.extrusion import Extrusion
from .objects.gltf import Gltf
from .objects.group import Group
from .objects.line import Line
from .objects.point_cloud import PointCloud
from .objects.quadratic_bezier_tube import QuadraticBezierTube
from .objects.ring import Ring
from .objects.sphere import Sphere
from .objects.spot_light import SpotLight
from .objects.stl import Stl
from .objects.text import Text
from .objects.text3d import Text3d
from .objects.texture import Texture
from .scene_object3d import Object3D

__all__ = [
    'AxesHelper',
    'Box',
    'Curve',
    'Cylinder',
    'Extrusion',
    'Gltf',
    'Group',
    'Line',
    'Object3D',
    'PointCloud',
    'QuadraticBezierTube',
    'Ring',
    'Sphere',
    'SpotLight',
    'Stl',
    'Text',
    'Text3d',
    'Texture',
]

warn_once('The module `nicegui.elements.scene.scene_objects` is deprecated and will be removed in NiceGUI 4.0. '
          'Import scene objects from `nicegui.elements.scene.objects` instead.')
