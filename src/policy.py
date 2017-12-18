def _fail_strict(expected_type, received_value):
    raise TypeError(
        "Expected an instance of {}, received {} instance '{}'".format(
            expected_type, type(received_value), received_value))


def _fail_cast(expected_type, received_value):
    raise TypeError(
        "Could not cast {} instance '{}' into {}".format(
            type(received_value), received_value, expected_type))


class Policy:
    STRICT_ARGS     = ("process_args",   "STRICT_ARGS")
    CAST_ARGS       = ("process_args",   "CAST_ARGS")
    STRICT_KWARGS   = ("process_kwargs", "STRICT_KWARGS")
    CAST_KWARGS     = ("process_kwargs", "CAST_KWARGS")
    STRICT_RESULT   = ("process_return", "STRICT_RESULT")
    CAST_RESULT     = ("process_return", "CAST_RESULT")

    def __init__(self, *policies):
        for policy in policies:
            setattr(self, policy[0], getattr(type(self), "_" + policy[1].lower()))

    def process_args(self, args, args_t):
        pass

    def process_kwargs(self, kwargs, kwargs_t):
        pass

    def process_result(self, result, result_t):
        return result

    @staticmethod
    def _strict_args(args, args_t):
        for i, value in enumerate(args):
            if value is not None and not isinstance(value, args_t[i]):
                _fail_strict(args_t[i], value)

    @staticmethod
    def _cast_args(args, args_t):
        for i, value in enumerate(args):
            if value is not None and not isinstance(value, args_t[i]):
                try:
                    args[i] = args_t[i](args[i])
                except BaseException:
                    _fail_strict(args_t[i], value)

    @staticmethod
    def _strict_kwargs(kwargs, kwargs_t):
        for key, value in kwargs.items():
            if value is not None and not isinstance(value, kwargs_t[key]):
                    _fail_strict(kwargs_t[key], value)

    @staticmethod
    def _cast_kwargs(kwargs, kwargs_t):
        for key, value in kwargs.items():
            if value is not None and not isinstance(value, kwargs_t[key]):
                try:
                    kwargs[key] = kwargs_t[key](value)
                except BaseException:
                    _fail_cast(kwargs_t[key], value)

    @staticmethod
    def _strict_result(result, result_t):
        if result is not None and not isinstance(result, result_t):
            _fail_strict(result_t, result)

    @staticmethod
    def _cast_result(result, result_t):
        if result is not None and not isinstance(result, result_t):
            try:
                return result_t(result)
            except BaseException:
                _fail_cast(result_t, result)


STRICT = Policy(Policy.STRICT_ARGS, Policy.STRICT_KWARGS, Policy.STRICT_RESULT)
CAST = Policy(Policy.CAST_ARGS, Policy.CAST_KWARGS, Policy.CAST_RESULT)
