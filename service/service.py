import flask
import kv_pb2
import requests
import struct

app = flask.Flask(__name__)

# Configuration information for the gRPC client.
HOST = "http://localhost:8000/grpc"
HEADERS = {
    "Content-Type": "application/grpc",
    "Host": "grpc"
}

class KeyValueClient():
    def get(self, key):
        req = kv_pb2.GetRequest(key=key)

        data = req.SerializeToString()
        data = struct.pack("!cI", b"\0", len(data)) + data

        res = requests.post(
            HOST + "/kv.KeyValueStore/get",
            data=data,
            headers=HEADERS
        )

        return kv_pb2.GetResponse().FromString(res.contents[5:])

    def set(self, key, value):
        req = kv_pb2.SetRequest(key=key, value=value)

        data = req.SerializeToString()
        data = struct.pack("!cI", "b\0", len(data)) + data

        res = requests.post(
            HOST + "/kv.KeyValueStore/set",
            data=data,
            headers=HEADERS
        )

        return kv_pb2.SetResponse().FromString(res.contents[5:])

@app.route("/")
def root():
    client = KeyValueClient()

    value_raw = client.get("count")
    if value_raw.success:
        value = int(value_raw.value)
    else:
        value = 0

    client.set("count", str(value + 1))

    return "Hello world, {} times!".format(value)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
