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
