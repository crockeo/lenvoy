#!/usr/bin/env bash

set -e

cd $(dirname $0)/..

echo $(pwd)
mkdir gen
python -m grpc.tools.protoc \
        -I./protos \
        --python_out=./gen \
        --grpc_python_out=./gen ./protos/kv.proto
