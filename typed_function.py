class TypedFunction:
    def __init__(self, function, policy):
        self.function = function
        self.policy = policy

        self.args_t, self.kwargs_t = self._make_type_masks()
        self.result_t = object

        if 'return' in self.function.__annotations__:
            self.result_t = self.function.__annotations__['return']

    def __call__(self, *args, **kwargs):
        args = list(args)
        self.process_arguments(args, kwargs)
        result = self.process_result(self.function(*args, **kwargs))

        return result

    def _make_type_masks(self):
        args_t = []
        kwargs_t = {}

        for i in range(self.function.__code__.co_argcount):
            varname = self.function.__code__.co_varnames[i]
            if varname in self.function.__annotations__:
                args_t.append(self.function.__annotations__[varname])
            else:
                args_t.append(object)

        i += 1
        for j in range(self.function.__code__.co_kwonlyargcount):
            varname = self.function.__code__.co_varnames[i+j]
            if varname in self.function.__annotations__:
                kwargs_t[varname] = self.function.__annotations__[varname]
            else:
                kwargs_t[varname] = object

        return args_t, kwargs_t

    def process_arguments(self, args, kwargs):
        self.policy.process_args(args, self.args_t)
        self.policy.process_kwargs(kwargs, self.kwargs_t)

    def process_result(self, result):
        return self.policy.process_result(result, self.result_t)
