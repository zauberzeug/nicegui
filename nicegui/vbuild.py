#!/usr/bin/python2
# -*- coding: utf-8 -*-
# #############################################################################
#    Copyright (C) 2018 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/vbuild
# #############################################################################
__version__ = "0.8.2" # auto-updated

import glob
import itertools
import json
import os
import pkgutil
import re
import subprocess
import traceback

try:
    import urllib as urlparse

    import urllib2 as urlrequest
    from HTMLParser import HTMLParser
except ImportError:
    import urllib.parse as urlparse
    import urllib.request as urlrequest
    from html.parser import HTMLParser

transHtml = lambda x: x  # override them to use your own transformer/minifier
transStyle = lambda x: x
transScript = lambda x: x

partial = ""
fullPyComp = True  # 3 states ;-)
# None  : minimal py comp, it's up to u to include "pscript.get_full_std_lib()"
# False : minimal py comp, vbuild will include the std lib
# True  : each component generate its needs (default)

hasLess = bool(pkgutil.find_loader("lesscpy"))
hasSass = bool(pkgutil.find_loader("scss"))
hasClosure = bool(pkgutil.find_loader("closure"))


class VBuildException(Exception):
    pass


def minimize(code):
    if hasClosure:
        return jsmin(code)
    else:
        return jsminOnline(code)


