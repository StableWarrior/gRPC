from concurrent import futures

import grpc

from . import kvstore_pb2_grpc
from .server import KeyValueStoreService


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreService(), server)

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Server started on port 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    run()
