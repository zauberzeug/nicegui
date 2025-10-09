import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest

""" urgghh ... minimal tests here ;-) """


def test_ok():
    c = """<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):
        self.cpt=0

    def inc(self):
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
    r = vbuild.VBuild("pyc.vue", c)
    assert "_pyfunc_op_instantiate" in r.script
    assert "Vue.component(" in r.script


def test_ko_syntax():
    c = """<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class Component:
    def __init__(self, name):
        self.cpt=0

    def inc(self)           # miss : !!!
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
    with pytest.raises(vbuild.VBuildException):  # Python Component 'pyc.vue' is broken
        vbuild.VBuild("pyc.vue", c)


def test_ko_semantic():
    c = """<template>
    <div>
        {{name}} {{cpt}}
        <button @click="inc()">++</button>
    </div>
</template>
<script lang="python">

class ComponentV0:                  # bad class name
    def __init__(self, name):
        self.cpt=0

    def inc(self):
        self.cpt+=1

</script>
<style scoped>
    :scope {background:#EEE}
</style>"""
    with pytest.raises(
        vbuild.VBuildException
    ):  # Component pyc.vue contains a bad script
        vbuild.VBuild("pyc.vue", c)
