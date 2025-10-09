**0.8.2: 2023/08/03**
- FIX #10 with [PR](https://github.com/manatlan/vbuild/pull/9)

**0.8.1: 2019/08/24**
- EVOL: unique identifier, replace "." -> "_" to
- EVOL: module pscript is only needed for pyComponents now !

**0.8.0: 2019/02/24**
- EVOL: new build chain : poetry/pytest/tox & black

**0.7.4: 2018/10/24**
- EVOL: vbuild generate es5 compliant code structure
- EVOL: pycomponents manage more lifecycle events (+ "UPDATED","BEFOREUPDATE","BEFOREDESTROY","DESTROYED")

**0.7.3: 2018/10/22**
- EVOL: styles can contains mediaquery now
- EVOL: repr(vbuild) return only needed tags
- don't remove ":scope" when styles are non scoped
- EVOL: better handle filename -> component name
- one month anniversary ;-)

**0.7.2: 2018/10/19**
- EVOL: PyComp generate JS Closure(online)'s compliant (avoid "This code cannot be converted from ES6.")
- more unit tests

**0.7.1: 2018/10/17**
- FIX: sass/less nested rules works now !

**0.7.0: 2018/10/17**
- EVOL: pre-process css & trans[Script|Html|Style] is done at rendering time
    (not during vbuild instanciation)
- FIX: understand void elements, to avoid closing tags troubles
- more unit tests

**0.6.2: Oct 8, 2018**
- ...

**0.6.1: Oct 7, 2018**
- ...

**0.6.0: Oct 4, 2018**
- Ability to use [python components](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md)

**0.5.0: Oct 1, 2018**
- ...

**0.4.5: Sep 29, 2018**
- ...

**0.4.4: Sep 29, 2018**
- ...

**0.4.3: Sep 25, 2018**
- ...

**0.3.0: Sep 22, 2018**
- First public release available on pypi
