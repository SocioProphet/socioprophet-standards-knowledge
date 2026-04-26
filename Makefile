.PHONY: validate
validate:
	./.venv/bin/python tools/validate.py 2>/dev/null || python3 tools/validate.py

.PHONY: hygiene
hygiene:
	for i in 1 2 3 4 5; do find . -name .DS_Store -delete; n=$$(find . -name .DS_Store | wc -l | tr -d " "); echo "DS_Store remaining: $$n"; [ "$$n" = "0" ] && break; sleep 0.2; done
	make validate
.PHONY: verify
verify:
	make hygiene
	./.venv/bin/python tools/verify_knowledge_tritrpc_fixtures.py 2>/dev/null || python3 tools/verify_knowledge_tritrpc_fixtures.py

.PHONY: roundtrip
roundtrip:
	make hygiene
	./.venv/bin/python tools/verify_avro_path_a_roundtrip.py 2>/dev/null || python3 tools/verify_avro_path_a_roundtrip.py

.PHONY: verify-shacl
verify-shacl:
	./.venv/bin/python policy/tools/validate_all.py --data fixtures/shacl/semantic_core_conforms.ttl --json 2>/dev/null || python3 policy/tools/validate_all.py --data fixtures/shacl/semantic_core_conforms.ttl --json
	@if ./.venv/bin/python policy/tools/validate_all.py --data fixtures/shacl/semantic_core_violates.ttl --json >/tmp/semantic_core_violates.out 2>/tmp/semantic_core_violates.err || python3 policy/tools/validate_all.py --data fixtures/shacl/semantic_core_violates.ttl --json >/tmp/semantic_core_violates.out 2>/tmp/semantic_core_violates.err; then cat /tmp/semantic_core_violates.out; cat /tmp/semantic_core_violates.err >&2; echo "ERR: expected violating semantic-core fixture to fail"; exit 2; else cat /tmp/semantic_core_violates.out; cat /tmp/semantic_core_violates.err >&2; echo "OK: violating semantic-core fixture failed as expected"; fi

.PHONY: verify-abd
verify-abd:
	python3 Lower/tools/validate_abd.py --abd fixtures/semantic-core/abd/valid-port-socket.json --json

.PHONY: verify-k8s
verify-k8s:
	python3 k8s/tools/shapecheck.py --manifest fixtures/semantic-core/k8s/valid-nodeport-service.yaml fixtures/semantic-core/k8s/valid-deployment-service-ingress.yaml fixtures/semantic-core/k8s/valid-k3s-ingress.yaml fixtures/semantic-core/k8s/valid-kubeedge-deployment.yaml --json
	@if python3 k8s/tools/shapecheck.py --manifest fixtures/semantic-core/k8s/invalid-deployment-selector-mismatch.yaml --json; then echo "ERR: expected invalid deployment selector fixture to fail"; exit 2; else echo "OK: invalid deployment selector fixture failed as expected"; fi
	@if python3 k8s/tools/shapecheck.py --manifest fixtures/semantic-core/k8s/invalid-ingress-tls-host-mismatch.yaml --json; then echo "ERR: expected invalid ingress TLS fixture to fail"; exit 2; else echo "OK: invalid ingress TLS fixture failed as expected"; fi
	@if python3 k8s/tools/shapecheck.py --manifest fixtures/semantic-core/k8s/invalid-kubeedge-missing-edge-selector.yaml --json; then echo "ERR: expected invalid KubeEdge fixture to fail"; exit 2; else echo "OK: invalid KubeEdge fixture failed as expected"; fi

