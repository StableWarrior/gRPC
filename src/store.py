import threading
import time
from collections import OrderedDict


class KVStore:
    MAX_ITEMS = 10

    def __init__(self):
        self.data = OrderedDict()
        self.lock = threading.Lock()

    @classmethod
    def expired(cls, expire_at):
        return expire_at is not None and expire_at < time.time()

    def put(self, key, value, ttl):
        with self.lock:
            expire_at = None
            if ttl > 0:
                expire_at = time.time() + ttl

            if key in self.data:
                del self.data[key]

            self.data[key] = (value, expire_at)
            self.data.move_to_end(key)

            if len(self.data) > self.MAX_ITEMS:
                self.data.popitem(last=False)

    def get(self, key):
        with self.lock:
            if key not in self.data:
                return None

            value, expire_at = self.data[key]

            if self.expired(expire_at):
                del self.data[key]
                return None

            self.data.move_to_end(key)

            return value

    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]

    def list(self, prefix):
        result = []

        with self.lock:
            keys = list(self.data.keys())

            for key in keys:
                value, expire_at = self.data[key]

                if self.expired(expire_at):
                    del self.data[key]
                    continue

                if key.startswith(prefix):
                    result.append((key, value))

        return result
