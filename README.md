# prototype
Framework for adding strict typing to python.

A package of utility functions and decorators which allow you to add basic type checking to your python code.

# Why would I want to add type checking to python?

Python's flexable duck typing system is great for allowing people to write generic funcitons which can be re-used 
with various kinds of input functions. However, not all functions are written with this generality in mind. 

By annotating your functions you give a clear signal to callers about what inputs are expected.
Additionally, annotations can help you write functions with fewer type checking conditionals. 
Annotations allow you to find bugs at the top of your functions rather than in the middle of a calculation.

# Examples:

## Consructors

Implicitly passes function arguments to a type constructor. Raises ValueError when invalid inputs are provided.
### Before:
```
def integer_adder(a, b):
  a = int(a)
  b = int(b)
  return a+b
```
### After:
```
@constructors(int, int)
def integer_adder(a, b):
  return a+b
```
