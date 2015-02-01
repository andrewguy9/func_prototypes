# prototype
Framework for adding strict typing to python.

# Why would I want to add type checking to python?

Python's flexable duck typing system is great for allowing people to write generic funcitons which can be re-used 
with various kinds of input. However, not all functions are written with this generality in mind.

By annotating your functions you give a clear signal to callers about what inputs are expected.
Additionally, annotations can help you write functions with fewer type checking conditionals. 
Annotations allow you to find bugs at the top of your functions rather than in the middle of a calculation.

# Implicit Converters:
These decorators implicitly convert arguments are return values to the type you expect. When a value cannot be coerced into the specified type, ValueError is raised.

## Constructors
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
def int_adder(a, b):
  return a+b
```
### Examples:
```
int_adder(3,4) = 7
int_adder(3.9,4.7) = 7
int_adder("3", "4") = 7
int_adder("asdf", "4") Raises ValueError
```

## Returns:
Converts the result of a function to a given type. Raises ValueError on error.
### Before:
```
def int_adder(a, b):
  return int(a+b)
```
### After:
```
@returns(int)
def int_adder(a, b):
  return a+b
```
### Examples:
```
int_adder(3,4) = 7
int_adder(3.9, 4.7) = 8
int_adder("3", "4") Raises ValueError
```

# Type Constrainers:
These decorators raise TypeError when a constraint is violated.

## Typed
Enforces instanceof checks to arguments of a function.
### Before:
```
def int_adder(a, b):
  if not instanceof(a, int):
    raise TypeError("%s is not of type int" % a)
  if not instanceof(b, int):
    raise TypeError("%s is not of type int" % b)
  return a+b
```
### After:
```
@typed(int, int)
def int_adder(a, b):
  return a+b
```
### Examples:
```
int_adder(3,4) = 7
int_adder(3.9,4.7) Raises TypeError
int_adder("3", "4") Raises TypeError
int_adder("asdf", "4") Raises TypeError
```
## Returned 
Enforces the result type of a function.
### Before:
```
def integer_adder(a, b):
  result = a+b
  if not instanceof(result, int):
    raise TypeError("%s is not an int" % result)
  else:
    return result
  ```
### After:
```
@returned(int)
def integer_adder(a, b):
  return a+b
```
### Examples:
```
int_adder(3,4) = 7
int_adder(3.9,4.7) Raises TypeError
int_adder("3", "4") Raises TypeError
int_adder("asdf", "4") Raises TypeError
```

#Limitiations:
@constructors and @typed are unable to deal with other decorators which convert a function from having explit args to \*args, **kwargs (i.e. any decorator). As a result, @constructors and @typed should be the lowest decorator on a function.

## Example:
```
@returned(int)
@typed(int, int)
def int_adder(a, b):
  return a+b
```

