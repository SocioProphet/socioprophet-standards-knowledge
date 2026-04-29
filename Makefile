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

.PHONY: fixtures
fixtures:
	./.venv/bin/python tools/generate_knowledge_tritrpc_fixtures.py 2>/dev/null || python3 tools/generate_knowledge_tritrpc_fixtures.py

.PHONY: fixtures-v1
fixtures-v1:
	KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_AVRO_PROTOCOL=schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr KC_FIXTURE_OUT=fixtures/knowledge_store_v1_vectors_hex_pathA.txt KC_NONCE_OUT=fixtures/knowledge_store_v1_vectors_hex_pathA.txt.nonces ./.venv/bin/python tools/generate_knowledge_tritrpc_fixtures.py 2>/dev/null || KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_AVRO_PROTOCOL=schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr KC_FIXTURE_OUT=fixtures/knowledge_store_v1_vectors_hex_pathA.txt KC_NONCE_OUT=fixtures/knowledge_store_v1_vectors_hex_pathA.txt.nonces python3 tools/generate_knowledge_tritrpc_fixtures.py

.PHONY: verify-v1
verify-v1:
	make hygiene
	KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_FIXTURE_OVERRIDE=fixtures/knowledge_store_v1_vectors_hex_pathA.txt KC_NONCE_OVERRIDE=fixtures/knowledge_store_v1_vectors_hex_pathA.txt.nonces ./.venv/bin/python tools/verify_knowledge_tritrpc_fixtures.py 2>/dev/null || KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_FIXTURE_OVERRIDE=fixtures/knowledge_store_v1_vectors_hex_pathA.txt KC_NONCE_OVERRIDE=fixtures/knowledge_store_v1_vectors_hex_pathA.txt.nonces python3 tools/verify_knowledge_tritrpc_fixtures.py

.PHONY: roundtrip-v1
roundtrip-v1:
	make hygiene
	KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_AVRO_PROTOCOL=schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr ./.venv/bin/python tools/verify_avro_path_a_roundtrip.py 2>/dev/null || KC_RPC_CONFIG=rpc/knowledge.store.v1.yaml KC_AVRO_PROTOCOL=schemas/avro/knowledge.store.v1/knowledge.store.v1.avpr python3 tools/verify_avro_path_a_roundtrip.py

.PHONY: verify-shacl
verify-shacl:
	./.venv/bin/python policy/tools/validate_all.py --data fixtures/shacl/semantic_core_conforms.ttl --json 2>/dev/null || python3 policy/tools/validate_all.py --data fixtures/shacl/semantic_core_conforms.ttl --json
	@if ./.venv/bin/python policy/tools/validate_all.py --data fixtures/shacl/semantic_core_violates.ttl --json >/tmp/semantic_core_violates.out 2>/tmp/semantic_core_violates.err || python3 policy/tools/validate_all.py --data fixtures/shacl/semantic_core_violates.ttl --json >/tmp/semantic_core_violates.out 2>/tmp/semantic_core_violates.err; then cat /tmp/semantic_core_violates.out; cat /tmp/semantic_core_violates.err >&2; echo "ERR: expected violating semantic-core fixture to fail"; exit 2; else cat /tmp/semantic_core_violates.out; cat /tmp/semantic_core_violates.err >&2; echo "OK: violating semantic-core fixture failed as expected"; fi

