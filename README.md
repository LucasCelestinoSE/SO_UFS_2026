# AV1 Sistemas Operacionais — Trilha A (Ollama + Open WebUI)

**Disciplina:** Sistemas Operacionais — AV1 — 2026.2
**Equipe:** Equipe 07
**Integrantes:** 
Mikael Douglas Santos Farias;
Cadmo Otávio José do Nascimento Neto; 
Mateus do Rosario Costa;
Douglas de Oliveira Déda;
Paulo Gabriel de Oliveira Cardoso;
Lucas Conceicao Celestino.

**Professor(a):** GLAUCO DE FIGUEIREDO CARNEIRO

## Resumo

Este repositório contém a implementação, os experimentos e as evidências da **Trilha A — Chat local:
Ollama + Open WebUI**, utilizando o modelo **Granite-3.1-3B-A800M-Instruct** (IBM), rodando em WSL2 com
GPU NVIDIA, comparando execução com e sem GPU.

## Modelo utilizado

| Item | Valor |
|---|---|
| Nome completo | ibm-granite/granite-3.1-3b-a800m-instruct |
| Model card | https://huggingface.co/ibm-granite/granite-3.1-3b-a800m-instruct |
| Arquitetura | Mixture of Experts (MoE) — 3B parâmetros totais / ~800M ativos por token |
| Formato / Quantização | GGUF / Q4_K_M (~2,0 GB) |
| Licença | Apache 2.0 |
| Nome no Ollama | `granite3.1-moe:3b` |
| Contexto máximo | 128.000 tokens |

Ficha técnica completa em [`docs/ficha_tecnica_modelo.md`](docs/ficha_tecnica_modelo.md).

## Ambiente experimental

| Componente | Detalhe |
|---|---|
| Host | Windows + WSL2 (Ubuntu 26.04 LTS) |
| Kernel | 6.18.33.2-microsoft-standard-WSL2 |
| CPU | Intel Xeon E5-2680 v4 @ 2.40GHz — 28 CPUs lógicas (14 núcleos × 2 threads) |
| RAM | 15 GiB |
| GPU | NVIDIA GeForce RTX 3060 — 12 GB VRAM |
| Driver / CUDA | 615.65.07 / CUDA UMD 13.4 |
| Docker | 29.8.0 |
| Ollama | 0.34.0 |
| Python | 3.14.4 |

Inventário completo (coletado automaticamente) em [`inventario/inventario.md`](inventario/inventario.md).

## Arquitetura

Três containers Docker independentes, na rede host do WSL2:

- **ollama-gpu** — servidor Ollama com acesso à GPU (`--gpus=all`), porta `11434`
- **ollama-cpu** — servidor Ollama idêntico, sem acesso à GPU, porta `11435`
- **open-webui** — interface de chat, porta `8080`, conversando com um dos dois servidores via `OLLAMA_BASE_URL`

## Como reproduzir

### 1. Pré-requisitos

- WSL2 (Ubuntu) com driver NVIDIA atualizado no Windows
- Docker Engine instalado dentro do WSL2
- NVIDIA Container Toolkit configurado (`nvidia-ctk runtime configure --runtime=docker`)

### 2. Subir a infraestrutura

Usando o `docker-compose.yml` incluído neste repositório:
```bash
docker compose up -d
docker compose ps
```
> Se os volumes `ollama-gpu-data`, `ollama-cpu-data` e `open-webui-data` ainda não existirem na sua
> máquina, remova `external: true` das definições de volume no `docker-compose.yml` antes de subir —
> veja o comentário no final do próprio arquivo.

### 3. Baixar o modelo

```bash
docker exec ollama-gpu ollama pull granite3.1-moe:3b
docker exec ollama-cpu ollama pull granite3.1-moe:3b
```

### 4. Rodar os experimentos

