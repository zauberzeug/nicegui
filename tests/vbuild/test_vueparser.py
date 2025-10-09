import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest

tu = u"""<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""

ts = """<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""


def test_unicode():
    r = vbuild.VueParser(tu)
    assert type(tu) == type(r.html.value)


def test_str():
    r = vbuild.VueParser(ts)
    assert type(ts) == type(r.html.value)


def test_1():
    h = """<template><div>XXX</div></template>"""
    r = vbuild.VueParser(h)
    assert isinstance(r.html, vbuild.Content)
    assert repr(r.html) == "<div>XXX</div>"
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []
    assert r.rootTag == "div"

    h = """<template type="xxx"><div>XXX</div></template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"


def test_malformed():
    h = """<template><div><br>XXX</div></template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div><br>XXX</div>"
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []
    assert r.rootTag == "div"


def test_empty():
    h = """<template></template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == ""
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []
    assert r.rootTag is None


def test_more_than_one_template():
    h = """<template><div>jo</div></template><template><div>jo</div></template>"""
    with pytest.raises(vbuild.VBuildException):
        vbuild.VueParser(h)  # Component  contains more than one template


def test_2():
    h = """<template>\n     \n   \t     \n     <div>XXX</div> \t \n    </template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"

    h = """<template type="xxx">\n     \n   \t     \n     <div>XXX</div> \t \n    </template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"

    h = """<template> gsfdsgfd   <div>XXX</div>     gfdsgfd    </template>"""
    r = vbuild.VueParser(h)
    assert (
        repr(r.html) == "gsfdsgfd   <div>XXX</div>     gfdsgfd"
    )  # acceptable, but not good
    assert r.rootTag == "div"  # acceptable, but not good


def test_3():
    h = """<template type="xxx">
        <div>XXX</div></template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"

    h = """<template type="xxx"><div>XXX</div>
    </template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"

    h = """<template type="xxx">
        <div>XXX</div>
    </template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"

    h = """<template type="xxx">\r\n<div>XXX</div>\r\n</template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"
    h = """<template type="xxx">\n<div>XXX</div>\n</template>"""
    r = vbuild.VueParser(h)
    assert repr(r.html) == "<div>XXX</div>"


def test_bad_not_at_root():
    h = """<a><template type="xxx"><div>XXX</div></template></a>"""
    r = vbuild.VueParser(h)
    assert r.html == None
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []


def test_bad_not_openclose():
    h = """<template type="xxx"><div>XXX</div>"""
    r = vbuild.VueParser(h)
    assert r.html == None
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []

    h = """<div>XXX</div></template>"""
    r = vbuild.VueParser(h)
    assert r.html == None
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []


def test_bad_more_than_one_root():
    h = """<template type="xxx"> <div>XXX</div> <div>XXX</div> </template>"""
    with pytest.raises(vbuild.VBuildException):
        vbuild.VueParser(h)  # Component mycomp.vue can have only one top level tag


def test_bad_no_template():
    h = """<templite type="xxx"> <div>XXX</div> <div>XXX</div> </templite>"""
    r = vbuild.VueParser(h)
    assert r.html == None


def test_bad_script_bad():
    h = """<template> <div>XXX</div></template><script> gdsf gfds """
    r = vbuild.VueParser(h)
    assert r.script == None


def test_bad_style_bad():
    h = """<template> <div>XXX</div></template><style> gdsf gfds """
    r = vbuild.VueParser(h)
    assert r.script == None
    assert r.styles == []
    assert r.scopedStyles == []


def test_full():
    h = """<template><div>XXX</div></template><style lang="sass">style</style><script lang="python">script</script>"""
    r = vbuild.VueParser(h)
    assert isinstance(r.html, vbuild.Content)
    assert isinstance(r.script, vbuild.Content)
    assert type(r.styles) == list
    assert isinstance(r.styles[0], vbuild.Content)

    assert repr(r.script) == "script"
    assert repr(r.styles[0]) == "style"
    assert r.script.type == "python"
    assert r.styles[0].type == "sass"

    assert r.html.type == None  # not used for html (now)

    h = """<template><div>XXX</div></template><style scoped>style</style><script>script</script>"""
    r = vbuild.VueParser(h)
    assert repr(r.script) == "script"
    assert repr(r.scopedStyles[0]) == "style"
    assert r.script.type == None
    assert r.scopedStyles[0].type == None
    assert r.html.type == None  # not used for html (now)
