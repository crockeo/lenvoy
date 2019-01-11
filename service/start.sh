#!/usr/bin/env bash

python /code/service.py &
envoy -c /etc/envoy.yaml --service-cluster service
