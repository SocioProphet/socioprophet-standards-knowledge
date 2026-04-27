.PHONY: validate
validate:
	./.venv/bin/python tools/validate.py 2>/dev/null || python3 tools/validate.py

.PHONY: multidomain-geospatial-validate
multidomain-geospatial-validate:
	./.venv/bin/python tools/validate_multidomain_geospatial_knowledge.py 2>/dev/null || python3 tools/validate_multidomain_geospatial_knowledge.py

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

