.PHONY: validate
validate:
	./.venv/bin/python tools/validate.py 2>/dev/null || python3 tools/validate.py

.PHONY: hygiene
hygiene:
	find . -name .DS_Store -delete
	make validate
