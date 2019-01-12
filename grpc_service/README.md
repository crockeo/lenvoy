# lenvoy/grpc_service

The back-end gRPC service that powers the key/value store used by `lenvoy/service`. Provides:

1. `get(key)` &mdash; Returns a `value`, based on its `key.`
2. `set(key, value)` &mdash; Sets a `key` to a given `value`.
3. `has(key)` &mdash; Returns whether or not the store contains a `key`.
4. `clear(key)` &mdash; Clears a value, if it exists, from the store.

Refer to `protos/kv.proto` for more information.
