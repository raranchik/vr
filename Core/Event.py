class Event:
    def __init__(self):
        self.__subscribers = []

    def subscribe(self, callback):
        self.__subscribers.append(callback)

    def unsubscribe(self, callback):
        self.__subscribers.remove(callback)

    def notify(self, *args, **kwargs):
        for callback in self.__subscribers:
            callback(*args, **kwargs)
