from .typed_function import TypedFunction
from .policy import CAST, STRICT


def typing_policy(policy):
    def typing_policy_decorator(function):
        return TypedFunction(function, policy).__call__
    return typing_policy_decorator


weakly_typed = typing_policy(CAST)
strongly_typed = typing_policy(STRICT)
