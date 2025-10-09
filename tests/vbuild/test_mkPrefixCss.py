import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vbuild_package")); import vbuild
import sys; sys.path.insert(0, "../.."); import nicegui.vbuild as vbuild
import pytest


def test_css1():
    assert vbuild.mkPrefixCss("", "XXX") == ""


def test_css2():
    assert vbuild.mkPrefixCss("   a    {color}  ") == "a {color}"
    assert vbuild.mkPrefixCss("   a    {color}  ", "XXX") == "XXX a {color}"


def test_cssTop():
    t = """
:scope
{padding:4px;background: yellow}

  button[ name  ] {\t\tbackground:red /*que neni*/
}
hr *,        body:hover {
color:red;}

p > a, p>i { /*nib*/ }

"""
    ok = """
XXX {padding:4px;background: yellow}
XXX button[ name ] {background:red }
XXX hr *, XXX body:hover {color:red;}
XXX p > a, XXX p>i {}
"""
    tt = vbuild.mkPrefixCss(t, "XXX")
    assert tt == ok.strip()


def test_mediaquery_noprefix():
    t = """
    :scope {color:green}
    @media (max-width: 700px) {
        button {color:red}
        body {color:green}
    }
    button2 {color:yellow}
    """
    r = """:scope {color:green}
button2 {color:yellow}
@media (max-width: 700px) {button {color:red}
body {color:green}}"""
    x = vbuild.mkPrefixCss(t)
    assert x == r


def test_mediaquery_prefix():
    t = """
    :scope {color:green}
    @media (max-width: 700px) {
        button {color:red}
        body {color:green}
    }
    button2 {color:yellow}
    """
    r = """XXX {color:green}
XXX button2 {color:yellow}
@media (max-width: 700px) {XXX button {color:red}\nXXX body {color:green}}"""
    x = vbuild.mkPrefixCss(t, "XXX")
    assert x == r
