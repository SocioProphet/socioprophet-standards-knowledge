.PHONY: validate
validate:
	./.venv/bin/python tools/validate.py 2>/dev/null || python3 tools/validate.py

.PHONY: hygiene
hygiene:
	find . -name .DS_Store -delete
	make validate

.PHONY: verify
verify:
	make hygiene
	./.venv/bin/python tools/verify_knowledge_tritrpc_fixtures.py 2>/dev/null || python3 tools/verify_knowledge_tritrpc_fixtures.py

