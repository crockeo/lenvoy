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
        print "get {}".format(request.key)
        with self._lock:
            if request.key in self._store:
                return kv_pb2.GetResponse(success=True, value=self._store[request.key])
            else:
                return kv_pb2.GetResponse(success=False, value="")

    def set(self, request, context):
        print "set {} = {}".format(request.key, request.value)
        with self._lock:
            self._store[request.key] = request.value
            return kv_pb2.SetResponse(success=True)

    def has(self, request, context):
        print "has {}".format(request.key)
        with self._lock:
            return kv_pb2.HasResponse(has=request.key in self._store)

    def clear(self, request, context):
        print "clear {}".format(request.key)
        with self._lock:
            if request.key in self._store:
                del self._store[request.key]
                return kv_pb2.ClearResponse(success=True)
            else:
                return kv_pb2.ClearResponse(success=False)

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
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.exit(0)
