

class Event(object):
    def __init__(self):
        self.listeners = set()

    def subscribe(self, callback):
        self.listeners.add(callback)

    def unsubscribe(self, callback):
        self.listeners.discard(callback)

    def fire(self, *args, **kwargs):
        for callback in self.listeners:
            callback(*args, **kwargs)
