import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest
import unittest


class TestPyStdLibIncludeOrNot(unittest.TestCase):
    cj = """<template><div>yo</div></template>"""
    cp = """<template><div>yo</div></template><script>class Component: pass</script>"""

    def setUp(self):
        self.default = vbuild.fullPyComp

    def tearDown(self):
        vbuild.fullPyComp = self.default  # reset to default

    def isPythonComp(self, r):
        return "_pyfunc_op_instantiate(" in r.script

    def nbPythonLibIncluded(self, r):
        return r.script.count("var _pyfunc_op_instantiate")

    def test_base(self):
        r = vbuild.VBuild("c.vue", self.cj)
        self.assertFalse(self.isPythonComp(r))  # comp is js

        r = vbuild.VBuild("c.vue", self.cp)
        self.assertTrue(self.isPythonComp(r))  # comp is py

    def test_fullPyComp_Default(self):
        r = vbuild.VBuild("c.vue", self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r), 0)  # no py no lib
        r += vbuild.VBuild("c1.vue", self.cp)
        r += vbuild.VBuild("c2.vue", self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(
            self.nbPythonLibIncluded(r), 2
        )  # each comp got its own std methods

    def test_fullPyComp_False(self):
        vbuild.fullPyComp = False
        r = vbuild.VBuild("c.vue", self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r), 0)  # no py no lib
        r += vbuild.VBuild("c1.vue", self.cp)
        r += vbuild.VBuild("c2.vue", self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(self.nbPythonLibIncluded(r), 1)  # the full std lib is included

    def test_fullPyComp_True(self):
        vbuild.fullPyComp = True
        r = vbuild.VBuild("c.vue", self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r), 0)  # no py no lib
        r += vbuild.VBuild("c1.vue", self.cp)
        r += vbuild.VBuild("c2.vue", self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(
            self.nbPythonLibIncluded(r), 2
        )  # each comp got its own std methods

    def test_fullPyComp_None(self):
        vbuild.fullPyComp = None
        r = vbuild.VBuild("c.vue", self.cj)
        self.assertEqual(self.nbPythonLibIncluded(r), 0)  # no py no lib
        r += vbuild.VBuild("c1.vue", self.cp)
        r += vbuild.VBuild("c2.vue", self.cp)
        self.assertTrue(self.isPythonComp(r))
        self.assertEqual(
            self.nbPythonLibIncluded(r), 0
        )  # nothing is included, it's up to you
