# Negative K8s Shapecheck Fixtures

These fixtures are expected to fail `k8s/tools/shapecheck.py`.

## Included

- `invalid-deployment-selector-mismatch.yaml` — Deployment selector does not match pod template labels.
- `invalid-ingress-tls-host-mismatch.yaml` — Ingress TLS host does not appear in rule hosts.
- `invalid-kubeedge-missing-edge-selector.yaml` — KubeEdge-marked Deployment lacks an edge node selector.
- `invalid-k3s-missing-ingress-class.yaml` — K3s-marked Ingress lacks `spec.ingressClassName`.

## Notes

These are smoke fixtures for the current K8s shapecheck contract. Add focused negative fixtures as the K8s/K3s/KubeEdge shape surface grows.
