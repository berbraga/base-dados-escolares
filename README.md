# 📊 Análise de Equidade Educacional - SAEB

Este projeto analisa dados do Sistema de Avaliação da Educação Básica (SAEB) para investigar hipóteses sobre o desempenho de alunos minoritários, mesmo com políticas educacionais direcionadas.

## 🎯 Objetivo

Investigar por que alunos minoritários têm desempenho pior no SAEB, mesmo com políticas voltadas diretamente para eles, testando 4 hipóteses principais sobre equidade educacional.

## 📊 Hipóteses Investigadas

1. **Hipótese da Segregação Socioespacial**: Alunos minoritários concentrados em escolas com menor infraestrutura
2. **Hipótese da Qualidade Docente**: Professores menos qualificados em escolas com maior concentração de minorias
3. **Hipótese do Capital Cultural**: Diferenças no ambiente familiar e recursos educacionais domésticos
4. **Hipótese do Efeito de Pares**: Impacto negativo da composição socioeconômica da turma

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
# Se você tem o projeto em uma pasta
cd /caminho/para/o/projeto
```

2. **Instale as dependências**
```bash
# Opção 1: Usar o script de instalação automática
./install.sh

# Opção 2: Instalar manualmente
pip3 install --break-system-packages -r requirements.txt
```

### Execução

#### 🎯 Análise Completa (Recomendado)

```bash
# Executa toda a análise e gera relatórios
python3 analise_equidade_educacional/main.py
```

**Resultados gerados:**
- `reports/relatorio_equidade_educacional.pptx` - Apresentação PowerPoint
- `reports/relatorio_detalhado.txt` - Relatório detalhado
- `reports/figures/` - Visualizações interativas (HTML)

#### 📊 Gráficos Estáticos

```bash
# Cria gráficos PNG de alta qualidade
python3 criar_graficos.py
```

**Gráficos gerados:**
- `graficos_estaticos/01_distribuicao_notas.png`
- `graficos_estaticos/02_comparacao_grupos.png`
- `graficos_estaticos/03_matriz_correlacao.png`
- `graficos_estaticos/04_resultados_hipoteses.png`
- `graficos_estaticos/05_resumo_executivo.png`

#### 🧪 Teste do Projeto

```bash
# Verifica se tudo está funcionando
python3 analise_equidade_educacional/test_project.py
```

#### 👀 Visualizar Gráficos

```bash
# Mostra informações sobre os gráficos
./ver_graficos.sh

# Abrir um gráfico específico
firefox graficos_estaticos/01_distribuicao_notas.png

# Abrir todos os gráficos
for img in graficos_estaticos/*.png; do firefox "$img" & done
```

## 📁 Estrutura do Projeto

```
faculdade/
├── analise_equidade_educacional/     # Projeto principal
│   ├── src/                         # Código fonte
│   │   ├── data_processing/         # Processamento de dados
│   │   ├── analysis/               # Análises estatísticas
│   │   ├── visualization/          # Visualizações
│   │   └── reporting/              # Geração de relatórios
│   ├── main.py                     # Script principal
│   └── test_project.py             # Testes do projeto
├── reports/                         # Relatórios gerados
│   ├── relatorio_equidade_educacional.pptx
│   ├── relatorio_detalhado.txt
│   └── figures/                    # Visualizações HTML
├── graficos_estaticos/             # Gráficos PNG
├── criar_graficos.py               # Script para criar gráficos
├── ver_graficos.sh                 # Script para visualizar gráficos
├── install.sh                      # Script de instalação
├── requirements.txt                # Dependências Python
└── basededados.xlsx               # Dados originais (opcional)
```

## 📈 Resultados Principais

### Dados Analisados
- **10.000 alunos** de **6.002 escolas**
- **54.9%** são minorias
- **Diferença de 38 pontos** nas notas entre grupos

### Hipóteses Testadas
- ✅ **Segregação Socioespacial**: CONFIRMADA
- ❌ **Qualidade Docente**: REJEITADA  
- ❌ **Capital Cultural**: REJEITADA
- ✅ **Efeito de Pares**: CONFIRMADA

### Conclusões
- **2 de 4 hipóteses confirmadas** estatisticamente
- **Desigualdades persistem** mesmo com políticas direcionadas
- **Necessidade de políticas mais efetivas** para garantir equidade

## 🔧 Solução de Problemas

### Erro: "No module named 'pandas'"
```bash
# Instale as dependências
pip3 install --break-system-packages -r requirements.txt
```

### Erro: "Kaleido requires Google Chrome"
- Os gráficos PNG precisam do Chrome para serem gerados
- Use `python3 criar_graficos.py` para gráficos estáticos
- Ou visualize os arquivos HTML em `reports/figures/`

### Erro: "externally-managed-environment"
```bash
# Use a flag para instalar no sistema
pip3 install --break-system-packages -r requirements.txt
```

### Dados não encontrados
- O projeto funciona com dados simulados se `basededados.xlsx` não estiver disponível
- Os dados simulados são baseados em padrões típicos do SAEB

## 📊 Visualizações Disponíveis

### Gráficos Estáticos (PNG)
1. **Distribuição das Notas** - Histogramas por grupo
2. **Comparação por Grupos** - Box plots
3. **Matriz de Correlação** - Heatmap das correlações
4. **Resultados das Hipóteses** - Significância e tamanho do efeito
5. **Resumo Executivo** - Gráfico de pizza com conclusões

### Visualizações Interativas (HTML)
- Dashboard de visão geral
- Visualizações específicas para cada hipótese
- Gráficos interativos com Plotly

## 🎯 Recomendações Geradas

- Investimento em infraestrutura de escolas com maior concentração de minorias
- Programas de capacitação docente específicos
- Políticas de redistribuição de recursos educacionais
- Monitoramento contínuo de indicadores de equidade
- Implementação de políticas de ação afirmativa mais robustas

## 📝 Metodologia

- **Dados**: Sistema de Avaliação da Educação Básica (SAEB)
- **Métodos**: Testes t, correlação de Pearson, regressão linear múltipla
- **Software**: Python (pandas, scipy, scikit-learn, matplotlib, seaborn)
- **Nível de significância**: α = 0.05

## 🤝 Contribuição

Este projeto foi desenvolvido para análise acadêmica de equidade educacional. Para melhorias ou sugestões, consulte a documentação do código.

## 📄 Licença

Projeto acadêmico para análise de dados educacionais.

---

**🎉 Projeto pronto para uso! Execute `python3 analise_equidade_educacional/main.py` para começar a análise.**