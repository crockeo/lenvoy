#!/usr/bin/env bash

python3 /code/service.py &
envoy -c /etc/envoy.yaml --service-cluster service
