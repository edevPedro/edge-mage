#!/usr/bin/env bash
# Instala Edge Mage com entrypoints globais em ~/.local/bin
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
VENV="${ROOT}/.venv"
PYTHON="${PYTHON:-}"

pick_python() {
  if [[ -n "${PYTHON}" ]]; then
    echo "${PYTHON}"
    return
  fi
  for cand in python3.13 python3.12 python3.11 python3; do
    if command -v "${cand}" >/dev/null 2>&1; then
      ver="$("${cand}" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"
      major="${ver%%.*}"
      minor="${ver#*.}"
      if [[ "${major}" -gt 3 ]] || { [[ "${major}" -eq 3 ]] && [[ "${minor}" -ge 11 ]]; }; then
        echo "${cand}"
        return
      fi
    fi
  done
  echo "erro: precisa de Python 3.11+" >&2
  exit 1
}

PY="$(pick_python)"
echo "==> Python: ${PY}"
echo "==> Projeto: ${ROOT}"

if [[ "${USE_PIPX:-0}" == "1" ]] && command -v pipx >/dev/null 2>&1; then
  echo "==> pipx install -e ."
  (cd "${ROOT}" && pipx install -e . --force)
  echo "==> OK (pipx). Comandos: edge-mage, emage, mage"
  command -v edge-mage && which edge-mage
  exit 0
fi

mkdir -p "${BIN_DIR}"
if [[ ! -d "${VENV}" ]]; then
  echo "==> criando venv em ${VENV}"
  "${PY}" -m venv "${VENV}"
fi

echo "==> instalando (editable) no venv"
"${VENV}/bin/pip" install -U pip setuptools wheel >/dev/null
"${VENV}/bin/pip" install -e "${ROOT}[dev]"

for cmd in edge-mage emage mage; do
  target="${VENV}/bin/${cmd}"
  if [[ ! -x "${target}" ]]; then
    echo "erro: entrypoint ausente: ${target}" >&2
    exit 1
  fi
  # Wrapper estável (sobrevive a recreate do venv path)
  cat > "${BIN_DIR}/${cmd}" <<EOF
#!/usr/bin/env bash
exec "${ROOT}/.venv/bin/${cmd}" "\$@"
EOF
  chmod +x "${BIN_DIR}/${cmd}"
  echo "==> ${BIN_DIR}/${cmd} -> ${target}"
done

if ! command -v edge-mage >/dev/null 2>&1; then
  echo ""
  echo "AVISO: ${BIN_DIR} não está no PATH."
  echo "Adicione ao shell (zsh/bash):"
  echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
  echo "Depois: source ~/.zshrc   # ou abra um terminal novo"
else
  echo ""
  echo "OK: $(command -v edge-mage)"
fi

echo ""
echo "Verifique de qualquer pasta:"
echo "  which edge-mage && edge-mage --help 2>/dev/null || which emage"
echo "Comandos: edge-mage | emage | mage"
