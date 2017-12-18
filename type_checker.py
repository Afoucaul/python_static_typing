"""type_checker.py

Enforce a typing policy that relies on function annotations.
This module provides a `typing_policy` decorator, to use along with the Policy
class members.
"""
import itertools


class Policy:
    strictArg       = "POLICY_STRICT_ARG"
    castArg         = "POLICY_CAST_ARG"
    strictReturn    = "POLICY_STRICT_RETURN"
    castReturn      = "POLICY_CAST_RETURN"

    class _PolicyObject:
        def __init__(self, *policies):
            self._policies = policies

        def _is_set(self, flag):
            return flag in self._policies


def typing_policy(*policies):
    """Declare policies to apply to a function.

    This decorator modifies the given function, so as to have it apply the
    specified policies.
    """
    policy = Policy._PolicyObject(*policies)

    def typing_policy_decorator(function):
        def typing_policy_decorated(*args, **kwargs):
            args = list(args)
            for index, arg in itertools.chain(enumerate(args), kwargs.items()):
                varname = function.__code__.co_varnames[index]
                if varname in function.__annotations__:
                    expectedType = function.__annotations__[varname]
                    if not isinstance(arg, expectedType):
                        if policy._is_set(Policy.strictArg):
                            raise TypeError(
                                "Type of '{}' is expected to be {} but a {} "
                                "instance was passed".format(
                                    varname,
                                    expectedType,
                                    type(arg)))
                        elif policy._is_set(Policy.castArg):
                            try:
                                if isinstance(index, int) and index < len(args):
                                    args[index] = expectedType(arg)
                                else:
                                    kwargs[index] = expectedType(arg)
                            except BaseException:
                                raise TypeError(
                                    "Could not convert {} instance '{}' "
                                    "into {}".format(
                                        type(arg),
                                        varname,
                                        expectedType))

            result = function(*args, **kwargs)

            if 'return' in function.__annotations__:
                expectedType = function.__annotations__['return']
                if not isinstance(result, expectedType):
                    if policy._is_set(Policy.strictReturn):
                        raise TypeError(
                            "Return type should be {} but a {} instance was "
                            "returned".format(
                                expectedType,
                                type(result)))
                    elif policy._is_set(Policy.castReturn):
                        try:
                            result = expectedType(result)
                        except BaseException:
                            raise TypeError(
                                "Could not convert {} return value"
                                " into {}".format(
                                    type(result),
                                    expectedType))

            return result

        typing_policy_decorated.__name__ = "typed_" + function.__name__

        return typing_policy_decorated

    return typing_policy_decorator
