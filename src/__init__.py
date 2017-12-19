from importlib import import_module

policy = import_module("{}.policy".format(__name__))
TypeChecker = import_module("{}.type_checker".format(__name__)).TypeChecker
decorators = import_module("{}.decorators".format(__name__))

typing_policy = decorators.typing_policy
