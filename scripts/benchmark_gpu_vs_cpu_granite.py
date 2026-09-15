"""
benchmark_gpu_vs_cpu.py
-------------------------
Compara desempenho e consumo de recursos entre dois containers Ollama:
  - ollama-gpu (porta 11434, com --gpus=all)
  - ollama-cpu (porta 11435, sem GPU)
rodando o mesmo modelo (granite3.1-moe:3b — Granite 3.1 3B-A800M-Instruct), na Trilha A (Ollama + Open WebUI) da
Atividade AV1, em ambiente WSL2 com GPU NVIDIA.

O que o script faz, para CADA uma das duas configurações (GPU e CPU):
  1. Roda N perguntas em SEQUÊNCIA (uma de cada vez), medindo duração e
     tokens/segundo de cada uma.
  2. Roda as mesmas perguntas em diferentes NÍVEIS DE CONCORRÊNCIA
     (2, 4, 6, 12 simultâneas), medindo duração total, throughput e falhas.
  3. Em paralelo às requisições, coleta `docker stats` do respectivo
     container (CPU%, memória) via subprocess.

Pré-requisitos:
    pip3 install requests
    Containers já rodando (ver guia_projeto_trilha_a_wsl_gpu.md):
        docker run -d --gpus=all -p 11434:11434 --name ollama-gpu ollama/ollama
        docker run -d -p 11435:11434 --name ollama-cpu ollama/ollama
        docker exec ollama-gpu ollama pull granite3.1-moe:3b
        docker exec ollama-cpu ollama pull granite3.1-moe:3b

Uso:
    python3 benchmark_gpu_vs_cpu.py
"""

import subprocess
import threading
import time
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    raise SystemExit("Instale a dependência antes de rodar: pip3 install requests")

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

CONFIGURACOES = [
    {"nome": "GPU", "container": "ollama-gpu", "url": "http://localhost:11434/api/generate"},
    {"nome": "CPU", "container": "ollama-cpu", "url": "http://localhost:11435/api/generate"},
]

MODELO = "granite3.1-moe:3b"
INTERVALO_DOCKER_STATS = 1.0  # segundos entre leituras de `docker stats`
NIVEIS_CONCORRENCIA = [2, 4, 6, 12]
TIMEOUT_REQUISICAO_S = 900  # 15 min — aumentado por causa de rodadas CPU com alta concorrência

POOL_PROMPTS = [
    "O que é um sistema operacional?",
    "Explique em uma frase o que é uma thread.",
    "O que faz o escalonador de processos?",
    "Explique detalhadamente a diferença entre processos e threads em um "
    "sistema operacional, incluindo como o escalonador decide qual executar.",
    "Descreva passo a passo como uma chamada de sistema funciona, desde o "
    "processo em modo usuário até o retorno do kernel.",
]

SEQUENCIAL_CSV = "benchmark_sequencial.csv"
CONCORRENCIA_RAW_CSV = "benchmark_concorrencia_raw.csv"
CONCORRENCIA_SUMMARY_CSV = "benchmark_concorrencia_summary.csv"

# ---------------------------------------------------------------------------
# Coleta de docker stats de um container específico
# ---------------------------------------------------------------------------

def _ler_docker_stats(container):
    """Lê uma amostra pontual de CPU% e memória (MB) de um container via
    `docker stats --no-stream`."""
    try:
        resultado = subprocess.run(
            ["docker", "stats", container, "--no-stream", "--format",
             "{{.CPUPerc}}|{{.MemUsage}}"],
            capture_output=True, text=True, timeout=10
        )
        linha = resultado.stdout.strip()
        if not linha:
            return 0.0, 0.0
        cpu_str, mem_str = linha.split("|")
        cpu_pct = float(cpu_str.replace("%", "").strip())
        # MemUsage vem tipo "123.4MiB / 8GiB" -> pega só o primeiro valor em MiB
        mem_usada = mem_str.split("/")[0].strip()
        if "GiB" in mem_usada:
            mem_mb = float(mem_usada.replace("GiB", "")) * 1024
        else:
            mem_mb = float(mem_usada.replace("MiB", ""))
        return cpu_pct, round(mem_mb, 1)
    except Exception:
        return 0.0, 0.0


