import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import pytest


def test_names():
    h = """<template><div>XXX</div></template>"""
    assert vbuild.VBuild("mycomp.vue", h).tags[0] == "mycomp"
    assert vbuild.VBuild("jo/mycomp.vue", h).tags[0] == "mycomp"
    assert vbuild.VBuild("jo/mycomp.vuec", h).tags[0] == "mycomp"
    assert vbuild.VBuild("jo/mycomp.vu", h).tags[0] == "mycomp"
    assert vbuild.VBuild("jo/mycomp", h).tags[0] == "mycomp"
    with pytest.raises(vbuild.VBuildException):
        r = vbuild.VBuild("", h)  # Component %s should be named
    with pytest.raises(vbuild.VBuildException):
        r = vbuild.VBuild(None, h)  # Component %s should be named


def test_bad_more_than_one_root():
    h = """<template type="xxx"> <div>XXX</div> <div>XXX</div> </template>"""
    with pytest.raises(vbuild.VBuildException):
        r = vbuild.VBuild(
            "mycomp.vue", h
        )  # Component mycomp.vue can have only one top level tag


def test_bad_no_template():
    h = """<templite type="xxx"> <div>XXX</div> <div>XXX</div> </templite>"""
    with pytest.raises(vbuild.VBuildException):
        r = vbuild.VBuild("comp.vue", h)  # Component comp.vue doesn't have a template


def test_bad_script_bad():
    h = """<template> <div>XXX</div></template><script> gdsf gfds </script>"""
    with pytest.raises(vbuild.VBuildException):
        r = vbuild.VBuild("comp.vue", h)  # Component %s contains a bad script


def test_bad_script_not_closed():
    h = """<template> <div>XXX</div></template><script> gdsf gfds """
    r = vbuild.VBuild("comp.vue", h)  # Component %s contains a bad script
    assert r.script


def test_composant_complet():
    h = """
<template>
  <div>
    {{c}} <button @click="inc">++</button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      c: 0,
    }
  },
  methods: {
    inc() {this.c+=1;}
  }
}
</script>
<style scoped>
:scope {
    padding:4px;
    background: yellow
}
  button {background:red}
</style>
<style>
  button {background:black}
</style>
"""
    r = vbuild.VBuild("name.vue", h)
    assert r.tags == ["name"]
    assert r.style.count("*[data-name]") == 2
    assert r.style.count("background") == 3

    assert ":scope" not in repr(r)
    assert "<div data-name>" in repr(r)
    assert '<script type="text/x-template" id="tpl-name">' in repr(r)
    assert "var name = Vue.component('name', {template:'#tpl-name'," in repr(r)


def test_composant_complet_trans():
    h = """
<template>
  <div>
    {{c}} <button @click="inc">++</button>
  </div>
</template>
<script>
export default {
  data () {
    return {
      c: 0,
    }
  },
  methods: {
    inc() {this.c+=1;}
  }
}
</script>
<style scoped>
:scope {
    padding:4px;
    background: yellow
}
  button {background:red}
</style>
<style>
  button {background:black}
</style>
"""
    oh = vbuild.transHtml
    oj = vbuild.transScript
    oc = vbuild.transStyle
    try:
        vbuild.transHtml = lambda x: "h"
        vbuild.transScript = lambda x: "j"
        vbuild.transStyle = lambda x: "c"
        r = vbuild.VBuild("name.vue", h)
        assert r.html, '<script type="text/x-template" id="tpl-name">h</script>'
        assert r.script, "j"
        assert r.style, "c"
    finally:
        vbuild.transHtml = oh
        vbuild.transScript = oj
        vbuild.transStyle = oc


def test_composant_min():
    h = """
<template>
  <div>Load</div>
</template>
"""
    r = vbuild.VBuild("name.vue", h)
    assert "<div data-name>" in str(r)
    assert '<script type="text/x-template" id="tpl-name">' in str(r)
    assert "var name = Vue.component('name', {template:'#tpl-name'," in str(r)


def test_bad_composant_add():
    c = vbuild.VBuild("c.vue", """<template><div>XXX</div></template>""")
    with pytest.raises(vbuild.VBuildException):
        cc = sum([c, c])  # You can't have multiple set(['c'])


def test_composant_add():
    c = vbuild.VBuild("c.vue", """<template><div>XXX</div></template>""")
    d = vbuild.VBuild("d.vue", """<template><div>XXX</div></template>""")
    cc = sum([c, d])
    assert cc.html.count("<div data-c>XXX</div>") == 1
    assert cc.html.count("<div data-d>XXX</div>") == 1
    assert cc.script.count("var c = Vue.component('c', {template:'#tpl-c',});") == 1
    assert cc.script.count("var d = Vue.component('d', {template:'#tpl-d',});") == 1


def test_pickable():  # so it's GAE memcach'able !
    h = """
<template>
  <div>Load</div>
</template>
"""
    import pickle

    r = vbuild.VBuild("name.vue", h)
    f_string = pickle.dumps(r)
    f_new = pickle.loads(f_string)
    assert str(r) == str(f_new)


def test_script_good():  # so it's GAE memcach'able !
    h = """
<template>
  <div>Load</div>
</template>
<script>
export default {
    mounted() {}
}
</script>
"""
    r = vbuild.VBuild("name.vue", h)
    assert (
        r.script
        == """var name = Vue.component('name', {template:'#tpl-name',\n    mounted() {}\n});"""
    )


def testVoidElements():
    t = """<template>
<div>
    <hr>
    hello {{name}}<br>
    <hr>
</div>
</template>
<style>
h1 {color:blue}
</style>
<script>
export defailt {
    props:["name"],
}
</script>
    """
    rendered = """<style>
h1 {color:blue}
</style>
<script type="text/x-template" id="tpl-jo"><div data-jo>
    <hr>
    hello {{name}}<br>
    <hr>
</div></script>
<script>
var jo = Vue.component('jo', {template:'#tpl-jo',
    props:["name"],
});
</script>
"""
    r = vbuild.VBuild("jo.vue", t)
    assert str(r) == rendered


def testVoidElements_closed():
    t = """<template>
<div>
    <hr/>
    hello {{name}}<br/>
    <hr>
</div>
</template>
<style>
h1 {color:blue}
</style>
<script>
export defailt {
    props:["name"],
}
</script>
    """
    rendered = """<style>
h1 {color:blue}
</style>
<script type="text/x-template" id="tpl-jo"><div data-jo>
    <hr/>
    hello {{name}}<br/>
    <hr>
</div></script>
<script>
var jo = Vue.component('jo', {template:'#tpl-jo',
    props:["name"],
});
</script>
"""
    r = vbuild.VBuild("jo.vue", t)
    assert str(r) == rendered
