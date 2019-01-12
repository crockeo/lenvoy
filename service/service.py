import flask
import grpc
import kv_pb2
import kv_pb2_grpc
import requests
import struct

app = flask.Flask(__name__)

# Configuration information for the gRPC client.
HOST = "grpc_service:80"

class KeyValueClient():
    def __init__(self, stub):
        self._stub = stub

    def get(self, key):
        req = kv_pb2.GetRequest(key=key)
        return self._stub.get(req)

    def set(self, key, value):
        req = kv_pb2.SetRequest(key=key, value=value)
        return self._stub.set(req)

@app.route("/")
def root():
    with grpc.insecure_channel(HOST) as channel:
        stub = kv_pb2_grpc.KeyValueStoreStub(channel)
        client = KeyValueClient(stub)

        value_raw = client.get("count")
        if value_raw.success:
            value = int(value_raw.value)
        else:
            value = 0

        client.set("count", str(value + 1))

    return "Hello world, {} times!".format(value)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
