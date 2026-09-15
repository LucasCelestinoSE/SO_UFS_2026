# Ficha técnica do modelo — Granite 3.1 3B-A800M-Instruct

| Item | Valor |
|---|---|
| Organização | IBM (Granite Team) |
| Nome completo do modelo | ibm-granite/granite-3.1-3b-a800m-instruct |
| URL do model card (Hugging Face) | https://huggingface.co/ibm-granite/granite-3.1-3b-a800m-instruct |
| Arquitetura | Mixture of Experts (MoE) — `GraniteMoeForCausalLM` |
| Nº total de parâmetros | 3 bilhões (3B) |
| Nº de parâmetros ativos por token | ~800 milhões (A800M) |
| Variante | Instruct |
| Formato utilizado | GGUF |
| Quantização utilizada | Q4_K_M *(ajuste se sua equipe usar outra)* |
| Nome no Ollama | `granite3.1-moe:3b` |
| Licença | Apache 2.0 |
| Contexto máximo | 128.000 tokens (long-context) |
| Idiomas suportados oficialmente | Inglês, alemão, espanhol, francês, japonês, português, árabe, tcheco, italiano, coreano, holandês, chinês |
| Data de lançamento | 18 de dezembro de 2024 |
| Dados de treinamento | Mais de 10 trilhões de tokens (família Granite 3.1 MoE) |

## O que muda em relação a um modelo denso (ex.: Phi-4-mini)

O Granite-3.1-3B-A800M-Instruct é um modelo **Mixture of Experts (MoE)**: apesar de ter 3 bilhões de
parâmetros no total, apenas cerca de **800 milhões são ativados por token** durante a inferência. Isso o
diferencia estruturalmente de um modelo denso como o Phi-4-mini (3,8B, todos os parâmetros ativos em
toda inferência):

- **Custo computacional por token menor**: mesmo "pesando" 3B, o custo de inferência por token se
  aproxima do de um modelo denso bem menor (~800M), o que tende a se traduzir em respostas mais
  rápidas e menor uso de CPU/GPU por requisição.
- **Memória (RAM/VRAM) ainda reflete o total de parâmetros**: os 3B de parâmetros do modelo (todos os
  "especialistas") precisam ficar carregados em memória, mesmo que só uma fração seja usada a cada
  token — então a economia de recursos aparece principalmente em **tempo de computação**, não
  necessariamente em **memória ocupada**.
- **Roteamento dinâmico**: a cada token, um mecanismo de roteamento decide quais "especialistas" (subrede
  do modelo) processam aquela entrada — um comportamento diferente de uso de CPU/GPU em relação a um
  modelo puramente denso, interessante de observar nos experimentos da atividade.

## Critérios obrigatórios (Seção 5.3 da atividade)

| Critério | Verificação |
|---|---|
| Identificação | Organização IBM, nome completo e URL do model card confirmados acima |
| Parâmetros | 3B totais / ~800M ativos — dentro do limite de 10B da atividade |
| Formato e quantização | GGUF, compatível com Ollama (`ollama pull granite3.1-moe:3b`) |
| Licença | Apache 2.0 — uso e redistribuição permitidos |
| Execução local | Compatível com Ollama e com a camada de aplicação Open WebUI (Trilha A) |

## Justificativa curta da escolha (até 100 palavras)

> O Granite-3.1-3B-A800M-Instruct foi escolhido, com autorização do professor para a troca de modelo,
> por ser uma arquitetura Mixture of Experts (MoE): embora possua 3B de parâmetros totais, ativa apenas
> ~800M por token, favorecendo respostas rápidas com uso eficiente de CPU/GPU. Sua licença Apache 2.0 é
> totalmente permissiva, e o contexto de 128K tokens é equivalente ao de modelos maiores. A escolha
> também permite comparar, na prática, o comportamento de um modelo MoE com o de um modelo denso já
> testado anteriormente (Phi-4-mini), enriquecendo a análise de processos, threads e uso de recursos
> pedida pela atividade.

---
*Ajuste a quantização na primeira linha da tabela caso sua equipe utilize uma variante diferente de
Q4_K_M, e confirme o nome exato da tag no Ollama com `ollama pull granite3.1-moe:3b` antes do registro
final no Google Classroom.*
