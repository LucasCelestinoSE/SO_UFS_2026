"""
gerar_graficos_comparacao.py
------------------------------
Lê os CSVs gerados pelo benchmark_gpu_vs_cpu.py e produz gráficos comparando
a execução do Granite 3.1 3B-A800M-Instruct (MoE) COM GPU (container ollama-gpu) e SEM GPU
(container ollama-cpu), prontos para colar no relatório da AV1.

Espera encontrar, na mesma pasta:
    - benchmark_sequencial.csv
    - benchmark_concorrencia_summary.csv

Gera (todos em ./graficos/):
    1. duracao_sequencial.png     -> tempo de resposta por pergunta, GPU vs CPU
    2. tokens_por_s_sequencial.png -> tokens/segundo por pergunta, GPU vs CPU
    3. duracao_vs_concorrencia.png -> tempo médio de resposta x nível de concorrência
    4. throughput_vs_concorrencia.png -> requisições/segundo x nível de concorrência
    5. cpu_pico_vs_concorrencia.png   -> % de CPU do container x nível de concorrência
    6. mem_pico_vs_concorrencia.png   -> memória do container (MB) x nível de concorrência
    7. resumo_comparacao.txt         -> resumo em texto (speedup médio, etc.)

Pré-requisitos:
    pip3 install pandas matplotlib

Uso:
    python3 gerar_graficos_comparacao.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

SEQUENCIAL_CSV = "benchmark_sequencial.csv"
CONCORRENCIA_SUMMARY_CSV = "benchmark_concorrencia_summary.csv"
PASTA_SAIDA = "graficos"
MODELO_LABEL = "Granite 3.1 3B-A800M-Instruct (MoE)"  # ajuste aqui se trocar de modelo de novo

CORES = {"GPU": "#2E86AB", "CPU": "#E76F51"}


def preparar_pasta():
    os.makedirs(PASTA_SAIDA, exist_ok=True)


def carregar_dados():
    if not os.path.exists(SEQUENCIAL_CSV):
        raise SystemExit(f"Arquivo não encontrado: {SEQUENCIAL_CSV}. "
                          "Rode benchmark_gpu_vs_cpu.py primeiro.")
    if not os.path.exists(CONCORRENCIA_SUMMARY_CSV):
        raise SystemExit(f"Arquivo não encontrado: {CONCORRENCIA_SUMMARY_CSV}. "
                          "Rode benchmark_gpu_vs_cpu.py primeiro.")
    seq = pd.read_csv(SEQUENCIAL_CSV)
    conc = pd.read_csv(CONCORRENCIA_SUMMARY_CSV)
    return seq, conc


# ---------------------------------------------------------------------------
# Gráficos da fase sequencial (uma pergunta de cada vez)
# ---------------------------------------------------------------------------

def grafico_duracao_sequencial(seq):
    pivot = seq.pivot_table(index="execucao_id", columns="config",
                             values="duracao_s", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot(kind="bar", ax=ax, color=[CORES.get(c, "gray") for c in pivot.columns])
    ax.set_title("Tempo de resposta por pergunta — GPU vs CPU")
    ax.set_xlabel("Pergunta (nº na sequência)")
    ax.set_ylabel("Duração (segundos)")
    ax.legend(title="Configuração")
    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "duracao_sequencial.png")
    plt.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Gerado: {caminho}")


def grafico_tokens_sequencial(seq):
    pivot = seq.pivot_table(index="execucao_id", columns="config",
                             values="tokens_por_s", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot(kind="bar", ax=ax, color=[CORES.get(c, "gray") for c in pivot.columns])
    ax.set_title("Tokens gerados por segundo — GPU vs CPU")
    ax.set_xlabel("Pergunta (nº na sequência)")
    ax.set_ylabel("Tokens / segundo")
    ax.legend(title="Configuração")
    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, "tokens_por_s_sequencial.png")
    plt.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Gerado: {caminho}")


# ---------------------------------------------------------------------------
# Gráficos da fase de concorrência (linhas por nível de concorrência)
# ---------------------------------------------------------------------------

def _grafico_linha_por_config(conc, coluna_y, titulo, rotulo_y, nome_arquivo):
    fig, ax = plt.subplots(figsize=(8, 5))
    for config, cor in CORES.items():
        dados = conc[conc["config"] == config].sort_values("nivel_concorrencia")
        if dados.empty:
            continue
        ax.plot(dados["nivel_concorrencia"], dados[coluna_y],
                marker="o", label=config, color=cor, linewidth=2)
    ax.set_title(titulo)
    ax.set_xlabel("Nível de concorrência (nº de requisições simultâneas)")
    ax.set_ylabel(rotulo_y)
    ax.legend(title="Configuração")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    caminho = os.path.join(PASTA_SAIDA, nome_arquivo)
    plt.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"Gerado: {caminho}")


def grafico_duracao_vs_concorrencia(conc):
    _grafico_linha_por_config(
        conc, "duracao_media_req_s",
        "Tempo médio de resposta por nível de concorrência",
        "Duração média por requisição (s)",
        "duracao_vs_concorrencia.png",
    )


def grafico_throughput_vs_concorrencia(conc):
    _grafico_linha_por_config(
        conc, "throughput_req_s",
        "Throughput por nível de concorrência",
        "Requisições completadas / segundo",
        "throughput_vs_concorrencia.png",
    )


def grafico_cpu_vs_concorrencia(conc):
    _grafico_linha_por_config(
        conc, "cpu_pico_pct",
        "Uso de CPU do container (pico) por nível de concorrência",
        "CPU do container (%)",
        "cpu_pico_vs_concorrencia.png",
    )


def grafico_mem_vs_concorrencia(conc):
    _grafico_linha_por_config(
        conc, "mem_pico_mb",
        "Uso de memória do container (pico) por nível de concorrência",
        "Memória do container (MB)",
        "mem_pico_vs_concorrencia.png",
    )


# ---------------------------------------------------------------------------
# Resumo textual da comparação (para colar direto no relatório)
# ---------------------------------------------------------------------------

def gerar_resumo_texto(seq, conc):
    linhas = [f"Resumo comparativo — {MODELO_LABEL} com GPU vs. sem GPU", "=" * 55, ""]

    # --- Fase sequencial ---
    media_seq = seq.groupby("config")[["duracao_s", "tokens_por_s"]].mean().round(2)
    linhas.append("Fase sequencial (médias das perguntas):")
    linhas.append(media_seq.to_string())
    linhas.append("")

    if "GPU" in media_seq.index and "CPU" in media_seq.index:
        speedup_tempo = round(media_seq.loc["CPU", "duracao_s"] /
                               media_seq.loc["GPU", "duracao_s"], 2)
        speedup_tokens = round(media_seq.loc["GPU", "tokens_por_s"] /
                                media_seq.loc["CPU", "tokens_por_s"], 2) \
            if media_seq.loc["CPU", "tokens_por_s"] > 0 else float("inf")
        linhas.append(f"-> Com GPU, o tempo médio de resposta foi {speedup_tempo}x "
                       f"mais rápido que só CPU.")
        linhas.append(f"-> Com GPU, a geração de tokens foi {speedup_tokens}x "
                       f"mais rápida (tokens/s) que só CPU.")
        linhas.append("")

    # --- Fase de concorrência ---
    linhas.append("Fase de concorrência (por nível):")
    tabela_conc = conc.pivot_table(
        index="nivel_concorrencia", columns="config",
        values=["duracao_media_req_s", "throughput_req_s", "falhas"]
    ).round(2)
    linhas.append(tabela_conc.to_string())
    linhas.append("")

    linhas.append(
        "Interpretação sugerida para o relatório: observe se o tempo médio por "
        "requisição da configuração CPU cresce mais rápido conforme o nível de "
        "concorrência aumenta (sinal de fila/escalonamento saturando a CPU), "
        "enquanto a GPU tende a sustentar tempos mais estáveis até o ponto em "
        "que a VRAM ou o paralelismo do Ollama vira o gargalo."
    )

    caminho = os.path.join(PASTA_SAIDA, "resumo_comparacao.txt")
    with open(caminho, "w") as f:
        f.write("\n".join(linhas))
    print(f"Gerado: {caminho}")
    print("\n" + "\n".join(linhas))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    preparar_pasta()
    seq, conc = carregar_dados()

    grafico_duracao_sequencial(seq)
    grafico_tokens_sequencial(seq)
    grafico_duracao_vs_concorrencia(conc)
    grafico_throughput_vs_concorrencia(conc)
    grafico_cpu_vs_concorrencia(conc)
    grafico_mem_vs_concorrencia(conc)
    gerar_resumo_texto(seq, conc)

    print(f"\nTudo pronto. Gráficos e resumo salvos na pasta '{PASTA_SAIDA}/'.")


if __name__ == "__main__":
    main()
