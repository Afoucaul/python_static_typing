# python_static_typing

This package provides a way to enforce static typing, by making use of Python's annotation system.

The purpose of this package is to show the feasibility of making Python a statically typed language.
Additionally, this is motivated by an incentive to prove the usefulness of Python's annotations.

# Overview

What you can do with this package:

    >>> @typing_policy(policy.STRICT)
    ... def add(x: int, y: int) -> int:
    ...     return x + y
    ...
    >>> add("Hello ", "World!")
    TypeError: Expected an instance of <class 'int'>, received <class 'str'> instance 'Hello '
        

# How to use this package

This package provides a `typing_policy` decorator, to be used along with instances of the `Policy` class.
A function decorated with the `typing_policy` decorator will check the type of its parameters and return value every time it is called.
The `typing_policy` decorator takes a single parameter, the policy to enforce.
A policy is an instance of the `Policy` class, possibly one of the predefined `policy.STRICT` and `policy.CAST`.

## The `typing_policy` decorator
When decorated with the `typing_decorator`, a function is wrapped into a `TypedFunction` instance.
At initialisation, this instance processes the annotations of the original function, located in the function's `__annotations__` attribute.
When called, the decorated function will confront the type of the passed parameters to its annotations.

## The `Policy` class
The `typing_policy` decorator expects an instance of the `Policy` class as its only parameter.
The latter can be manually instantiated, so as to thoroughly control its behaviour.
However, most use cases should be covered by the pre-defined `STRICT` and `CAST` policies.
The `STRICT` policy will cause the function to fail if any argument has the wrong type.
The `CAST` policy is more lenient, and will try to cast the arguments that have the wrong type.

# Examples

## Basic use of the `typing_policy` decorator

### The `STRICT` policy

We consider an `add` function, that takes two parameters and returns its sum.
A generic implementation would be as follows:

    def add(x, y):
        return x + y

This function would accept any type in input for `x` and `y`, and would attempt to return their sum.
Now, suppose we want to signal that this function should be used with integers.
We can use the annotation system:

    def add(x: int, y: int) -> int:
        return x + y

Now, the user of this function is aware that it should be given integers, and that it is supposed to return an integer.
However, the annotations are no guarantee, and any other types would still be supported.
But if we decorate the `add` function with the `typing_policy` decorator, we can cause it to fail when the input types are not those expected.
Let's try with the `STRICT` policy:

    @typing_policy(policy.STRICT)
    def add(x: int, y: int) -> int:
        return x + y

Now, a call such as `add("Hello, ", "World!")` would fail, although instances of `str` do support the `+` operator.
The function execution would in this case result in a `TypeError`.

### The `CAST` policy

We can make a more lenient version of our `add` function, that attempts to convert the input argument into the expected types.
    
    @typing_policy(policy.CAST)
    def add(x: int, y: int) -> int:
        return x + y

Now, we can call the `add` function with strings, as long as those can be converted into integers.
Behind the scene, `x` will be replaced by `int(x)`, and the same for `y`.
Of course, if one of these conversion fails, the function invokation will fail, and raise a `TypeError`.
