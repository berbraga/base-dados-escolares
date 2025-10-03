
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

logger = logging.getLogger(__name__)

class PowerPointReporter:
    
    def __init__(self, data: pd.DataFrame, results: Dict[str, Any]):
        
        self.vasco_data = data
        self.results = results
        self.prs = Presentation()
        
    def create_presentation(self) -> Presentation:
        
        logger.info("Criando apresentação PowerPoint")
        
        self._add_title_slide()
        
        self._add_objectives_slide()
        
        self._add_methodology_slide()
        
        self._add_data_overview_slide()
        
        self._add_hypothesis_slides()
        
        self._add_results_summary_slide()
        
        self._add_conclusions_slide()
        
        return self.prs
    
    def _add_title_slide(self):
        
        slide_layout = self.prs.slide_layouts[0]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        
        title.text = "Análise de Equidade Educacional"
        subtitle.text = "Investigação das Causas do Desempenho Diferenciado de Alunos Minoritários no SAEB\n\nAnálise Estatística de 4 Hipóteses Principais"
        
        title.text_frame.paragraphs[0].font.size = Pt(44)
        title.text_frame.paragraphs[0].font.bold = True
        title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)
        
        subtitle.text_frame.paragraphs[0].font.size = Pt(20)
        subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(64, 64, 64)
    
    def _add_objectives_slide(self):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "Objetivos da Análise"
        
        objectives_text = 
        
        content.text = objectives_text
        self._format_content_text(content)
    
    def _add_methodology_slide(self):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "Metodologia"
        
        methodology_text = .format(len(self.data))
        
        content.text = methodology_text
        self._format_content_text(content)
    
    def _add_data_overview_slide(self):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "Visão Geral dos Dados"
        
        total_students = len(self.data)
        total_schools = self.data['CODIGO_ESCOLA'].nunique() if 'CODIGO_ESCOLA' in self.data.columns else 'N/A'
        minority_pct = self.data['MINORIA'].mean() * 100
        avg_math_score = self.data['NOTA_MATEMATICA'].mean()
        avg_port_score = self.data['NOTA_PORTUGUES'].mean()
        
        overview_text = f
        
        content.text = overview_text
        self._format_content_text(content)
    
    def _add_hypothesis_slides(self):
        
        hypothesis_descriptions = {
            'hypothesis_1': {
                'title': 'Hipótese 1: Segregação Socioespacial',
                'description': 'Alunos minoritários concentrados em escolas com menor infraestrutura'
            },
            'hypothesis_2': {
                'title': 'Hipótese 2: Qualidade Docente',
                'description': 'Professores menos qualificados em escolas com maior concentração de minorias'
            },
            'hypothesis_3': {
                'title': 'Hipótese 3: Capital Cultural',
                'description': 'Diferenças no ambiente familiar e recursos educacionais domésticos'
            },
            'hypothesis_4': {
                'title': 'Hipótese 4: Efeito de Pares',
                'description': 'Impacto negativo da composição socioeconômica da turma'
            }
        }
        
        for key, info in hypothesis_descriptions.items():
            if key in self.results:
                self._add_single_hypothesis_slide(info['title'], info['description'], self.results[key])
    
    def _add_single_hypothesis_slide(self, title: str, description: str, results: Dict[str, Any]):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        slide_title = slide.shapes.title
        content = slide.placeholders[1]
        
        slide_title.text = title
        
        slide_text = f"{description}\n\n"
        
        significant_tests = []
        non_significant_tests = []
        
        for test_name, test_result in results['tests'].items():
            if isinstance(test_result, dict) and 'significant' in test_result:
                if test_result['significant']:
                    significant_tests.append(f"• {test_name}: SIGNIFICATIVO (p = {test_result['p_value']:.4f})")
                else:
                    non_significant_tests.append(f"• {test_name}: Não significativo (p = {test_result['p_value']:.4f})")
        
        if significant_tests:
            slide_text += "Resultados Significativos:\n" + "\n".join(significant_tests) + "\n\n"
        
        if non_significant_tests:
            slide_text += "Resultados Não Significativos:\n" + "\n".join(non_significant_tests) + "\n\n"
        
        if 'summary_stats' in results:
            slide_text += "Estatísticas Resumidas:\n"
            for stat_name, stat_value in results['summary_stats'].items():
                if isinstance(stat_value, float):
                    slide_text += f"• {stat_name}: {stat_value:.2f}\n"
                else:
                    slide_text += f"• {stat_name}: {stat_value}\n"
        
        content.text = slide_text
        self._format_content_text(content)
    
    def _add_results_summary_slide(self):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "Resumo dos Resultados"
        
        confirmed_hypotheses = []
        rejected_hypotheses = []
        
        for key, result in self.results.items():
            has_significant_vasco_result = False
            
            for test_name, test_result in result['tests'].items():
                if isinstance(test_result, dict) and test_result.get('significant', False):
                    has_significant_vasco_result = True
                    break
            
            if has_significant_result:
                confirmed_hypotheses.append(result['hypothesis'])
            else:
                rejected_hypotheses.append(result['hypothesis'])
        
        summary_text = f
        
        for hypothesis in confirmed_hypotheses:
            summary_text += f"• {hypothesis}\n"
        
        summary_text += f"\nHipóteses Rejeitadas ({len(rejected_hypotheses)}):\n"
        
        for hypothesis in rejected_hypotheses:
            summary_text += f"• {hypothesis}\n"
        
        summary_text += f
        
        content.text = summary_text
        self._format_content_text(content)
    
    def _add_conclusions_slide(self):
        
        slide_layout = self.prs.slide_layouts[1]
        slide = self.prs.slides.add_slide(slide_layout)
        
        title = slide.shapes.title
        content = slide.placeholders[1]
        
        title.text = "Conclusões e Recomendações"
        
        conclusions_text = 
        
        content.text = conclusions_text
        self._format_content_text(content)
    
    def _format_content_text(self, content):
        
        for paragraph in content.text_frame.paragraphs:
            paragraph.font.size = Pt(18)
            paragraph.font.color.rgb = RGBColor(64, 64, 64)
            paragraph.alignment = PP_ALIGN.LEFT
    
    def save_presentation(self, output_path: str) -> None:
        
        self.prs.save(output_path)
        logger.info(f"Apresentação salva em {output_path}")
    
    def create_detailed_report(self) -> str:
        
        report = "RELATÓRIO DETALHADO - ANÁLISE DE EQUIDADE EDUCACIONAL\n"
        report += "=" * 60 + "\n\n"
        
        report += "RESUMO EXECUTIVO\n"
        report += "-" * 20 + "\n"
        report += f"Este relatório apresenta uma análise estatística abrangente dos fatores que influenciam\n"
        report += f"o desempenho educacional de alunos minoritários no Sistema de Avaliação da Educação Básica (SAEB).\n"
        report += f"A análise baseia-se em uma amostra de {len(self.data):,} alunos e testa 4 hipóteses principais\n"
        report += f"sobre as causas das desigualdades educacionais.\n\n"
        
        report += "METODOLOGIA\n"
        report += "-" * 15 + "\n"
        report += "• Dados: Sistema de Avaliação da Educação Básica (SAEB)\n"
        report += "• Métodos: Testes t, correlação de Pearson, regressão linear múltipla\n"
        report += "• Software: Python (pandas, scipy, scikit-learn)\n"
        report += "• Nível de significância: α = 0.05\n\n"
        
        report += "RESULTADOS POR HIPÓTESE\n"
        report += "-" * 25 + "\n\n"
        
        for key, result in self.results.items():
            report += f"{result['hypothesis'].upper()}\n"
            report += f"Descrição: {result['description']}\n"
            report += "-" * 30 + "\n"
            
            for test_name, test_result in result['tests'].items():
                if isinstance(test_result, dict) and 'significant' in test_result:
                    significance = "SIGNIFICATIVO" if test_result['significant'] else "NÃO SIGNIFICATIVO"
                    report += f"{test_name}: {significance} (p = {test_result['p_value']:.4f})\n"
                    if 'effect_size' in test_result:
                        report += f"  Tamanho do efeito: {test_result['effect_size']:.4f}\n"
                elif isinstance(test_result, (int, float)):
                    report += f"{test_name}: {test_result:.4f}\n"
            
            report += "\n"
        
        report += "CONCLUSÕES\n"
        report += "-" * 12 + "\n"
        
        confirmed_count = sum(1 for result in self.results.values() 
                            if any(test.get('significant', False) 
                                 for test in result['tests'].values() 
                                 if isinstance(test, dict)))
        
        report += f"• {confirmed_count} de {len(self.results)} hipóteses foram confirmadas estatisticamente\n"
        report += "• Evidências de desigualdades estruturais no sistema educacional\n"
        report += "• Necessidade de políticas mais efetivas para garantir equidade\n"
        report += "• Importância de monitoramento contínuo de indicadores de equidade\n\n"
        
        report += "RECOMENDAÇÕES\n"
        report += "-" * 15 + "\n"
        report += "• Investimento em infraestrutura de escolas com maior concentração de minorias\n"
        report += "• Programas de capacitação docente específicos\n"
        report += "• Políticas de redistribuição de recursos educacionais\n"
        report += "• Implementação de políticas de ação afirmativa mais robustas\n"
        report += "• Monitoramento contínuo de indicadores de equidade\n"
        
        return report

if __name__ == "__main__":

    from data_processing.data_processor import create_sample_data
    from analysis.hypothesis_tester import HypothesisTester
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

    
    
    reporter = PowerPointReporter(sample_data, results)
    presentation = reporter.create_presentation()
    
    reporter.save_presentation("relatorio_equidade_educacional.pptx")
    
    detailed_report = reporter.create_detailed_report()
    print(detailed_report)
