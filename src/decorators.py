from .type_checker import TypeChecker


def typing_policy(policy):
    def typing_policy_decorator(function):
        typeChecker = TypeChecker(function, policy)

        def typing_policy_decorated(*args, **kwargs):
            args = list(args)
            typeChecker.process_arguments(args, kwargs)
            result = typeChecker.process_result(function(*args, **kwargs))

            return result

        return typing_policy_decorated

    return typing_policy_decorator
