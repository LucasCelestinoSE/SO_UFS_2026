#!/bin/bash
# coletar_inventario.sh
# ------------------------------------------------------------------------
# Coleta o "Inventário do ambiente" pedido na Seção 6.1 da atividade AV1:
# distribuição/versão do SO, kernel, CPU, RAM, GPU/VRAM, armazenamento,
# versão do Ollama, versão da camada de aplicação e ambiente de execução.
#
# Salva cada comando em um .txt separado dentro de inventario/, e monta um
# inventario.md consolidado, pronto para colar no relatório ou no repositório.
#
# Uso:
#   chmod +x coletar_inventario.sh
#   ./coletar_inventario.sh
#
# Rode a partir da pasta scripts/ do projeto (ele cria ../inventario/
# automaticamente). Se preferir, pode rodar de qualquer lugar e passar a
# pasta de destino como argumento:
#   ./coletar_inventario.sh /caminho/para/inventario
# ------------------------------------------------------------------------

set -uo pipefail

PASTA="${1:-$(dirname "$0")/../inventario}"
mkdir -p "$PASTA"
cd "$PASTA" || exit 1

echo ">> Salvando inventário em: $(pwd)"

# --------------------------------------------------------------------
# Helper: roda um comando, salva a saída (e o erro) num .txt nomeado,
# e não interrompe o script se o comando não existir.
# --------------------------------------------------------------------
run() {
  local nome="$1"; shift
  echo "   -> ${nome}"
  if command -v "$1" &> /dev/null; then
    { "$@"; } > "${nome}.txt" 2>&1
  else
    echo "Comando '$1' não encontrado neste ambiente." > "${nome}.txt"
  fi
}

# --------------------------------------------------------------------
# 1. Sistema operacional, kernel, ambiente de execução
# --------------------------------------------------------------------
run "01_uname"        uname -a
run "02_os_release"   cat /etc/os-release
run "03_ambiente_wsl" cat /proc/version   # confirma WSL2 na string do kernel

# --------------------------------------------------------------------
# 2. Processador, memória, armazenamento
# --------------------------------------------------------------------
run "04_lscpu"        lscpu
run "05_nproc"        nproc
run "06_free"         free -h
run "07_df"           df -h
run "08_lsblk"        lsblk

# --------------------------------------------------------------------
# 3. GPU (se houver)
# --------------------------------------------------------------------
if command -v nvidia-smi &> /dev/null; then
  run "09_nvidia_smi" nvidia-smi
else
  echo "GPU NVIDIA não detectada neste ambiente (nvidia-smi ausente)." > 09_nvidia_smi.txt
fi

# --------------------------------------------------------------------
# 4. Docker e camada de aplicação (host)
# --------------------------------------------------------------------
run "10_docker_version" docker --version
run "11_docker_ps"       docker ps
run "12_python_version"  python3 --version

# --------------------------------------------------------------------
# 5. Ollama — versão e modelos, DENTRO de cada container (Trilha A)
#    (o Ollama roda nos containers ollama-gpu/ollama-cpu, não no host)
# --------------------------------------------------------------------
for container in ollama-gpu ollama-cpu; do
  if docker inspect "$container" &> /dev/null; then
    echo "   -> ollama --version ($container)"
    docker exec "$container" ollama --version > "13_ollama_version_${container}.txt" 2>&1
    echo "   -> ollama list ($container)"
    docker exec "$container" ollama list > "14_ollama_list_${container}.txt" 2>&1
  else
    echo "Container '$container' não encontrado (não está rodando?)." > "13_ollama_${container}.txt"
  fi
done

# --------------------------------------------------------------------
# 6. Versão da imagem do Open WebUI (camada de aplicação)
# --------------------------------------------------------------------
if docker inspect open-webui &> /dev/null; then
  docker inspect --format='{{.Config.Image}} | Criado em: {{.Created}} | Digest: {{.Image}}' \
    open-webui > 15_open_webui_imagem.txt 2>&1
else
  echo "Container 'open-webui' não encontrado (não está rodando?)." > 15_open_webui_imagem.txt
fi

# --------------------------------------------------------------------
# Monta o inventario.md consolidado
# --------------------------------------------------------------------
{
  echo "# Inventário do ambiente"
  echo
  echo "Coletado em: $(date '+%Y-%m-%d %H:%M:%S')"
  echo
  for f in $(ls [0-9]*_*.txt 2>/dev/null | sort); do
    titulo=$(echo "$f" | sed -E 's/^[0-9]+_//; s/\.txt$//; s/_/ /g')
    echo "## ${titulo}"
    echo '```'
    cat "$f"
    echo '```'
    echo
  done
} > inventario.md

echo ""
echo "Concluído. $(ls [0-9]*_*.txt 2>/dev/null | wc -l) arquivos individuais + inventario.md salvos em:"
echo "$(pwd)"
