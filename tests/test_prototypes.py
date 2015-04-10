import pytest
from func_prototypes import *

def test_to_kwargs():
  def foo(a,b,c):
    return a+b+c
  test_function = partial(to_kwargs, foo)
  expected = {'a':1, 'b':2, 'c':3}
  test_function([1,2,3], {}) == expected
  test_function([1], {'b':2, 'c':3}) == expected
  test_function([], {'a':1, 'b':2, 'c':3}) == expected
  with pytest.raises(TypeError):
    test_function([1], {'a':1, 'b':2, 'c':3})

def test_adapter():
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

def test_constructors_args():
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

def test_constructors_defaults():
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

def test_typed_args():
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

def test_typed_defaults():
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

def test_returns():
  @returns(float)
  def _float_plus(a, b):
    return a+b

  assert isinstance(_float_plus(1, 2), float)
  with pytest.raises(ValueError):
    _float_plus("adsf", "1234")

def test_returned():
  @returned(list)
  def _concat(a, b):
    return a+b

  assert isinstance(_concat([1,2,3], [4,5,6]), list)
  with pytest.raises(TypeError):
    _concat("123", "456")

