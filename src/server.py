import grpc

from . import kvstore_pb2
from .kvstore_pb2_grpc import KeyValueStoreServicer
from .store import KVStore


class KeyValueStoreService(KeyValueStoreServicer):
    def __init__(self):
        self.store = KVStore()

    def Put(self, request, context):
        self.store.put(request.key, request.value, request.ttl_seconds)
        return kvstore_pb2.PutResponse()

    def Get(self, request, context):
        value = self.store.get(request.key)

        if value is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "key not found")

        return kvstore_pb2.GetResponse(value=value)

    # def Delete(self, request, context):
    #     self.store.delete(request.key)
    #     return kvstore_pb2.DeleteResponse()

    def List(self, request, context):
        items = self.store.list(request.prefix)

        response_items = [kvstore_pb2.KeyValue(key=k, value=v) for k, v in items]

        return kvstore_pb2.ListResponse(items=response_items)
