class TypedFunction:
    def __init__(self, function):
        self.function = function
        self.args_t, self.kwargs_t = self._make_type_masks()

    def __call__(self, *args, **kwargs):
        args_t, kwargs_t = self.process_arguments(args, kwargs)
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
        pass

    def process_result(self, result):
        pass


if __name__ == '__main__':
    def add(w, x: int, y: int, *, z: str="hello"):
        pass

    typed_add = TypedFunction(add)
