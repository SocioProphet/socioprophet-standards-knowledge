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
	./.venv/bin/python tools/verify_shacl_semantic_core.py 2>/dev/null || python3 tools/verify_shacl_semantic_core.py

