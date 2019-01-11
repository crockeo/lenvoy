import concurrent.futures
import grpc
import time
import threading

import kv_pb2
import kv_pb2_grpc

class KeyValueStore(kv_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self._lock = threading.Lock()
        self._store = {}

    def get(self, request, context):
        with self._lock:
            if request.key in self._store:
                return kv_pb2.GetResponse(True, self._store[request.key])
            else:
                return kv_pb2.GetResponse(False, "");

    def set(self, request, context):
        with self._lock:
            self._store[request.key] = request.value
            return kv_pb2.SetResponse(True)

if __name__ == "__main__":
    port = 8080

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    kv_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(),
        server
    )
    server.add_insecure_port("0.0.0.0:{}".format(port))
    server.start()

    print "gRPC listening on 0.0.0.0:{}".format(port)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.exit(0)
