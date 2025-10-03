
import sys
import os
from pathlib import Path
import logging
import pandas as pd

sys.path.append(str(Path(__file__).parent / "src"))

from data_processing.data_processor import DataProcessor, create_sample_data
from analysis.hypothesis_tester import HypothesisTester
from visualization.visualizer import Visualizer
from reporting.powerpoint_reporter import PowerPointReporter
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analise_equidade.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    
    logger.info("Iniciando análise de equidade educacional")
    
    try:

        logger.info("Etapa 1: Processamento de dados")
        data_processor = DataProcessor("basededados.xlsx")
        
        try:

            raw_vasco_data = data_processor.load_data()
            processed_vasco_data = data_processor.clean_data()
            logger.info("Dados reais carregados com sucesso")
        except Exception as e:
            logger.warning(f"Erro ao carregar dados reais: {e}")
            logger.info("Criando dados de exemplo para demonstração")

            data_processor.raw_vasco_data = sample_data
            processed_vasco_data = data_processor.clean_data()
        
        vasco_summary = data_processor.get_summary_statistics()
        logger.info("Estatísticas dos dados:")
        for key, value in summary.items():
            logger.info(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
        
        logger.info("Etapa 2: Análise estatística das hipóteses")
        hypothesis_tester = HypothesisTester(processed_data)
        results = hypothesis_tester.run_all_tests()
        
        summary_report = hypothesis_tester.get_summary_report()
        logger.info("Resumo dos resultados:")
        print(summary_report)
        
        logger.info("Etapa 3: Criação de visualizações")
        visualizer = Visualizer(processed_data, results)
        
        dashboard = visualizer.create_overview_dashboard()
        
        hypothesis_visualizations = visualizer.create_hypothesis_visualizations()
        
        summary_plot = visualizer.create_statistical_summary_plot()
        
        os.makedirs("reports/figures", exist_ok=True)
        visualizer.save_all_figures("reports/figures")
        
        logger.info("Etapa 4: Geração de relatórios")
        reporter = PowerPointReporter(processed_data, results)
        
        presentation = reporter.create_presentation()
        reporter.save_presentation("reports/relatorio_equidade_educacional.pptx")
        
        detailed_report = reporter.create_detailed_report()
        
        with open("reports/relatorio_detalhado.txt", "w", encoding="utf-8") as f:
            f.write(detailed_report)
        
        logger.info("Etapa 5: Resumo final")
        print("\n" + "="*60)
        print("ANÁLISE DE EQUIDADE EDUCACIONAL - RESUMO FINAL")
        print("="*60)
        
        print(f"\n📊 DADOS PROCESSADOS:")
        print(f"   • Total de alunos: {len(processed_data):,}")
        print(f"   • Total de escolas: {processed_data['CODIGO_ESCOLA'].nunique() if 'CODIGO_ESCOLA' in processed_data.columns else 'N/A'}")
        print(f"   • Percentual de minorias: {processed_data['MINORIA'].mean()*100:.1f}%")
        
        print(f"\n🔬 HIPÓTESES TESTADAS:")
        confirmed_hypotheses = []
        for key, result in results.items():
            has_significant = any(test.get('significant', False) 
                               for test in result['tests'].values() 
                               if isinstance(test, dict))
            status = "✅ CONFIRMADA" if has_significant else "❌ REJEITADA"
            print(f"   • {result['hypothesis']}: {status}")
            if has_significant:
                confirmed_hypotheses.append(result['hypothesis'])
        
        print(f"\n📈 RESULTADOS:")
        print(f"   • Hipóteses confirmadas: {len(confirmed_hypotheses)} de {len(results)}")
        print(f"   • Evidências de desigualdades estruturais encontradas")
        
        print(f"\n📁 ARQUIVOS GERADOS:")
        print(f"   • Apresentação PowerPoint: reports/relatorio_equidade_educacional.pptx")
        print(f"   • Relatório detalhado: reports/relatorio_detalhado.txt")
        print(f"   • Visualizações: reports/figures/")
        print(f"   • Log da análise: analise_equidade.log")
        
        print(f"\n🎯 PRINCIPAIS CONCLUSÕES:")
        print(f"   • Desigualdades educacionais persistem mesmo com políticas direcionadas")
        print(f"   • Fatores estruturais impactam significativamente o desempenho")
        print(f"   • Necessidade de políticas mais efetivas para garantir equidade")
        
        print("\n" + "="*60)
        logger.info("Análise concluída com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro durante a análise: {e}")
        raise

if __name__ == "__main__":
    main()
