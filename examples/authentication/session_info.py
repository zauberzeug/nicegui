from collections import UserDict


# in reality we would load/save session info to DB
class SessionInfo(UserDict):

    def __getitem__(self, item):
        if item not in self.data:
            self.data[item] = {}
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)
