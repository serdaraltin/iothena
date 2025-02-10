class BaseInfo:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            return cls._instance

    def __repr__(self):
        return repr(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def __contains__(self, item):
        return item in self.__dict__
