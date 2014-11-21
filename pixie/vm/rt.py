__config__ = None
py_list = list
py_str = str
from rpython.rlib.objectmodel import specialize
from rpython.rtyper.lltypesystem import lltype, rffi
from pixie.vm.effects.effects import ArgList, raise_Ef, Continuation, answer_k, Object
from pixie.vm.effects.environment import Resolve
from pixie.vm.keyword import keyword
from rpython.rlib.rbigint import rbigint

from pixie.vm.effects.effect_transform import cps
from pixie.vm.code import munge
#import pixie.vm.stdlib



def wrap_fn(nm):
    kw_nm = keyword(unicode(nm))
    kw_ns = keyword(unicode("pixie.stdlib"))

    class ResolveResult(Continuation):
        _immutable_ = True
        def __init__(self, w_args):
            self._w_args = w_args

        def step(self, result):
            return result.invoke_Ef(self._w_args)

    def wrapper(*args):
        return raise_Ef(Resolve(kw_ns, kw_nm), ResolveResult(ArgList(py_list(args))))




    return wrapper


_inited_fns = ["first", "count", "list", "next", "-str", "-print"]

for x in _inited_fns:
    globals()[munge(x+"_Ef")] = wrap_fn(x)

_inited_vals = ["load-paths"]


def wrap_val(nm):
    kw_nm = keyword(unicode(nm))
    kw_ns = keyword(unicode("pixie.stdlib"))

    def wrapper():
        return raise_Ef(Resolve(kw_ns, kw_nm), answer_k)

    return wrapper

for x in _inited_vals:
    globals()[munge(x+"_Ef")] = wrap_val(x)
    
    
@specialize.argtype(0)
def wrap(x):
    if isinstance(x, bool):
        from pixie.vm.primitives import true, false
        return true if x else false
    if isinstance(x, int):
        from pixie.vm.numbers import Integer
        return Integer(x)
    if isinstance(x, rbigint):
        import pixie.vm.numbers as numbers
        return numbers.BigInteger(x)
    if isinstance(x, float):
        import pixie.vm.numbers as numbers
        return numbers.Float(x)
    if isinstance(x, unicode):
        from pixie.vm.string import String
        return String(x)
    if isinstance(x, py_str):
        from pixie.vm.string import String
        return String(unicode(x))
    if isinstance(x, Object):
        return x
    if x is None:
        from pixie.vm.primitives import nil
        return nil

    assert False, "Bad Wrap"







