"""typed_function.py

Provides the TypedFunction class, that wraps around a function to enforce
a typing policy.
"""


class TypedFunction:
    """Wrap a typing policy around a function"""

    def __init__(self, function, policy):
        """Initialisation method

        The type masks will be pre-processed at init time.
        """

        self.function = function
        self.policy = policy

        self.args_t, self.kwargs_t = self.make_type_masks(self.function)
        self.result_t = object

        if 'return' in self.function.__annotations__:
            self.result_t = self.function.__annotations__['return']

    def __call__(self, *args, **kwargs):
        """Call wrapper

        Triggers a type check on the arguments and the return value.
        """

        args = list(args)
        self.process_arguments(args, kwargs)
        result = self.process_result(self.function(*args, **kwargs))

        return result

    def __repr__(self):
        return "TypedFunction({})".format(self.function.__name__)

    def process_arguments(self, args, kwargs):
        """Check the types of the arguments"""

        self.policy.process_args(args, self.args_t)
        self.policy.process_kwargs(kwargs, self.kwargs_t)

    def process_result(self, result):
        """Check the type of the return value"""

        return self.policy.process_result(result, self.result_t)

    @staticmethod
    def make_type_masks(function):
        """Process the type masks"""

        args_t = []
        kwargs_t = {}

        for i in range(function.__code__.co_argcount):
            varname = function.__code__.co_varnames[i]
            if varname in function.__annotations__:
                args_t.append(function.__annotations__[varname])
            else:
                args_t.append(object)

        i += 1
        for j in range(function.__code__.co_kwonlyargcount):
            varname = function.__code__.co_varnames[i+j]
            if varname in function.__annotations__:
                kwargs_t[varname] = function.__annotations__[varname]
            else:
                kwargs_t[varname] = object

        return args_t, kwargs_t
