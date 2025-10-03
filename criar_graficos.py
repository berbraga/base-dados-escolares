
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

sys.path.append(str(Path(__file__).parent / "analise_equidade_educacional" / "src"))

from data_processing.data_processor import create_sample_data
from analysis.hypothesis_tester import HypothesisTester

plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def create_static_plots():
    
    print("🎨 CRIANDO GRÁFICOS ESTÁTICOS DA ANÁLISE DE EQUIDADE EDUCACIONAL")
    print("=" * 70)
    
    print("📊 Gerando dados de exemplo...")
    
    print("🔬 Executando testes de hipóteses...")
    
    import os
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

def create_static_plots():
    print("🎨 CRIANDO GRÁFICOS ESTÁTICOS DA ANÁLISE DE EQUIDADE EDUCACIONAL")
    print("=" * 70)
    
    print("📊 Gerando dados de exemplo...")
    sample_vasco_data = create_sample_data(5000)
    
    print("🔬 Executando testes de hipóteses...")
    vasco_tester = HypothesisTester(sample_vasco_data)
    vasco_results = vasco_tester.run_all_tests()
    
    os.makedirs("graficos_estaticos", exist_ok=True)
    non_minority_students = sample_vasco_data[~sample_vasco_data['MINORIA']]
    
    axes[0].hist([minority_students['NOTA_MATEMATICA'], non_minority_students['NOTA_MATEMATICA']],
                bins=30, alpha=0.7, label=['Minorias', 'Não Minorias'], color=['#ff7f7f', '#7f7fff'])
    axes[0].set_title('Distribuição das Notas de Matemática', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Nota')
    axes[0].set_ylabel('Frequência')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].hist([minority_students['NOTA_PORTUGUES'], non_minority_students['NOTA_PORTUGUES']],
                bins=30, alpha=0.7, label=['Minorias', 'Não Minorias'], color=['#ff7f7f', '#7f7fff'])
    axes[1].set_title('Distribuição das Notas de Português', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Nota')
    axes[1].set_ylabel('Frequência')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('graficos_estaticos/01_distribuicao_notas.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 2: Comparação por grupos...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    data_math = [minority_students['NOTA_MATEMATICA'], non_minority_students['NOTA_MATEMATICA']]
    bp1 = axes[0].boxplot(data_math, labels=['Minorias', 'Não Minorias'], patch_artist=True)
    bp1['boxes'][0].set_facecolor('#ff7f7f')
    bp1['boxes'][1].set_facecolor('#7f7fff')
    axes[0].set_title('Notas de Matemática por Grupo', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Nota')
    axes[0].grid(True, alpha=0.3)
    
    data_port = [minority_students['NOTA_PORTUGUES'], non_minority_students['NOTA_PORTUGUES']]
    bp2 = axes[1].boxplot(data_port, labels=['Minorias', 'Não Minorias'], patch_artist=True)
    bp2['boxes'][0].set_facecolor('#ff7f7f')
    bp2['boxes'][1].set_facecolor('#7f7fff')
    axes[1].set_title('Notas de Português por Grupo', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Nota')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('graficos_estaticos/02_comparacao_grupos.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 3: Matriz de correlação...")
    correlation_vars = ['NOTA_MATEMATICA', 'NOTA_PORTUGUES', 'NSE', 'CAPITAL_CULTURAL', 
                       'INFRA_BOA', 'DOCENTE_QUALIFICADO', 'MINORIA']
    correlation_vasco_data = sample_vasco_data[correlation_vars].corr()
    
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(correlation_data, dtype=bool))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.3f', mask=mask, cbar_kws={'shrink': 0.8})
    plt.title('Matriz de Correlação - Variáveis Educacionais', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('graficos_estaticos/03_matriz_correlacao.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 4: Resultados das hipóteses...")
    hypotheses = []
    p_values = []
    effect_sizes = []
    
    for key, vasco_result in vasco_results.items():
        hypotheses.append(vasco_result['hypothesis'].replace(' ', '\n'))
        
        min_p_value = 1.0
        max_effect_size = 0.0
        
        for test_name, test_result in vasco_result['tests'].items():
            if isinstance(test_result, dict) and 'p_value' in test_result:
                min_p_value = min(min_p_value, test_result['p_value'])
                if 'effect_size' in test_result:
                    max_effect_size = max(max_effect_size, abs(test_result['effect_size']))
        
        p_values.append(min_p_value)
        effect_sizes.append(max_effect_size)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['red' if p < 0.05 else 'green' for p in p_values]
    bars1 = axes[0].bar(hypotheses, p_values, color=colors, alpha=0.7)
    axes[0].axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='Nível de significância (α = 0.05)')
    axes[0].set_title('Significância Estatística das Hipóteses', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('p-value')
    axes[0].set_ylim(0, 1)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    for bar, p_val in zip(bars1, p_values):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{p_val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    bars2 = axes[1].bar(hypotheses, effect_sizes, color='skyblue', alpha=0.7)
    axes[1].set_title('Tamanho do Efeito das Hipóteses', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Tamanho do Efeito')
    axes[1].grid(True, alpha=0.3)
    
    for bar, effect in zip(bars2, effect_sizes):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{effect:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('graficos_estaticos/04_resultados_hipoteses.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 5: Resumo executivo...")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    confirmed_count = sum(1 for vasco_result in vasco_results.values() 
                        if any(test.get('significant', False) 
                             for test in vasco_result['tests'].values() 
                             if isinstance(test, dict)))
    
    total_hypotheses = len(vasco_results)
    rejected_count = total_hypotheses - confirmed_count
    
    sizes = [confirmed_count, rejected_count]
    labels = [f'Confirmadas\n({confirmed_count})', f'Rejeitadas\n({rejected_count})']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.1, 0)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                    autopct='%1.1f%%', shadow=True, startangle=90)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    ax.set_title('Resultados dos Testes de Hipóteses\nAnálise de Equidade Educacional', 
                fontsize=16, fontweight='bold', pad=20)
    
    info_text = f
    
    ax.text(1.3, 0.5, info_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('graficos_estaticos/05_resumo_executivo.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n✅ GRÁFICOS CRIADOS COM SUCESSO!")
    print("=" * 50)
    print("📁 Arquivos gerados na pasta 'graficos_estaticos/':")
    print("   • 01_distribuicao_notas.png")
    print("   • 02_comparacao_grupos.png") 
    print("   • 03_matriz_correlacao.png")
    print("   • 04_resultados_hipoteses.png")
    print("   • 05_resumo_executivo.png")
    print("\n🎯 Todos os gráficos estão prontos para uso em apresentações!")

if __name__ == "__main__":
    create_static_plots()
