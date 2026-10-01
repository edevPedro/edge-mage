#!/usr/bin/env bash
# e-mage — instalador (clone local ou curl|bash)
# Uso:
#   ./install.sh
#   curl -fsSL https://raw.githubusercontent.com/edevPedro/edge-mage/main/install.sh | bash
set -euo pipefail

REPO_URL="${EDGE_MAGE_REPO_URL:-https://github.com/edevPedro/edge-mage.git}"
REPO_BRANCH="${EDGE_MAGE_BRANCH:-main}"
BIN_DIR="${HOME}/.local/bin"
DEFAULT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/e-mage"
CLONE_DIR="${EDGE_MAGE_HOME:-${HOME}/edge-mage}"
PYTHON="${PYTHON:-}"

die() {
  echo "erro: $*" >&2
  exit 1
}

info() {
  # stderr: stdout é só o path em ensure_repo / pick_python
  echo "==> $*" >&2
}

# --- localizar / obter o código ---------------------------------------------

resolve_root() {
  local script="${BASH_SOURCE[0]:-}"
  local base=""
  local script_dir=""

  # curl|bash / bash -s: sem path real do install.sh
  # (cuidado: $0 vira "bash" e dirname="." = cwd — não usar)
  if [[ -z "${script}" ]] \
    || [[ "${script}" == "bash" ]] \
    || [[ "${script}" == "-bash" ]] \
    || [[ "${script}" == /dev/fd/* ]] \
    || [[ "${script}" == /proc/self/fd/* ]] \
    || [[ "${script}" == /dev/stdin ]]; then
    echo ""
    return
  fi

  base="$(basename "${script}")"
  [[ "${base}" == "install.sh" ]] || { echo ""; return; }

  if script_dir="$(cd "$(dirname "${script}")" 2>/dev/null && pwd)"; then
    if [[ -f "${script_dir}/pyproject.toml" ]] \
      && grep -Eq 'name = "(e-mage|edge-mage)"' "${script_dir}/pyproject.toml" 2>/dev/null; then
      echo "${script_dir}"
      return
    fi
  fi
  echo ""
}

ensure_repo() {
  local root
  root="$(resolve_root)"
  if [[ -n "${root}" ]]; then
    echo "${root}"
    return
  fi

  command -v git >/dev/null 2>&1 || die "git não encontrado (precisa pra clonar o repo)"

  local dest="${CLONE_DIR}"
  if [[ ! -d "${dest}/.git" ]]; then
    # fallback XDG se ~/edge-mage já existir sem ser o repo
    if [[ -e "${dest}" ]] && [[ ! -d "${dest}/.git" ]]; then
      dest="${DEFAULT_HOME}"
    fi
    info "clonando ${REPO_URL} → ${dest}"
    mkdir -p "$(dirname "${dest}")"
    git clone --depth 1 --branch "${REPO_BRANCH}" "${REPO_URL}" "${dest}"
  else
    info "atualizando ${dest} (${REPO_BRANCH})"
    git -C "${dest}" fetch --depth 1 origin "${REPO_BRANCH}"
    git -C "${dest}" checkout "${REPO_BRANCH}"
    git -C "${dest}" pull --ff-only origin "${REPO_BRANCH}" || true
  fi

  [[ -f "${dest}/pyproject.toml" ]] || die "clone inválido em ${dest}"
  echo "${dest}"
}

# --- python -----------------------------------------------------------------

pick_python() {
  if [[ -n "${PYTHON}" ]]; then
    if ! command -v "${PYTHON}" >/dev/null 2>&1; then
      die "PYTHON='${PYTHON}' não encontrado no PATH"
    fi
    echo "${PYTHON}"
    return
  fi
  local cand ver major minor
  for cand in python3.13 python3.12 python3.11 python3; do
    if command -v "${cand}" >/dev/null 2>&1; then
      ver="$("${cand}" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")' 2>/dev/null)" || continue
      major="${ver%%.*}"
      minor="${ver#*.}"
      if [[ "${major}" -gt 3 ]] || { [[ "${major}" -eq 3 ]] && [[ "${minor}" -ge 11 ]]; }; then
        echo "${cand}"
        return
      fi
    fi
  done
  die "precisa de Python 3.11+ (achei só versões antigas, ou nenhum python3). Instale 3.11+ e rode de novo."
}

# --- install ----------------------------------------------------------------

ROOT="$(ensure_repo)"
PY="$(pick_python)"
VENV="${EDGE_MAGE_VENV:-${ROOT}/.venv}"

info "Python: ${PY} ($("${PY}" -c 'import sys; print(sys.version.split()[0])'))"
info "Projeto: ${ROOT}"
info "Venv: ${VENV}"

if [[ "${USE_PIPX:-0}" == "1" ]]; then
  command -v pipx >/dev/null 2>&1 || die "USE_PIPX=1 mas pipx não está no PATH"
  info "pipx install -e ."
  (cd "${ROOT}" && pipx install -e . --force)
  echo ""
  echo "OK (pipx). Comandos: mage | emage | edge-mage"
  command -v mage >/dev/null 2>&1 && which mage
  exit 0
fi

mkdir -p "${BIN_DIR}"
if [[ ! -d "${VENV}" ]]; then
  info "criando venv"
  "${PY}" -m venv "${VENV}" || die "falha ao criar venv (python -m venv)"
fi

info "pip install -e ."
"${VENV}/bin/pip" install -U pip setuptools wheel >/dev/null
if [[ "${WITH_DEV:-0}" == "1" ]]; then
  "${VENV}/bin/pip" install -e "${ROOT}[dev]"
else
  "${VENV}/bin/pip" install -e "${ROOT}"
fi

for cmd in edge-mage emage mage; do
  target="${VENV}/bin/${cmd}"
  [[ -x "${target}" ]] || die "entrypoint ausente após install: ${target}"
  ln -sfn "${target}" "${BIN_DIR}/${cmd}"
  info "${BIN_DIR}/${cmd} → ${target}"
done

# PATH check — use explicit path; command -v may miss new symlink in same shell
echo ""
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  echo "AVISO: ${BIN_DIR} não está no PATH."
  echo "Adicione (zsh/bash):"
  echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
  echo "Depois: source ~/.zshrc   # ou abra um terminal novo"
  echo ""
  echo "Enquanto isso, rode:"
  echo "  ${BIN_DIR}/mage --version"
else
  echo "OK: mage no PATH"
fi

echo ""
echo "Próximo passo:"
echo "  mage --version"
echo "  mage          # course launcher"
echo "  mage sync     # packs + progress stub"
echo ""
echo "Teste de qualquer pasta:"
echo "  cd /tmp && mage --version"
echo ""
echo "Comandos: mage | emage | edge-mage"
echo "Progresso: ~/.mage/progress.json  (migra de ~/.edge-mage/ na 1ª execução)"
