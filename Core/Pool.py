class Pool:
    def __init__(self, create_instance):
        self._create_instance = create_instance
        self._pool = []

    def acquire(self):
        if len(self._pool) > 0:
            return self._pool.pop()
        else:
            return self._create_instance()

    def release(self, instance):
        self._pool.append(instance)
