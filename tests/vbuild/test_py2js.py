import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest


def test_1():
    c = "class Component: pass"
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component('toto',{" in js
    assert 'name: "toto",' in js
    assert "template: '<div></div>'," in js


def test_MOUNTED():
    c = """class Component:
    def MOUNTED(self):
        pass"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert "mounted: C.prototype.MOUNTED," in js


def test_CREATED():
    c = """class Component:
    def CREATED(self):
        pass"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert "created: C.prototype.CREATED," in js


def test_COMPUTED():
    c = """class Component:
    def COMPUTED_var(self):
        pass"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert "var: C.prototype.COMPUTED_var," in js


def test_WATCH():
    c = """class Component:
    def WATCH_var(self,oldVal,newVal,name="$store.state.yo"):
        pass"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert '"$store.state.yo": C.prototype.WATCH_var,' in js


def test_WATCH_ko():
    c = """class Component:
    def WATCH_var(self):
        pass"""
    with pytest.raises(
        vbuild.VBuildException
    ):  # vbuild.VBuildException: name='var_to_watch' is not specified in WATCH_var
        vbuild.mkPythonVueComponent("toto", "<div></div>", c)

    c = """class Component:
    def WATCH_var(self,oldVal,newVal,name):
        pass"""
    with pytest.raises(
        vbuild.VBuildException
    ):  # vbuild.VBuildException: name='var_to_watch' is not specified in WATCH_var
        vbuild.mkPythonVueComponent("toto", "<div></div>", c)


def test_INIT_PROPS():
    c = """class Component:
    def __init__(self,prop1="?",prop2="?"):
        self.val1=42
        self.val2=True
        self.val3="hello"
"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert "props: ['prop1', 'prop2']," in js
    assert "for(var i in ll) props.push( this.$props" in js
    jsinit = """C.prototype.__init__ = function (prop1, prop2) {
    prop1 = (prop1 === undefined) ? "?": prop1;
    prop2 = (prop2 === undefined) ? "?": prop2;
    this.val1 = 42;
    this.val2 = true;
    this.val3 = "hello";
    return null;
};"""
    assert jsinit in js


def test_METHODS():
    c = """class Component:
    def method1(self,nb):
        self["$parent"].nb=nb;
"""
    js = vbuild.mkPythonVueComponent("toto", "<div></div>", c)
    assert "_pyfunc_op_instantiate" in js
    assert "Vue.component(" in js
    assert "method1: C.prototype.method1," in js
    assert 'this["$parent"].nb = nb;' in js
