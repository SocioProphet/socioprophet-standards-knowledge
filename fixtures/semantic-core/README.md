# Semantic Core Smoke Fixtures

These fixtures are canonical smoke inputs for downstream runtime gates.

## Fixtures

- `abd/valid-port-socket.json` — minimal valid Agent Binding Descriptor with a port and runtime socket binding.
- `k8s/valid-nodeport-service.yaml` — minimal valid Kubernetes NodePort Service with selector labels and an in-range nodePort.

## Consumers

`SocioProphet/prophet-cli` CI should consume these fixtures instead of constructing equivalent JSON/YAML inline in workflow files.

The goal is to keep validation inputs stable, reviewable, and reusable across local CLI, CI, and release gates.
