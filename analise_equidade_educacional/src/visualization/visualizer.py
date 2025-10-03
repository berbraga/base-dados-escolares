
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class Visualizer:
    
    def __init__(self, data: pd.DataFrame, results: Dict[str, Any]):
        
        self.vasco_data = data
        self.results = results
        self.figures = {}
        
    def create_overview_dashboard(self) -> go.Figure:
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribuição das Notas', 'Percentual de Minorias por Escola',
                          'Correlação NSE vs Notas', 'Infraestrutura vs Desempenho'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Histogram(x=self.data['NOTA_MATEMATICA'], name='Matemática', opacity=0.7),
            row=1, col=1
        )
        fig.add_trace(
            go.Histogram(x=self.data['NOTA_PORTUGUES'], name='Português', opacity=0.7),
            row=1, col=1
        )
        
        school_minority = self.data.groupby('CODIGO_ESCOLA')['MINORIA'].mean().reset_index()
        fig.add_trace(
            go.Bar(x=school_minority['CODIGO_ESCOLA'], y=school_minority['MINORIA'] * 100,
                   name='% Minorias'),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=self.data['NSE'], y=self.data['NOTA_MATEMATICA'],
                      mode='markers', name='Matemática', opacity=0.6),
            row=2, col=1
        )
        
        school_vasco_stats = self.data.groupby('CODIGO_ESCOLA').agg({
            'INFRA_BOA': 'mean',
            'NOTA_MATEMATICA': 'mean'
        }).reset_index()
        
        fig.add_trace(
            go.Scatter(x=school_stats['INFRA_BOA'], y=school_stats['NOTA_MATEMATICA'],
                      mode='markers', name='Escolas'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Dashboard de Análise de Equidade Educacional",
            showlegend=True,
            height=800
        )
        
        self.figures['overview_dashboard'] = fig
        return fig
    
    def create_hypothesis_visualizations(self) -> Dict[str, go.Figure]:
        
        visualizations = {}
        
        visualizations['hypothesis_1'] = self._create_segregation_plot()
        
        visualizations['hypothesis_2'] = self._create_teacher_quality_plot()
        
        visualizations['hypothesis_3'] = self._create_cultural_capital_plot()
        
        visualizations['hypothesis_4'] = self._create_peer_effect_plot()
        
        self.figures.update(visualizations)
        return visualizations
    
    def _create_segregation_plot(self) -> go.Figure:
        
        school_vasco_stats = self.data.groupby('CODIGO_ESCOLA').agg({
            'MINORIA': 'mean',
            'INFRA_BOA': 'mean',
            'NOTA_MATEMATICA': 'mean',
            'NOTA_PORTUGUES': 'mean'
        }).reset_index()
        
        median_minority = school_stats['MINORIA'].median()
        high_minority = school_stats[school_stats['MINORIA'] >= median_minority]
        low_minority = school_stats[school_stats['MINORIA'] < median_minority]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Infraestrutura por Concentração de Minorias',
                          'Desempenho por Concentração de Minorias')
        )
        
        fig.add_trace(
            go.Bar(x=['Baixa Concentração', 'Alta Concentração'],
                   y=[low_minority['INFRA_BOA'].mean(), high_minority['INFRA_BOA'].mean()],
                   name='Infraestrutura Boa (%)', marker_color=['lightblue', 'lightcoral']),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=['Baixa Concentração', 'Alta Concentração'],
                   y=[low_minority['NOTA_MATEMATICA'].mean(), high_minority['NOTA_MATEMATICA'].mean()],
                   name='Nota Matemática', marker_color=['lightgreen', 'lightcoral']),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Hipótese 1: Segregação Socioespacial",
            showlegend=True
        )
        
        return fig
    
    def _create_teacher_quality_plot(self) -> go.Figure:
        
        school_vasco_stats = self.data.groupby('CODIGO_ESCOLA').agg({
            'MINORIA': 'mean',
            'DOCENTE_QUALIFICADO': 'mean',
            'NOTA_MATEMATICA': 'mean',
            'NOTA_PORTUGUES': 'mean'
        }).reset_index()
        
        median_minority = school_stats['MINORIA'].median()
        high_minority = school_stats[school_stats['MINORIA'] >= median_minority]
        low_minority = school_stats[school_stats['MINORIA'] < median_minority]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Qualificação Docente por Concentração de Minorias',
                          'Impacto da Qualificação no Desempenho')
        )
        
        fig.add_trace(
            go.Bar(x=['Baixa Concentração', 'Alta Concentração'],
                   y=[low_minority['DOCENTE_QUALIFICADO'].mean(), 
                      high_minority['DOCENTE_QUALIFICADO'].mean()],
                   name='Docentes Qualificados (%)', marker_color=['lightblue', 'lightcoral']),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=school_stats['DOCENTE_QUALIFICADO'],
                      y=school_stats['NOTA_MATEMATICA'],
                      mode='markers',
                      name='Escolas',
                      text=school_stats['MINORIA'],
                      hovertemplate='Qualificação: %{x}<br>Nota: %{y}<br>% Minorias: %{text}<extra></extra>'),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Hipótese 2: Qualidade Docente",
            showlegend=True
        )
        
        return fig
    
    def _create_cultural_capital_plot(self) -> go.Figure:
        
        minority_students = self.data[self.data['MINORIA']]
        non_minority_students = self.data[~self.data['MINORIA']]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Capital Cultural por Grupo',
                          'Correlação Capital Cultural vs Desempenho')
        )
        
        fig.add_trace(
            go.Box(y=minority_students['CAPITAL_CULTURAL'], name='Minorias'),
            row=1, col=1
        )
        fig.add_trace(
            go.Box(y=non_minority_students['CAPITAL_CULTURAL'], name='Não Minorias'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=self.data['CAPITAL_CULTURAL'],
                      y=self.data['NOTA_MATEMATICA'],
                      mode='markers',
                      name='Alunos',
                      marker=dict(color=self.data['MINORIA'], colorscale='RdYlBu'),
                      hovertemplate='Capital Cultural: %{x}<br>Nota: %{y}<extra></extra>'),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Hipótese 3: Capital Cultural",
            showlegend=True
        )
        
        return fig
    
    def _create_peer_effect_plot(self) -> go.Figure:
        
        school_minority_pct = self.data.groupby('CODIGO_ESCOLA')['MINORIA'].mean().reset_index()
        self.vasco_data = self.data.merge(school_minority_pct, on='CODIGO_ESCOLA', suffixes=('', '_ESCOLA'))
        
        quartiles = self.data['MINORIA_ESCOLA'].quantile([0.25, 0.5, 0.75])
        
        q1_students = self.data[self.data['MINORIA_ESCOLA'] <= quartiles[0.25]]
        q2_students = self.data[(self.data['MINORIA_ESCOLA'] > quartiles[0.25]) & 
                               (self.data['MINORIA_ESCOLA'] <= quartiles[0.5])]
        q3_students = self.data[(self.data['MINORIA_ESCOLA'] > quartiles[0.5]) & 
                               (self.data['MINORIA_ESCOLA'] <= quartiles[0.75])]
        q4_students = self.data[self.data['MINORIA_ESCOLA'] > quartiles[0.75]]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Desempenho por Quartil de Concentração de Minorias',
                          'Correlação Concentração vs Desempenho')
        )
        
        quartil_names = ['Q1 (Baixa)', 'Q2', 'Q3', 'Q4 (Alta)']
        quartil_vasco_data = [q1_students['NOTA_MATEMATICA'], q2_students['NOTA_MATEMATICA'],
                       q3_students['NOTA_MATEMATICA'], q4_students['NOTA_MATEMATICA']]
        
        for i, (name, data) in enumerate(zip(quartil_names, quartil_data)):
            fig.add_trace(
                go.Box(y=data, name=name),
                row=1, col=1
            )
        
        fig.add_trace(
            go.Scatter(x=self.data['MINORIA_ESCOLA'],
                      y=self.data['NOTA_MATEMATICA'],
                      mode='markers',
                      name='Alunos',
                      opacity=0.6,
                      hovertemplate='% Minorias Escola: %{x}<br>Nota: %{y}<extra></extra>'),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Hipótese 4: Efeito de Pares",
            showlegend=True
        )
        
        return fig
    
    def create_statistical_summary_plot(self) -> go.Figure:
        
        hypotheses = []
        p_values = []
        effect_sizes = []
        
        for key, result in self.results.items():
            hypotheses.append(result['hypothesis'])
            
            min_p_value = 1.0
            max_effect_size = 0.0
            
            for test_name, test_result in result['tests'].items():
                if isinstance(test_result, dict) and 'p_value' in test_result:
                    min_p_value = min(min_p_value, test_result['p_value'])
                    if 'effect_size' in test_result:
                        max_effect_size = max(max_effect_size, abs(test_result['effect_size']))
            
            p_values.append(min_p_value)
            effect_sizes.append(max_effect_size)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Significância Estatística (p-values)', 'Tamanho do Efeito')
        )
        
        colors = ['red' if p < 0.05 else 'green' for p in p_values]
        fig.add_trace(
            go.Bar(x=hypotheses, y=p_values, marker_color=colors, name='p-value'),
            row=1, col=1
        )
        fig.add_hline(y=0.05, line_dash="dash", line_color="red", row=1, col=1)
        
        fig.add_trace(
            go.Bar(x=hypotheses, y=effect_sizes, name='Tamanho do Efeito'),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Resumo dos Resultados Estatísticos",
            showlegend=True,
            height=500
        )
        
        return fig
    
    def save_all_figures(self, output_dir: str) -> None:
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, fig in self.figures.items():
            fig.write_html(f"{output_dir}/{name}.html")

        logger.info(f"Figuras salvas em {output_dir}")
    
    def create_matplotlib_figures(self) -> Dict[str, plt.Figure]:
        
        matplotlib_figs = {}
        
        fig1, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        minority_students = self.data[self.data['MINORIA']]
        non_minority_students = self.data[~self.data['MINORIA']]
        
        axes[0].hist([minority_students['NOTA_MATEMATICA'], non_minority_students['NOTA_MATEMATICA']],
                    bins=30, alpha=0.7, label=['Minorias', 'Não Minorias'])
        axes[0].set_title('Distribuição das Notas de Matemática')
        axes[0].set_xlabel('Nota')
        axes[0].set_ylabel('Frequência')
        axes[0].legend()
        
        axes[1].hist([minority_students['NOTA_PORTUGUES'], non_minority_students['NOTA_PORTUGUES']],
                    bins=30, alpha=0.7, label=['Minorias', 'Não Minorias'])
        axes[1].set_title('Distribuição das Notas de Português')
        axes[1].set_xlabel('Nota')
        axes[1].set_ylabel('Frequência')
        axes[1].legend()
        
        plt.tight_layout()
        matplotlib_figs['score_distribution'] = fig1
        
        fig2, ax = plt.subplots(figsize=(10, 8))
        
        correlation_vasco_data = self.data[['NOTA_MATEMATICA', 'NOTA_PORTUGUES', 'NSE', 
                                    'CAPITAL_CULTURAL', 'INFRA_BOA', 'DOCENTE_QUALIFICADO']].corr()
        
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Matriz de Correlação')
        
        matplotlib_figs['correlation_matrix'] = fig2
        
        return matplotlib_figs

if __name__ == "__main__":

    from data_processing.data_processor import create_sample_data
    from analysis.hypothesis_tester import HypothesisTester
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

    
    
    visualizer = Visualizer(sample_data, results)
    
    dashboard = visualizer.create_overview_dashboard()
    dashboard.show()
    
    hypothesis_viz = visualizer.create_hypothesis_visualizations()
    
    summary_plot = visualizer.create_statistical_summary_plot()
    summary_plot.show()
