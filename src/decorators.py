import policy
from typed_function import TypedFunction


def typing_policy(policy):
    def typing_policy_decorator(function):
        return TypedFunction(function, policy)
    return typing_policy_decorator