```bash
cd resultados
python3 ../scripts/benchmark_gpu_vs_cpu_granite.py
```
Isso executa:
- **Configuração 1 (padrão):** 5 perguntas sequenciais, uma de cada vez, em GPU e CPU.
- **Configuração 2 (concorrência/carga):** rodadas de 2, 4, 6 e 12 requisições simultâneas, em GPU e CPU.
- **Configuração 3 (ajuste de execução local):** a própria comparação GPU vs. CPU, mesmo modelo-base.

Total: 18 execuções mensuráveis (acima do mínimo de 12 exigido pela atividade).

### 5. Gerar os gráficos

```bash
python3 ../scripts/gerar_graficos_comparacao_granite.py
```
Gera 6 gráficos comparativos + um resumo textual em `resultados/graficos/`.

### 6. Coletar o inventário do ambiente

```bash
cd scripts
./coletar_inventario.sh
```
Salva em `inventario/` um `.txt` por comando e um `inventario.md` consolidado.

### 7. Coletar evidências de processos/threads/chamadas de sistema

```bash
docker exec ollama-gpu ps -eLf > evidencias/processos_threads_ollama-gpu.txt
docker exec ollama-cpu ps -eLf > evidencias/processos_threads_ollama-cpu.txt
docker stats --no-stream ollama-gpu ollama-cpu open-webui > evidencias/docker_stats.txt
nvidia-smi > evidencias/nvidia_smi_durante_execucao.txt
ss -tulpn | grep -E "11434|11435|8080" > evidencias/portas_conexoes.txt
```

## Resultados principais

| Métrica (execução sequencial) | GPU | CPU |
|---|---|---|
| Duração média | 3,41 s | 13,00 s |
| Tokens/s médio | 167,74 | 42,03 |

Com GPU, o tempo médio de resposta foi **3,81× mais rápido**, e a geração de tokens foi **3,99× mais
rápida** que apenas em CPU.

| Nível de concorrência | Duração média/req GPU (s) | Duração média/req CPU (s) |
|---|---|---|
| 2 | 1,10 | 3,74 |
| 4 | 4,88 | 22,08 |
| 6 | 8,13 | 34,52 |
| 12 | 13,35 | 63,21 |

Detalhes completos, gráficos e discussão no [relatório técnico](relatorio/relatorio_av1_granite.pdf).

## Estrutura do repositório

```
.
├── README.md
├── docker-compose.yml
├── .gitignore
├── scripts/
│   ├── benchmark_gpu_vs_cpu_granite.py     # roda os experimentos e mede tempo/CPU/RAM
│   ├── gerar_graficos_comparacao_granite.py # gera os gráficos comparativos
│   └── coletar_inventario.sh                # coleta o inventário do ambiente (Seção 6.1)
├── resultados/
│   ├── benchmark_sequencial.csv
│   ├── benchmark_concorrencia_raw.csv
│   ├── benchmark_concorrencia_summary.csv
│   └── graficos/                            # PNGs + resumo_comparacao.txt
├── evidencias/                              # processos, threads, docker stats, nvidia-smi, strace, portas
├── inventario/                              # inventário do ambiente (Seção 6.1 da atividade)
├── docs/
│   ├── ficha_tecnica_modelo.md
│   └── declaracao_ia_generativa.md
├── relatorio/
│   └── relatorio_av1_granite.pdf
└── apresentacao/
    └── [PREENCHER: slides/PDF da apresentação]
```

## Observação sobre arquivos grandes

Os pesos do modelo (`granite3.1-moe:3b`, ~2,0 GB) **não estão neste repositório** — ficam dentro dos
volumes Docker (`ollama-gpu-data`, `ollama-cpu-data`) e são baixados automaticamente com
`ollama pull granite3.1-moe:3b`, como descrito no passo 3 acima.

## Declaração de Uso de IA Generativa

Ver [`docs/declaracao_ia_generativa.md`](docs/declaracao_ia_generativa.md) e a Seção 14 do relatório
técnico.

## Video da  Atividade
https://youtu.be/3ue80ftj1Wc
