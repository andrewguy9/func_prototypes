import pytest
from prototypes import *

def test_dictjoin():
  eng = {1:"one", 2:"two"}
  esp = {1:"uno", 2:"dos", 3:"tres"}
  com = {1:("one", "uno"), 2:("two", "dos")}
  assert com == dictjoin(eng, esp)
  with pytest.raises(KeyError):
    dictjoin(esp, eng)

