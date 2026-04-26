# Negative K8s Shapecheck Fixtures

These fixtures are expected to fail `k8s/tools/shapecheck.py`.

## Included

- `invalid-deployment-selector-mismatch.yaml` — Deployment selector does not match pod template labels.
- `invalid-ingress-tls-host-mismatch.yaml` — Ingress TLS host does not appear in rule hosts.
- `invalid-kubeedge-missing-edge-selector.yaml` — KubeEdge-marked Deployment lacks an edge node selector.

## Pending

A K3s negative fixture for a K3s-marked Ingress without `spec.ingressClassName` should be added as a follow-up. The shape exists in `k8s/shapes/k8s.shacl.ttl`; only the committed negative fixture is pending.
