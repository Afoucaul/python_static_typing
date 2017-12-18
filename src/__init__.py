from importlib import import_module

policy = import_module("{}.policy".format(__name__))
TypedFunction = import_module(
                    "{}.typed_function".format(__name__)).TypedFunction
decorators = import_module("{}.decorators".format(__name__))

typing_policy = decorators.typing_policy
