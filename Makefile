.PHONY: install install-dev test uninstall-hint

install:
	./install.sh

install-dev:
	WITH_DEV=1 ./install.sh

test:
	@test -x .venv/bin/pytest || { echo "rode: make install-dev"; exit 1; }
	.venv/bin/pytest -q

uninstall-hint:
	@echo "rm -f ~/.local/bin/{mage,emage,edge-mage}"
	@echo "# opcional: rm -rf .venv  (ou o clone em ~/edge-mage)"
