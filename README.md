# a2a host with a2a-sdk

```sh
$ uv sync
```

### helloworld a2a

* a2a server

```base
$ uv run helloworld/server.py
```

* a2a client

```bash
$ uv run helloworld/client.py
```

### langgraph a2a

* a2a server

```base
$ export GOOGLE_API_KEY="GOOGLE_API_KEY"

$ uv run langgraph/server.py
```

* a2a client

```bash
$ uv run langgraph/client.py
```

### a2a host

* a2a servers

```bash
$ uv run helloworld/server.py
$ uv run langgraph/server.py
```

* a2a host

```bash
$ export GOOGLE_API_KEY="GOOGLE_API_KEY"

$ uv run a2a-host.py
```