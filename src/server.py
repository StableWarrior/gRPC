from . import kvstore_pb2
from .kvstore_pb2_grpc import KeyValueStoreServicer


class KeyValueStoreService(KeyValueStoreServicer):
    def Put(self, request, context):
        return kvstore_pb2.PutResponse()
