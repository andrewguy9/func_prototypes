from func_prototypes.util import dictjoin
from functools import partial, wraps
try:
    from inspect import getfullargspec as inspector
except ImportError:
    from inspect import getargspec as inspector # Python 2 fallback.


"""
Adapts args, kwargs into **kwargs only with help of function prototype.
Prototype should be a list of arg names.
"""
def to_kwargs(func, args, kwargs):
  fname = func.__name__
  spec = inspector(func)
  # spec 2 is kerwords for getargspec or varkw for getfullargspec
  if spec.varargs is not None or spec[2] is not None:
    raise TypeError( "Cannot convert arguments for function %s because it uses args or kwargs." % fname)
  prototype = spec.args
  out = kwargs.copy()
  if len(prototype) < len(args):
    raise TypeError("%s takes at most %d arguments (%s given)" % (fname, len(prototype), len(args)))
  for name, value in zip(prototype, args):
    if name in out:
      raise TypeError("%s got multiple values for keyword argument '%s'" % (fname, name))
    out[name] = value
  return out

"""Function which adapts arguments for function foo using convert"""
def adapt(foo, convert, context=None):
  @wraps(foo)
  def wrapped(*args, **kwargs):
    kwargs = to_kwargs(foo, args, kwargs)
    new_kwargs = convert(foo.__name__, kwargs, context)
    return foo(**new_kwargs)
  return wrapped

"""Decorator which allows for easy use of adapt"""
def adapter(convert, context=None):
  def wrap(foo):
    adapted = adapt(foo, convert, context)
    return adapted
  return wrap

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
    kwconstructors = to_kwargs(foo, constructors, {})
    foo2 = adapt(foo, map_constructors, kwconstructors)
    return foo2
  return wrap

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
    kwtypes = to_kwargs(foo, types, {})
    foo2 = adapt(foo, check_types, kwtypes)
    return foo2
  return wrap

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

