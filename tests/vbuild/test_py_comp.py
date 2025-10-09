import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild, os

cc = """
<template>
    <div>
        {{name}} ({{originalName}})
        <button @click="inc(3)">+3</button>
        <button @click="inc()">+1</button>
        {{cpt}} : {{ccpt}} {{wcpt}}
    </div>
</template>
<script>
class Component:

    def __init__(self, name="?"):
        print("DATA INIT",name)
        self.cpt=0
        self.wcpt=""
        self.originalName=name                      # copy the $props.name

    def inc(self,nb=1):                             # with py3, you can make this a async method !
        print("inc(%s)"%nb,self.name)
        self.cpt+=nb

    def CREATED(self):
        print("CREATED",self.name)

    def MOUNTED(self):
        print("mounted",self.name,"in",self["$parent"]["$options"].name)

    def COMPUTED_ccpt(self):
        print("COMPUTE",self.name,self.cpt,"changed")
        return self.cpt*"#"

    def WATCH_1(self,newVal,oldVal,name="cpt"):
        print("WATCH",self.name,name,oldVal,"-->",newVal)
        self.wcpt=self.cpt*"+"
        
    def WATCH_2(self,newVal,oldVal,name="name"):    # watch the prop !
        print("WATCH",name,oldVal,"-->",newVal)

</script>
<style scoped lang="sass">
:scope {background:#FFE;border:1px solid black;margin:$v;padding:$v;}
</style>
"""

cm = """
<template>
    <div>
        {{id}} <button @click="change()"><- change</button>
        <comp :name="id"></comp>
        <comp name="n2"></comp>
        <comp></comp>
    </div>
</template>
<script>
class Component:
    def __init__(self):
        self.id="n"
    def change(self):
        self.id+="x"
</script>
<style scoped lang="sass">
:scope {border:2px solid green;margin:$v;padding:$v;}
</style>

"""
try:
    vbuild.partial = "$v: 12px;"
    # ~ vbuild.fullPyComp=False

    dest = os.path.basename(__file__)[:-3] + ".html"

    with open(dest, "w+") as fid:
        v = vbuild.VBuild("comp.vue", cc) + vbuild.VBuild("mother.vue", cm)
        html = v.html
        style = v.style
        # script=vbuild.jsmin(v.script)
        script = v.script

        fid.write(
            """
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <style>%(style)s</style>
    %(html)s
    <script>%(script)s</script>
    <div id="app">
        <mother/>
    </div>
    <script>new Vue({el:"#app"})</script>    
    """
            % locals()
        )

    print("Generate html --> " + dest)
finally:
    vbuild.partial = ""

