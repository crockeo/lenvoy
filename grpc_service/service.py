import asyncio
import concurrent
import grpc
import time

import kv_pb2
import kv_pb2_grpc

class KeyValueStore(kv_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self._lock = asyncio.Lock()
        self._store = {}

    async def get(self, request, context):
        await self._lock.acquire()
        try:
            return kv_pb2.GetResponse(True, self._store[request.key])
        except KeyError:
            return kv_pb2.GetResponse(False, "");
        finally:
            lock.release()

    async def set(self, request, context):
        async with self._lock:
            self._store[request.key] = request.value
            return kv_pb2.SetResponse(True)

if __name__ == "__main__":
    port = 8081

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    kv_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(),
        server
    )
    server.add_insecure_port("0.0.0.0:{}".format(port))
    server.start()

    print("gRPC listening on 0.0.0.0:{}".format(port))

    try:
        while True:
            time.sleep(60 * 60 * 24) # Wait for a day at a time
    except KeyboardInterrupt:
        server.stop(0)
