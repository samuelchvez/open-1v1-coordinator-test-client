GLOBAL_TOKEN = None
GLOBAL_USERID = None
GLOBAL_Configurations_CONFIGURED = None


class ConfigurationsManagerSingletonMeta(type):
    """ . """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ . """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigurationsManager(metaclass=ConfigurationsManagerSingletonMeta):
    def __init__(self, initial={}):
        self.configurations = initial

    def sets(self, **kwargs):
        self.configurations = {
            **self.configurations,
            **kwargs
        }

    def set(self, key, value):
        self.configurations[key] = value

    def get(self, key, default=None):
        return self.configurations.get(key, default)