def _monitorar_container(container, amostras, parar):
    t0 = time.time()
    while not parar.is_set():
        ts = round(time.time() - t0, 2)
        cpu, mem = _ler_docker_stats(container)
        amostras.append((ts, cpu, mem))
        time.sleep(INTERVALO_DOCKER_STATS)


def resumir_amostras(amostras):
    if not amostras:
        return {"cpu_media": 0, "cpu_pico": 0, "mem_media": 0, "mem_pico": 0}
    cpus = [a[1] for a in amostras]
    mems = [a[2] for a in amostras]
    return {
        "cpu_media": round(sum(cpus) / len(cpus), 2),
        "cpu_pico": round(max(cpus), 2),
        "mem_media": round(sum(mems) / len(mems), 2),
        "mem_pico": round(max(mems), 2),
    }


# ---------------------------------------------------------------------------
# Requisição individual ao Ollama
# ---------------------------------------------------------------------------

def _chamar_ollama(url, prompt):
    inicio = time.time()
    payload = {"model": MODELO, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=TIMEOUT_REQUISICAO_S)
        duracao = round(time.time() - inicio, 2)
        resp.raise_for_status()
        dados = resp.json()
        eval_count = dados.get("eval_count", 0)
        eval_duration_s = dados.get("eval_duration", 0) / 1e9
        tokens_por_s = round(eval_count / eval_duration_s, 2) if eval_duration_s > 0 else 0
        return {"ok": True, "duracao_s": duracao, "tokens_por_s": tokens_por_s,
                "eval_count": eval_count}
    except requests.RequestException as e:
        duracao = round(time.time() - inicio, 2)
        print(f"   [AVISO] Falha na requisição ('{prompt[:40]}...'): {e}")
        return {"ok": False, "duracao_s": duracao, "tokens_por_s": 0, "eval_count": 0}


# ---------------------------------------------------------------------------
# Fase 1: testes sequenciais (uma pergunta de cada vez)
# ---------------------------------------------------------------------------

def rodar_testes_sequenciais(writer):
    for cfg in CONFIGURACOES:
        print(f"\n=== Testes sequenciais — {cfg['nome']} ({cfg['container']}) ===")
        for i, prompt in enumerate(POOL_PROMPTS, start=1):
            resultado = _chamar_ollama(cfg["url"], prompt)
            cpu, mem = _ler_docker_stats(cfg["container"])
            writer.writerow([cfg["nome"], i, prompt[:50], resultado["duracao_s"],
                              resultado["tokens_por_s"], resultado["eval_count"],
                              cpu, mem, resultado["ok"]])
            print(f"   [{i}/{len(POOL_PROMPTS)}] {resultado['duracao_s']}s | "
                  f"{resultado['tokens_por_s']} tok/s | CPU cont.: {cpu}% | "
                  f"RAM cont.: {mem} MB")


# ---------------------------------------------------------------------------
# Fase 2: testes de concorrência
# ---------------------------------------------------------------------------

def rodar_rodada_concorrente(cfg, nivel, raw_writer):
    prompts = [POOL_PROMPTS[i % len(POOL_PROMPTS)] for i in range(nivel)]

    amostras = []
    parar = threading.Event()
    thread_monitor = threading.Thread(
        target=_monitorar_container, args=(cfg["container"], amostras, parar)
    )
    thread_monitor.start()

    inicio_rodada = time.time()
    resultados = []
    with ThreadPoolExecutor(max_workers=nivel) as executor:
        futures = [executor.submit(_chamar_ollama, cfg["url"], p) for p in prompts]
        for future in as_completed(futures):
            resultados.append(future.result())
    duracao_total = round(time.time() - inicio_rodada, 2)

    parar.set()
    thread_monitor.join()

    for ts, cpu, mem in amostras:
        raw_writer.writerow([cfg["nome"], nivel, ts, cpu, mem])

    return amostras, resultados, duracao_total