def jsminOnline(code):
    """ JS-minimize (transpile to ES5 JS compliant) thru a online service
        (https://closure-compiler.appspot.com/compile)
    """
    data = [
        ("js_code", code),
        ("compilation_level", "SIMPLE_OPTIMIZATIONS"),
        ("output_format", "json"),
        ("output_info", "compiled_code"),
        ("output_info", "errors"),
    ]
    try:
        req = urlrequest.Request(
            "https://closure-compiler.appspot.com/compile",
            urlparse.urlencode(data).encode("utf8"),
            {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
        )
        response = urlrequest.urlopen(req)
        r = json.loads(response.read())
        response.close()
        code = r.get("compiledCode", None)
    except Exception as e:
        raise VBuildException("minimize error: %s" % e)
    if code:
        return code
    else:
        raise VBuildException("minimize error: %s" % r.get("errors", None))


def jsmin(code):  # need java & pip/closure
    """ JS-minimize (transpile to ES5 JS compliant) with closure-compiler
        (pip package 'closure', need java !)
    """
    if hasClosure:
        import closure  # py2 or py3
    else:
        raise VBuildException(
            "jsmin error: closure is not installed (sudo pip closure)"
        )
    cmd = ["java", "-jar", closure.get_jar_filename()]
    try:
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as e:
        raise VBuildException("jsmin error: %s" % e)
    out, err = p.communicate(code.encode("utf8"))
    if p.returncode == 0:
        return out.decode("utf8")
    else:
        raise VBuildException("jsmin error:" + err.decode("utf8"))


def preProcessCSS(cnt, partial=""):
    """ Apply css-preprocessing on css rules (according css.type) using a partial or not
        return the css pre-processed
    """
    if cnt.type in ["scss", "sass"]:
        if hasSass:
            from scss.compiler import compile_string  # lang="scss"

            return compile_string(partial + "\n" + cnt.value)
        else:
            print("***WARNING*** : miss 'sass' preprocessor : sudo pip install pyscss")
            return cnt.value
    elif cnt.type in ["less"]:
        if hasLess:
            import lesscpy
            import six

            return lesscpy.compile(
                six.StringIO(partial + "\n" + cnt.value), minify=True
            )
        else:
            print("***WARNING*** : miss 'less' preprocessor : sudo pip install lesscpy")
            return cnt.value
    else:
        return cnt.value


class Content:
    def __init__(self, v, typ=None):
        self.type = typ
        self.value = v.strip("\n\r\t ")

    def __repr__(self):
        return self.value


class VueParser(HTMLParser):
    """ Just a class to extract <template/><script/><style/> from a buffer.
        self.html/script/styles/scopedStyles are Content's object, or list of.
    """

    voidElements = "area base br col command embed hr img input keygen link menuitem meta param source track wbr".split(
        " "
    )

    def __init__(self, buf, name=""):
        """ Extract stuff from the vue/buffer 'buf'
            (name is just useful for naming the component in exceptions)
        """
        HTMLParser.__init__(self)
        self.name = name
        self._p1 = None
        self._level = 0
        self._scriptLang = None
        self._styleLang = None
        self.rootTag = None
        self.html, self.script, self.styles, self.scopedStyles = None, None, [], []
        self.feed(buf.strip("\n\r\t "))

    def handle_starttag(self, tag, attrs):
        self._tag = tag

        # don't manage if it's a void element
        if tag not in self.voidElements:
            self._level += 1

            attributes = dict([(k.lower(), v and v.lower()) for k, v in attrs])
            if tag == "style" and attributes.get("lang", None):
                self._styleLang = attributes["lang"]
            if tag == "script" and attributes.get("lang", None):
                self._scriptLang = attributes["lang"]
            if self._level == 1 and tag == "template":
                if self._p1 is not None:
                    raise VBuildException(
                        "Component %s contains more than one template" % self.name
                    )
                self._p1 = self.getOffset() + len(self.get_starttag_text())
            if self._level == 2 and self._p1:  # test p1, to be sure to be in a template
                if self.rootTag is not None:
                    raise VBuildException(
                        "Component %s can have only one top level tag !" % self.name
                    )
                self.rootTag = tag

    def handle_endtag(self, tag):
        if tag not in self.voidElements:
            if (
                tag == "template" and self._p1
            ):  # don't watch the level (so it can accept mal formed html
                self.html = Content(self.rawdata[self._p1 : self.getOffset()])
            self._level -= 1

    def handle_data(self, data):
        if self._level == 1:
            if self._tag == "script":
                self.script = Content(data, self._scriptLang)
            if self._tag == "style":
                if "scoped" in self.get_starttag_text().lower():
                    self.scopedStyles.append(Content(data, self._styleLang))
                else:
                    self.styles.append(Content(data, self._styleLang))

    def getOffset(self):
        lineno, off = self.getpos()
        rtn = 0
        for _ in range(lineno - 1):
            rtn = self.rawdata.find("\n", rtn) + 1
        return rtn + off


def mkPrefixCss(css, prefix=""):
    """Add the prexix (css selector) to all rules in the 'css'
       (used to scope style in context)
    """
    medias = []
    while "@media" in css:
        p1 = css.find("@media", 0)
        p2 = css.find("{", p1) + 1
        lv = 1
        while lv > 0:
            lv += 1 if css[p2] == "{" else -1 if css[p2] == "}" else 0
            p2 += 1
        block = css[p1:p2]
        mediadef = block[: block.find("{")].strip()
        mediacss = block[block.find("{") + 1 : block.rfind("}")].strip()
        css = css.replace(block, "")
        medias.append((mediadef, mkPrefixCss(mediacss, prefix)))

    lines = []
    css = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", css)
    css = re.sub(re.compile(r"[ \t\n]+", re.DOTALL), " ", css)
    for rule in re.findall(r"[^}]+{[^}]+}", css):
        sels, decs = rule.split("{", 1)
        if prefix:
            l = [
                (prefix + " " + i.replace(":scope", "").strip()).strip()
                for i in sels.split(",")
            ]
        else:
            l = [(i.strip()) for i in sels.split(",")]
        lines.append(", ".join(l) + " {" + decs.strip())
    lines.extend(["%s {%s}" % (d, c) for d, c in medias])
    return "\n".join(lines).strip("\n ")


class VBuild:
    """ the main class, provide an instance :

        .style : contains all the styles (scoped or not)
        .script: contains a (js) Vue.component() statement to initialize the component
        .html  : contains the <script type="text/x-template"/>
        .tags  : list of component's name whose are in the vbuild instance
    """

    def __init__(self, filename, content):
        """ Create a VBuild class, by providing a :
                filename: which will be used to name the component, and create the namespace for the template
                content: the string buffer which contains the sfc/vue component
        """
        if not filename:
            raise VBuildException("Component %s should be named" % filename)

        if type(content) != type(filename):  # only py2, transform
            if type(content) == unicode:  # filename to the same type
                filename = filename.decode("utf8")  # of content to avoid
            else:  # troubles with implicit
                filename = filename.encode("utf8")  # ascii conversions (regex)

        name = os.path.splitext(os.path.basename(filename))[0]

        unique = filename[:-4].replace("/", "-").replace("\\", "-").replace(":", "-").replace(".", "-")
        # unique = name+"-"+''.join(random.choice(string.letters + string.digits) for _ in range(8))
        tplId = "tpl-" + unique
        dataId = "data-" + unique

        vp = VueParser(content, filename)
        if vp.html is None:
            raise VBuildException("Component %s doesn't have a template" % filename)
        else:
            html = re.sub(r"^<([\w-]+)", r"<\1 %s" % dataId, vp.html.value)

            self.tags = [name]
            # self.html="""<script type="text/x-template" id="%s">%s</script>""" % (tplId, transHtml(html) )
            self._html = [(tplId, html)]

            self._styles = []
            for style in vp.styles:
                self._styles.append(("", style, filename))
            for style in vp.scopedStyles:
                self._styles.append(("*[%s]" % dataId, style, filename))

            # and set self._script !
            if vp.script and ("class Component:" in vp.script.value):
                ######################################################### python
                try:
                    self._script = [
                        mkPythonVueComponent(
                            name, "#" + tplId, vp.script.value, fullPyComp
                        )
                    ]
                except Exception as e:
                    raise VBuildException(
                        "Python Component '%s' is broken : %s"
                        % (filename, traceback.format_exc())
                    )
            else:
                ######################################################### js
                try:
                    # self._script = [
                    #     mkClassicVueComponent(
                    #         name, "#" + tplId, vp.script and vp.script.value
                    #     )
                    # ]
                    self._script = [
                        vp.script.value
                    ]
                except Exception as e:
                    raise VBuildException(
                        "JS Component %s contains a bad script" % filename
                    )

    @property
    def html(self):
        """ Return HTML (script tags of embbeded components), after transHtml"""
        l = []
        for tplId, html in self._html:
            l.append(
                """<script type="text/x-template" id="%s">%s</script>"""
                % (tplId, transHtml(html))
            )
        return "\n".join(l)

    @property
    def script(self):
        """ Return JS (js of embbeded components), after transScript"""
        js = "\n".join(self._script)
        isPyComp = "_pyfunc_op_instantiate(" in js  # in fact : contains
        isLibInside = "var _pyfunc_op_instantiate" in js

        if (fullPyComp is False) and isPyComp and not isLibInside:
            import pscript
            return transScript(pscript.get_full_std_lib() + "\n" + js)
        else:
            return transScript(js)

    @property
    def style(self):
        """ Return CSS (styles of embbeded components), after preprocess css & transStyle"""
        style = ""
        try:
            for prefix, s, filename in self._styles:
                style += mkPrefixCss(preProcessCSS(s, partial), prefix) + "\n"
        except Exception as e:
            raise VBuildException(
                "Component '%s' got a CSS-PreProcessor trouble : %s" % (filename, e)
            )
        return transStyle(style).strip()

    def __add__(self, o):
        same = set(self.tags).intersection(set(o.tags))
        if same:
            raise VBuildException("You can't have multiple '%s'" % list(same)[0])
        self._html.extend(o._html)
        self._script.extend(o._script)
        self._styles.extend(o._styles)
        self.tags.extend(o.tags)
        return self

    def __radd__(self, o):
        return self if o == 0 else self.__add__(o)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__ = d

    def __repr__(self):
        """ return an html ready represenation of the component(s) """
        hh = self.html
        jj = self.script
        ss = self.style
        s = ""
        if ss:
            s += "<style>\n%s\n</style>\n" % ss
        if hh:
            s += "%s\n" % hh
        if jj:
            s += "<script>\n%s\n</script>\n" % jj
        return s


def mkClassicVueComponent(name, template, code):
    if code is None:
        js = "{}"
    else:
        p1 = code.find("{")
        p2 = code.rfind("}")
        if 0 <= p1 <= p2:
            js = code[p1 : p2 + 1]
        else:
            raise Exception("Can't find valid content inside '{' and '}'")

    return """var %s = Vue.component('%s', %s);""" % (
        name,
        name,
        js.replace("{", "{template:'%s'," % template, 1),
    )


def mkPythonVueComponent(name, template, code, genStdLibMethods=True):
    """ Transpile the component 'name', which have the template 'template',
        and the code 'code' (which should contains a valid Component class)
        to a valid Vue.component js statement.

        genStdLibMethods : generate own std lib method inline (with the js)
                (if False: use pscript.get_full_std_lib() to get them)
    """
    import pscript
    code = code.replace(
        "class Component:", "class C:"
    )  # minimize class name (todo: use py2js option for that)
    exec(code, globals(), locals())
    klass = locals()["C"]

    computeds = []
    watchs = []
    methods = []
    lifecycles = []
    classname = klass.__name__
    props = []
    for oname, obj in vars(klass).items():
        if callable(obj):
            if not oname.startswith("_"):
                if oname.startswith("COMPUTED_"):
                    computeds.append(
                        "%s: %s.prototype.%s," % (oname[9:], classname, oname)
                    )
                elif oname.startswith("WATCH_"):
                    if obj.__defaults__:
                        varwatch = obj.__defaults__[
                            0
                        ]  # not neat (take the first default as whatch var)
                        watchs.append(
                            '"%s": %s.prototype.%s,' % (varwatch, classname, oname)
                        )
                    else:
                        raise VBuildException(
                            "name='var_to_watch' is not specified in %s" % oname
                        )
                elif oname in [
                    "MOUNTED",
                    "CREATED",
                    "UPDATED",
                    "BEFOREUPDATE",
                    "BEFOREDESTROY",
                    "DESTROYED",
                ]:
                    lifecycles.append(
                        "%s: %s.prototype.%s," % (oname.lower(), classname, oname)
                    )
                else:
                    methods.append("%s: %s.prototype.%s," % (oname, classname, oname))
            elif oname == "__init__":
                props = list(obj.__code__.co_varnames)[1:]

    methods = "\n".join(methods)
    computeds = "\n".join(computeds)
    watchs = "\n".join(watchs)
    lifecycles = "\n".join(lifecycles)

    pyjs = pscript.py2js(
        code, inline_stdlib=genStdLibMethods
    )  # https://pscript.readthedocs.io/en/latest/api.html

    return (
        """
var %(name)s=(function() {

    %(pyjs)s

    function construct(constructor, args) {
        function F() {return constructor.apply(this, args);}
        F.prototype = constructor.prototype;
        return new F();
    }

    return Vue.component('%(name)s',{
        name: "%(name)s",
        props: %(props)s,
        template: '%(template)s',
        data: function() {
            var props=[]
            var ll=%(props)s;
            for(var i in ll) props.push( this.$props[ ll[i] ] )
            var i=construct(%(classname)s,props) // new %(classname)s(...props)
            return JSON.parse(JSON.stringify( i ));
        },
        computed: {
            %(computeds)s
        },
        methods: {
            %(methods)s
        },
        watch: {
            %(watchs)s
        },
        %(lifecycles)s
    })
})();
"""
        % locals()
    )


def render(*filenames):
    """ Helpers to render VBuild's instances by providing filenames or pattern (glob's style)"""
    isPattern = lambda f: ("*" in f) or ("?" in f)

    files = []
    for i in filenames:
        if isinstance(i, list):
            files.extend(i)
        else:
            files.append(i)

    files = [glob.glob(i) if isPattern(i) else [i] for i in files]
    files = list(itertools.chain(*files))

    ll = []
    for f in files:
        try:
            with open(f, "r+") as fid:
                content = fid.read()
        except IOError as e:
            raise VBuildException(str(e))
        ll.append(VBuild(f, content))

    return sum(ll)


if __name__ == "__main__":
    print("Less installed (lesscpy)    :", hasLess)
    print("Sass installed (pyScss)     :", hasSass)
    print("Closure installed (closure) :", hasClosure)
    if os.path.isfile("tests.py"):
        exec(open("tests.py").read())
    # ~ if(os.path.isfile("test_py_comp.py")): exec(open("test_py_comp.py").read())
