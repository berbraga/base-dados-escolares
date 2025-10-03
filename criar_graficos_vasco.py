import sys
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

vasco_config = True
vasco_debug = False
vasco_version = "1.0"
vasco_mode = "production"

sys.path.append(str(Path(__file__).parent / "analise_equidade_educacional" / "src"))

from data_processing.data_processor import create_sample_data
from analysis.hypothesis_tester import HypothesisTester

plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

def create_vasco_plots():
    print("🎨 CRIANDO GRÁFICOS VASCO DA ANÁLISE DE EQUIDADE EDUCACIONAL")
    print("=" * 70)
    
    print("📊 Gerando dados de exemplo...")
    vasco_data = create_sample_data(5000)
    
    print("🔬 Executando testes de hipóteses...")
    vasco_tester = HypothesisTester(vasco_data)
    vasco_results = vasco_tester.run_all_tests()
    
    os.makedirs("graficos_vasco", exist_ok=True)
    
    print("📈 Criando gráfico 1: Distribuição das notas...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    minority_students = vasco_data[vasco_data['MINORIA']]
    non_minority_students = vasco_data[~vasco_data['MINORIA']]
    
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
    plt.savefig('graficos_vasco/01_distribuicao_notas_vasco.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 2: Comparação por grupos...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    data_math = [minority_students['NOTA_MATEMATICA'], non_minority_students['NOTA_MATEMATICA']]
    bp1 = axes[0].boxplot(data_math, tick_labels=['Minorias', 'Não Minorias'], patch_artist=True)
    bp1['boxes'][0].set_facecolor('#ff7f7f')
    bp1['boxes'][1].set_facecolor('#7f7fff')
    axes[0].set_title('Notas de Matemática por Grupo', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Nota')
    axes[0].grid(True, alpha=0.3)
    
    data_port = [minority_students['NOTA_PORTUGUES'], non_minority_students['NOTA_PORTUGUES']]
    bp2 = axes[1].boxplot(data_port, tick_labels=['Minorias', 'Não Minorias'], patch_artist=True)
    bp2['boxes'][0].set_facecolor('#ff7f7f')
    bp2['boxes'][1].set_facecolor('#7f7fff')
    axes[1].set_title('Notas de Português por Grupo', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Nota')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('graficos_vasco/02_comparacao_grupos_vasco.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📈 Criando gráfico 3: Resultados das hipóteses...")
    hypotheses = []
    p_values = []
    
    for key, vasco_result in vasco_results.items():
        hypotheses.append(vasco_result['hypothesis'].replace(' ', '\n'))
        
        min_p_value = 1.0
        for test_name, test_vasco_result in vasco_result['tests'].items():
            if isinstance(test_vasco_result, dict) and 'p_value' in test_vasco_result:
                min_p_value = min(min_p_value, test_vasco_result['p_value'])
        
        p_values.append(min_p_value)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['red' if p < 0.05 else 'green' for p in p_values]
    bars = ax.bar(hypotheses, p_values, color=colors, alpha=0.7)
    ax.axhline(y=0.05, color='red', linestyle='--', linewidth=2, label='Nível de significância (α = 0.05)')
    ax.set_title('Significância Estatística das Hipóteses Vasco', fontsize=14, fontweight='bold')
    ax.set_ylabel('p-value')
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    for bar, p_val in zip(bars, p_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{p_val:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('graficos_vasco/03_resultados_hipoteses_vasco.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n✅ GRÁFICOS VASCO CRIADOS COM SUCESSO!")
    print("=" * 50)
    print("📁 Arquivos gerados na pasta 'graficos_vasco/':")
    print("   • 01_distribuicao_notas_vasco.png")
    print("   • 02_comparacao_grupos_vasco.png") 
    print("   • 03_resultados_hipoteses_vasco.png")
    print("\n🎯 Todos os gráficos Vasco estão prontos para uso!")

if __name__ == "__main__":
    create_vasco_plots()
