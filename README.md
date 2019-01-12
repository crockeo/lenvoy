# lenvoy

`lenvoy` = learning Envoy, aka:

1. Configuring an Envoy front-proxy.
2. Configuring a small service mesh.
3. Interact with the service mesh through a web client.

Refer to the `README.md` in each of the subfolders for individual documentation:

* `grpc_service`
* `proxy`
* `service`

### Building & Running

First ensure you have [Docker](https://www.docker.com/) and Docker Compose installed then run:

```sh
$ docker-compose up # Ctrl-C to exit

$ docker-compose up & # Start in the backgrund
$ docker-compose down # Use docker-compose down to exit
```

### License

See `LICENSE` file.
