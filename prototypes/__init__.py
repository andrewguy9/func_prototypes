import pytest
from util import dictjoin
from functools import partial, wraps
from inspect import getargspec

"""
Adapts args, kwargs into **kwargs only with help of function prototype.
Prototype should be a list of arg names.
"""
def _to_kwargs(func, args, kwargs):
  fname = func.func_name
  spec = getargspec(func)
  if spec.varargs is not None or spec.keywords is not None:
    raise TypeError( "Cannot convert arguments for function %s because it uses args or kwargs." % fname)
  prototype = spec.args
  out = kwargs.copy()
  if len(prototype) < len(args):
    raise TypeError("%s takes at most %d arguments (%s given)" % (fname, len(prototype), len(args)))
  for name, value in zip(prototype, args):
    if out.has_key(name):
      raise TypeError("%s got multiple values for keyword argument '%s'" % (fname, name))
    out[name] = value
  return out

def _test_to_kwargs():
  def foo(a,b,c):
    return a+b+c
  test_function = partial(_to_kwargs, foo)
  expected = {'a':1, 'b':2, 'c':3}
  test_function([1,2,3], {}) == expected
  test_function([1], {'b':2, 'c':3}) == expected
  test_function([], {'a':1, 'b':2, 'c':3}) == expected
  with pytest.raises(TypeError):
    test_function([1], {'a':1, 'b':2, 'c':3})

"""Function which adapts arguments for function foo using convert"""
def adapt(foo, convert, context=None):
  @wraps(foo)
  def wrapped(*args, **kwargs):
    kwargs = _to_kwargs(foo, args, kwargs)
    new_kwargs = convert(foo.func_name, kwargs, context)
    return foo(**new_kwargs)
  return wrapped

"""Decorator which allows for easy use of adapt"""
def adapter(convert, context=None):
  def wrap(foo):
    adapted = adapt(foo, convert, context)
    return adapted
  return wrap

def _test_adapter():
  def add_n(name, kwargs, n):
    return {k:v+n for k,v in kwargs.items()}
  @adapter(add_n, 2)
  def add(a, b, c):
    return a+b+c
  assert add(1,2,3) == 12
  with pytest.raises(TypeError):
    assert add(1,2,3,4)
  with pytest.raises(TypeError):
    assert add(1,2)
  assert add(1,b=2,c=3) == 12
  with pytest.raises(TypeError):
    assert add(1,b=2,c=3,d=4)
  with pytest.raises(TypeError):
    assert add(a=1,b=2)

"""
Decorator which applies constructors to args before calling the wrapped function with new_args
"""
def constructors(*constructors):
  def map_constructors(func_name, kwargs, kwconstructors):
      try:
        ctor_values = dictjoin(kwargs, kwconstructors).items() # Returns [(name,(arg,constructor)),...]
      except KeyError as e:
        raise TypeError("%s got an unexpected keyword argument '%s'" % (func_name, e.args[0]))
      new_kwargs = {n:c(a) for (n,(a,c)) in ctor_values}
      return new_kwargs
  def wrap(foo):
    kwconstructors = _to_kwargs(foo, constructors, {})
    foo2 = adapt(foo, map_constructors, kwconstructors)
    return foo2
  return wrap

def _test_constructors_args():
  @constructors(int, int)
  def _plus(a, b):
    return a+b

  assert _plus(1,2) == 3
  assert _plus(3.5, 4.7) == 7
  assert _plus("1", "2") == 3
  assert _plus(a=1, b=2) == 3
  assert _plus(b=2, a=1) == 3
  with pytest.raises(ValueError):
    _plus("asdf", 3)
  with pytest.raises(TypeError):
    _plus(a=1, b=2, c=3)
  with pytest.raises(TypeError):
    _plus(a=1)

def _test_constructors_defaults():
  @constructors (str, int)
  def _parse_int(value, base=10):
    return int(value, base)
  with pytest.raises(ValueError):
    _parse_int("deadbeef")
  assert _parse_int("deadbeef", 16) == 3735928559
  assert _parse_int("deadbeef", base=16) == 3735928559
  assert _parse_int(value="deadbeef", base=16) == 3735928559
  assert _parse_int(value="deadbeef", base="16") == 3735928559
  assert _parse_int("deadbeef", "16") == 3735928559
  with pytest.raises(TypeError):
    _parse_int(value="deadbeef", base="16", extra=1)

"""
Decorator which applies type checking to args before calling the wrapped function.
"""
def typed(*types):
  def check_types(func_name, kwargs, kwtypes):
    for name, value in kwargs.items():
      try:
        type_ = kwtypes[name]
      except KeyError as e:
        raise TypeError("%s got an unexpected keyword argument '%s'" % (func_name, e.args[0]))
      if not isinstance(value, type_):
        raise TypeError("Argument %s to %s must be of %s" % (name, func_name, type_))
    return kwargs
  def wrap(foo):
    kwtypes = _to_kwargs(foo, types, {})
    foo2 = adapt(foo, check_types, kwtypes)
    return foo2
  return wrap

def _test_typed_args():
  @typed(int, int)
  def _plus(a, b):
    return a+b

  assert _plus(1,2) == 3
  with pytest.raises(TypeError):
    _plus(3.5, 4.7)
  with pytest.raises(TypeError):
    _plus("1", "2")
  assert _plus(a=1, b=2) == 3
  assert _plus(b=2, a=1) == 3
  with pytest.raises(TypeError):
    _plus("asdf", 3)
  with pytest.raises(TypeError):
    _plus(a=1, b=2, c=3)
  with pytest.raises(TypeError):
    _plus(a=1)

def _test_typed_defaults():
  @typed(str, int)
  def _parse_int(value, base=10):
    return int(value, base)
  with pytest.raises(ValueError):
    _parse_int("deadbeef")
  assert _parse_int("deadbeef", 16) == 3735928559
  assert _parse_int("deadbeef", base=16) == 3735928559
  assert _parse_int(value="deadbeef", base=16) == 3735928559
  with pytest.raises(TypeError):
    _parse_int(value="deadbeef", base="16")
  with pytest.raises(TypeError):
    _parse_int(value="deadbeef", base="16", extra=1)

"""
Decorator which converts the output of the wrapped function to out_type.
"""
def returns(out_type):
  def wrap(foo):
    @wraps(foo)
    def wrapped(*args, **kwargs):
      ret = foo(*args, **kwargs)
      return out_type(ret)
    return wrapped
  return wrap

def _test_returns():
  @returns(float)
  def _float_plus(a, b):
    return a+b

  assert isinstance(_float_plus(1, 2), float)
  with pytest.raises(ValueError):
    _float_plus("adsf", "1234")

"""
Decorator which checks that the retuned value of the wrapped function is an instance of out_type.
"""
def returned(out_type):
  def wrap(foo):
    @wraps(foo)
    def wrapped(*args, **kwargs):
      ret = foo(*args, **kwargs)
      if not isinstance(ret, out_type):
        raise TypeError("Return value to %s must be of %s, not %s" % (foo, out_type, type(ret)))
      else:
        return ret
    return wrapped
  return wrap

def _test_returned():
  @returned(list)
  def _concat(a, b):
    return a+b

  assert isinstance(_concat([1,2,3], [4,5,6]), list)
  with pytest.raises(TypeError):
    _concat("123", "456")