def rodar_testes_concorrencia(raw_writer, summary_writer):
    for cfg in CONFIGURACOES:
        for nivel in NIVEIS_CONCORRENCIA:
            print(f"\n>> [{cfg['nome']}] {nivel} requisições simultâneas...")
            amostras, resultados, duracao_total = rodar_rodada_concorrente(
                cfg, nivel, raw_writer
            )
            metrics = resumir_amostras(amostras)
            duracoes = [r["duracao_s"] for r in resultados]
            tokens_s = [r["tokens_por_s"] for r in resultados if r["ok"]]
            falhas = sum(1 for r in resultados if not r["ok"])
            throughput = round(nivel / duracao_total, 3) if duracao_total > 0 else 0

            linha = {
                "config": cfg["nome"],
                "nivel_concorrencia": nivel,
                "duracao_total_s": duracao_total,
                "duracao_media_req_s": round(sum(duracoes) / len(duracoes), 2),
                "duracao_max_req_s": round(max(duracoes), 2),
                "tokens_por_s_media": round(sum(tokens_s) / len(tokens_s), 2) if tokens_s else 0,
                "throughput_req_s": throughput,
                "falhas": falhas,
                "cpu_media_pct": metrics["cpu_media"],
                "cpu_pico_pct": metrics["cpu_pico"],
                "mem_media_mb": metrics["mem_media"],
                "mem_pico_mb": metrics["mem_pico"],
            }
            summary_writer.writerow(linha)
            print(f"   duração total: {duracao_total}s | "
                  f"média/req: {linha['duracao_media_req_s']}s | "
                  f"tok/s médio: {linha['tokens_por_s_media']} | "
                  f"CPU cont. pico: {linha['cpu_pico_pct']}% | "
                  f"RAM cont. pico: {linha['mem_pico_mb']} MB | falhas: {falhas}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Verifica se os dois containers respondem antes de começar
    for cfg in CONFIGURACOES:
        try:
            requests.get(cfg["url"].replace("/api/generate", ""), timeout=5)
        except requests.RequestException:
            raise SystemExit(
                f"Não consegui conectar em {cfg['url']} ({cfg['container']}). "
                "Confirme que o container está rodando: docker ps"
            )

    print(">> Fase 1: testes sequenciais (GPU vs CPU)")
    with open(SEQUENCIAL_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["config", "execucao_id", "pergunta", "duracao_s",
                          "tokens_por_s", "eval_count", "cpu_container_pct",
                          "mem_container_mb", "ok"])
        rodar_testes_sequenciais(writer)

    print("\n>> Fase 2: testes de concorrência (GPU vs CPU)")
    with open(CONCORRENCIA_RAW_CSV, "w", newline="") as f_raw, \
         open(CONCORRENCIA_SUMMARY_CSV, "w", newline="") as f_sum:
        raw_writer = csv.writer(f_raw)
        raw_writer.writerow(["config", "nivel_concorrencia", "tempo_s",
                              "cpu_container_pct", "mem_container_mb"])

        campos_resumo = ["config", "nivel_concorrencia", "duracao_total_s",
                          "duracao_media_req_s", "duracao_max_req_s",
                          "tokens_por_s_media", "throughput_req_s", "falhas",
                          "cpu_media_pct", "cpu_pico_pct", "mem_media_mb", "mem_pico_mb"]
        summary_writer = csv.DictWriter(f_sum, fieldnames=campos_resumo)
        summary_writer.writeheader()

        rodar_testes_concorrencia(raw_writer, summary_writer)

    print(f"\nConcluído. Arquivos gerados:\n"
          f"  {SEQUENCIAL_CSV}\n  {CONCORRENCIA_RAW_CSV}\n  {CONCORRENCIA_SUMMARY_CSV}")
    print("Compare as linhas 'GPU' vs 'CPU' em cada CSV para o gráfico "
          "comparativo do relatório (tempo de resposta, tokens/s, CPU%, RAM).")


if __name__ == "__main__":
    main()
