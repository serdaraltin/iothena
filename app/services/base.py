

class BaseService:
    def __init__(self):
        self.cls_name = self.__class__.__name__

    def __repr__(self):
        return repr(self.__dict__)