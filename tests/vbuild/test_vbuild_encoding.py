import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest
import sys

tu = u"""<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""

ts = """<template><div>français
    <a title='España'><span class="flags es"></span></a>
    <a title='中国'><span class="flags cn"></span></a>
</div></template>"""

""" ENSURE : output type is the same as the input type
    (mainly for py2, no trouble with py3)
"""


def test_unicode():
    r = vbuild.VBuild("x.vue", tu)
    assert type(tu) == type(r.html)

    r = vbuild.VBuild(u"x.vue", tu)
    assert type(tu) == type(r.html)


@pytest.mark.skipif(sys.version_info < (3, 0), reason="sass is bugged on py27")
def test_str():
    r = vbuild.VBuild("x.vue", ts)
    assert type(ts) == type(r.html)

    r = vbuild.VBuild(u"x.vue", ts)
    assert type(ts) == type(r.html)


def test_unicode2():
    r = vbuild.VBuild("xé.vue", tu)
    assert type(tu) == type(r.html)

    r = vbuild.VBuild(u"xé.vue", tu)
    assert type(tu) == type(r.html)


def test_str2():
    r = vbuild.VBuild("xé.vue", ts)
    assert type(ts) == type(r.html)

    r = vbuild.VBuild(u"xé.vue", ts)
    assert type(ts) == type(r.html)


# ~ test_str()
