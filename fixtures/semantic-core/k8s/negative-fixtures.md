# Negative K8s Shapecheck Fixtures

These fixtures are expected to fail `k8s/tools/shapecheck.py`.

## Included

- `invalid-deployment-selector-mismatch.yaml` — Deployment selector does not match pod template labels.
- `invalid-ingress-tls-host-mismatch.yaml` — Ingress TLS host does not appear in rule hosts.
- `invalid-kubeedge-missing-edge-selector.yaml` — KubeEdge-marked Deployment lacks an edge node selector.
- `invalid-k3s-no-class.yaml` — K3s-marked Ingress omits an explicit ingress class.
