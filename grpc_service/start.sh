#!/usr/bin/env bash

# -u flag provides unbuffered stdout
python -u /code/service.py &
envoy -c /etc/envoy.yaml --service-cluster grpc_service
