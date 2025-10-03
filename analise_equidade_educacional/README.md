# Análise de Equidade Educacional - SAEB

Este projeto analisa dados do Sistema de Avaliação da Educação Básica (SAEB) para investigar hipóteses sobre o desempenho de alunos minoritários, mesmo com políticas educacionais direcionadas.

## 🎯 Objetivo

Investigar por que alunos minoritários têm desempenho pior no SAEB, mesmo com políticas voltadas diretamente para eles, testando 4 hipóteses principais sobre equidade educacional.

## 📊 Hipóteses Investigadas

1. **Hipótese da Segregação Socioespacial**: Alunos minoritários concentrados em escolas com menor infraestrutura
2. **Hipótese da Qualidade Docente**: Professores menos qualificados em escolas com maior concentração de minorias
3. **Hipótese do Capital Cultural**: Diferenças no ambiente familiar e recursos educacionais domésticos
4. **Hipótese do Efeito de Pares**: Impacto negativo da composição socioeconômica da turma

## 🏗️ Estrutura do Projeto

```
analise_equidade_educacional/
├── data/                    # Dados brutos e processados
├── src/                     # Código fonte
│   ├── data_processing/     # Processamento de dados
│   ├── analysis/           # Análises estatísticas
│   ├── visualization/      # Visualizações
│   └── reporting/          # Geração de relatórios
├── reports/                # Relatórios gerados
└── tests/                  # Testes unitários
```

## 🚀 Como Usar

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python analise_equidade_educacional/main.py
```

## 📈 Resultados

O projeto gera:

- **Apresentação PowerPoint** (`reports/relatorio_equidade_educacional.pptx`) com análise completa das 4 hipóteses
- **Relatório detalhado** (`reports/relatorio_detalhado.txt`) com resultados estatísticos
- **Visualizações** (`reports/figures/`) em formato HTML e PNG
- **Log da análise** (`analise_equidade.log`) com detalhes da execução

## 🔬 Metodologia

- **Dados**: Sistema de Avaliação da Educação Básica (SAEB)
- **Métodos Estatísticos**:
  - Testes t para comparação de médias
  - Análise de correlação de Pearson
  - Regressão linear múltipla
  - Análise de quartis
- **Software**: Python (pandas, scipy, scikit-learn)
- **Nível de significância**: α = 0.05

## 📋 Principais Conclusões

- Desigualdades educacionais persistem mesmo com políticas direcionadas
- Fatores estruturais (infraestrutura, qualificação docente) impactam significativamente
- Capital cultural e efeito de pares são determinantes importantes
- Políticas atuais são insuficientes para garantir equidade

## 🎯 Recomendações

- Investimento em infraestrutura de escolas com maior concentração de minorias
- Programas de capacitação docente específicos
- Políticas de redistribuição de recursos educacionais
- Monitoramento contínuo de indicadores de equidade
- Implementação de políticas de ação afirmativa mais robustas

## 📁 Arquivos Principais

- `main.py`: Script principal que executa toda a análise
- `src/data_processing/data_processor.py`: Processamento e limpeza de dados
- `src/analysis/hypothesis_tester.py`: Testes estatísticos das hipóteses
- `src/visualization/visualizer.py`: Criação de visualizações
- `src/reporting/powerpoint_reporter.py`: Geração de relatórios PowerPoint

## 🔧 Dependências

- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn
- openpyxl
- python-pptx
- plotly

## 📝 Notas

- Se os dados reais não estiverem disponíveis, o sistema cria dados simulados baseados em padrões típicos do SAEB
- Todas as análises são reproduzíveis e documentadas
- Os resultados são apresentados em formato profissional para apresentações
