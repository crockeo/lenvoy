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
    def __init__(self, stub=None):
        if stub is None:
            self._channel = grpc.insecure_channel(HOST)
            self._stub = kv_pb2_grpc.KeyValueStoreStub(self._channel)
            self._owns = True
        else:
            self._stub = stub
            self._owns = False

    def __enter__(self):
        if self._owns:
            self._channel.__enter__()
        return self

    def __exit__(self, type, value, tb):
        if self._owns:
            self._channel.__exit__(type, value, tb)

    def get(self, key):
        req = kv_pb2.GetRequest(key=key)
        return self._stub.get(req)

    def set(self, key, value):
        req = kv_pb2.SetRequest(key=key, value=value)
        return self._stub.set(req)

    def has(self, key):
        req = kv_pb2.HasRequest(key=key)
        return self._stub.has(req)

    def clear(self, key):
        req = kv_pb2.ClearRequest(key=key)
        return self._stub.clear(req)

@app.route("/clear/<key>", methods=["POST"])
def clear(key):
    with KeyValueClient() as client:
        res = client.clear(key)
    return flask.jsonify({ "success": res.success })

@app.route("/has/<key>", methods=["GET"])
def has(key):
    with KeyValueClient() as client:
        res = client.has(key)
    return flask.jsonify({ "has": res.has })

@app.route("/")
def root():
    with KeyValueClient() as client:
        value_raw = client.get("count")
        if value_raw.success:
            value = int(value_raw.value)
        else:
            value = 0

        client.set("count", str(value + 1))

    return "Hello world, {} times!".format(value)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
