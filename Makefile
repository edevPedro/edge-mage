.PHONY: install test

install:
	./install.sh

test:
	.venv/bin/pytest -q
