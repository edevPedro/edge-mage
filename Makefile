.PHONY: install install-dev test lint-resources uninstall-hint

install:
	./install.sh

install-dev:
	WITH_DEV=1 ./install.sh

test:
	@test -x .venv/bin/pytest || { echo "rode: make install-dev"; exit 1; }
	.venv/bin/pytest -q
	.venv/bin/python scripts/lint_resources.py

lint-resources:
	@test -x .venv/bin/python || { echo "rode: make install-dev"; exit 1; }
	.venv/bin/python scripts/lint_resources.py

uninstall-hint:
	@echo "rm -f ~/.local/bin/{mage,emage,edge-mage}"
	@echo "# opcional: rm -rf .venv  (ou o clone em ~/edge-mage)"
	@echo "# progresso: ~/.mage/  (legado: ~/.edge-mage/)"
