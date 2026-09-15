# **Declaração de Uso de IA Generativa**

Conforme exigido na Seção 10 da atividade AV1 (Sistemas Operacionais), esta equipe declara o uso de ferramentas de IA generativa como apoio ao longo do desenvolvimento do projeto.

## **Ferramenta e modelo utilizados**

**Claude (Anthropic)**, utilizado como assistente de apoio ao longo de toda a atividade — desde a escolha inicial do modelo até a troca de modelo, a montagem da infraestrutura, os experimentos e a redação do relatório.

## **Finalidade de cada uso**

* Apoio na escolha do modelo Hugging Face, verificando a regra de exclusividade entre equipes e sugerindo alternativas compatíveis com o limite de parâmetros e com execução local via Ollama.  
* Apoio na definição da arquitetura experimental: dois containers Ollama isolados (um com e outro sem GPU), permitindo a comparação controlada exigida na Configuração 3 da Parte C da atividade.  
* Elaboração de guias passo a passo de instalação e configuração do ambiente: WSL2, Docker Engine, NVIDIA Container Toolkit, containers Ollama e Open WebUI.  
* Geração dos scripts de benchmark (`benchmark_gpu_vs_cpu_granite.py`) e de geração de gráficos (`gerar_graficos_comparacao_granite.py`), incluindo testes com dados fictícios antes do uso com dados reais.  
* Elaboração do `docker-compose.yml` para reproduzir a infraestrutura de forma declarativa, e do script `coletar_inventario.sh` para automatizar a coleta do inventário do ambiente (Seção 6.1 da atividade).  
* Apoio na solução de problemas de instalação e execução encontrados pela equipe (ver lista abaixo).  
* Geração inicial do relatório técnico, deste README e desta declaração, a partir dos dados e evidências produzidos pela própria equipe.

## **Até cinco prompts relevantes utilizados (exemplos)**

1. “Faça o script para gerar gráficos e compare os resultados com e sem gpu”  
2. “Faça um outro script para rodar consultas em paralelo”  
3. "\[imagem do erro\] apareceu esse erro" — conflito de nome de container ao rodar `docker compose up -d` pela primeira vez, com containers já criados manualmente”  
4. "Faça um rascunho de modelo de relatório e README com os dados"

## **Síntese das sugestões aproveitadas**

\[PREENCHER: resumo do que a equipe aceitou como estava, e por quê — por exemplo, os comandos de instalação do Docker/NVIDIA Container Toolkit, a estrutura de pastas do repositório, ou a lógica dos scripts de benchmark\]

## **Sugestões corrigidas ou rejeitadas**

O script de geração de gráficos (`gerar_graficos_comparacao.py`) trazia inicialmente o nome do modelo anterior (Phi-4-mini) fixo no texto do resumo comparativo gerado. Isso foi identificado e corrigido: o script passou a usar uma constante configurável (`MODELO_LABEL`), atualizada para "Granite 3.1 3B-A800M-Instruct (MoE)" antes de ser usado com os dados reais.

## **Erros encontrados**

Não foram encontrados erros na maioria das respostas sugeridas pela IA. Só a questão reportada anteriormente da correção de nome de um modelo de LLM testado anteriormente em um script gerado.

## **Testes, documentação ou observações usadas para verificar as respostas**

* O script de gráficos foi testado com dados fictícios (gerados localmente) antes de ser usado com os dados reais dos experimentos, para confirmar que rodava sem erros.  
* Os comandos de instalação (Docker, NVIDIA Container Toolkit, Docker Compose) foram efetivamente executados no ambiente WSL2 da equipe, com evidências capturadas em prints de tela e nos arquivos de `evidencias/`.  
* O inventário do ambiente (`inventario/inventario.md`) foi coletado com comandos padrão do Linux (`uname`, `lscpu`, `free`, `nvidia-smi` etc.), permitindo conferir de forma independente as informações de hardware e software citadas no relatório.  
* Os números apresentados no relatório (tempos de resposta, tokens/s, uso de CPU/memória/VRAM) vêm diretamente dos CSVs e logs gerados pelos próprios scripts de benchmark, não de estimativas da IA.

