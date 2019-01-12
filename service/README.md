# lenvoy/service

HTTP service that gets mapped to `localhost:8000`. Interacts with the internal `lenvoy/grpc_service` to:

1. Provide publicly available routes to run `clear` and `has` on the key/value store.

2. Provide a count of how many times you've navigated to `localhost:8000`.
