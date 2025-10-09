import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest
import sys


@pytest.mark.skipif(not vbuild.hasSass, reason="requires pyScss")
def test_sass():
    h = """<template><div>XXX</div></template>
    <Style scoped lang="sass">
    body {
        font: 2px *3;
        color: red + green;
    }
    </style>"""
    r = vbuild.VBuild("comp.vue", h)
    assert "6px" in r.style
    assert "#ff8000" in r.style

    h = """<template><div>XXX</div></template>
    <Style scoped lang="sass">
    body {
        font: $unknown;
    }
    </style>"""
    r = vbuild.VBuild("comp.vue", h)
    with pytest.raises(
        vbuild.VBuildException
    ):  # vbuild.VBuildException: Component 'comp.vue' got a CSS-PreProcessor trouble : Error evaluating expression:
        r.style

    # ensure inline def class are OK
    h = """<template><div>XXX</div></template>
    <Style scoped lang="sass">
    :scope {
        color:blue;

        div {color:red}
    }
    </style>"""
    r = vbuild.VBuild("comp.vue", h)
    assert (
        r.style == """*[data-comp] {color: blue; }\n*[data-comp] div {color: red; }"""
    )
