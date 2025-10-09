import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest

def test_bad():
    s="""
kk{{_=*jùhgj;://\\}$bc(.[hhh]
"""
    with pytest.raises(vbuild.VBuildException): # vbuild.VBuildException: minimize error: [{'type': 'JSC_PARSE_ERROR', 'file': 'Input_0', 'lineno': 2, 'charno': 10, 'error': 'Parse error. Semi-colon expected', 'line': '        kk{{_=*jùhgj;://\\}$bc(.[hhh]'}]
        vbuild.jsminOnline(s)

def test_min():
    s="""
async function  jo(...a) {
var f=(...a) => {let b=`hello`}
}
"""
    x=vbuild.jsminOnline(s)
    assert "$jscomp" in x


def test_pycomp_onlineClosurable():
    """ Ensure python component produce a JS which is closure's online ready !"""
    cp="""<template><div>yo</div></template><script>class Component: pass</script>"""
    try:
        default=vbuild.fullPyComp
        vbuild.fullPyComp=False
        r=vbuild.VBuild("c.vue",cp)
        x=vbuild.jsminOnline(r.script)
        assert x
    finally:
        vbuild.fullPyComp=default
