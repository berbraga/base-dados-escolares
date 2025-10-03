"""
Script de teste para verificar se o projeto está funcionando corretamente.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    try:
        from data_processing.data_processor import DataProcessor, create_sample_data
        print("✅ data_processor importado com sucesso")
        
        from analysis.hypothesis_tester import HypothesisTester
        print("✅ hypothesis_tester importado com sucesso")
        
        from visualization.visualizer import Visualizer
        print("✅ visualizer importado com sucesso")
        
        from reporting.powerpoint_reporter import PowerPointReporter
        print("✅ powerpoint_reporter importado com sucesso")
        
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False

def test_data_processing():
    """Testa o processamento de dados."""
    try:
        from data_processing.data_processor import create_sample_data
        
        # Cria dados de exemplo
        sample_data = create_sample_data(1000)
        print(f"✅ Dados de exemplo criados: {len(sample_data)} linhas")
        
        # Verifica se as colunas necessárias existem
        required_columns = ['NOTA_MATEMATICA', 'NOTA_PORTUGUES', 'MINORIA', 'NSE', 
                           'CAPITAL_CULTURAL', 'INFRA_BOA', 'DOCENTE_QUALIFICADO']
        
        missing_columns = [col for col in required_columns if col not in sample_data.columns]
        if missing_columns:
            print(f"❌ Colunas faltando: {missing_columns}")
            return False
        
        print("✅ Todas as colunas necessárias estão presentes")
        return True
        
    except Exception as e:
        print(f"❌ Erro no processamento de dados: {e}")
        return False

def test_hypothesis_testing():
    """Testa os testes de hipóteses."""
    try:
        from data_processing.data_processor import create_sample_data
        from analysis.hypothesis_tester import HypothesisTester
        
        # Cria dados de exemplo
        sample_data = create_sample_data(1000)
        
        # Executa testes
        tester = HypothesisTester(sample_data)
        results = tester.run_all_tests()
        
        print(f"✅ Testes de hipóteses executados: {len(results)} hipóteses testadas")
        
        # Verifica se todas as hipóteses foram testadas
        expected_hypotheses = ['Segregação Socioespacial', 'Qualidade Docente', 
                              'Capital Cultural', 'Efeito de Pares']
        
        tested_hypotheses = [result['hypothesis'] for result in results.values()]
        missing_hypotheses = [h for h in expected_hypotheses if h not in tested_hypotheses]
        
        if missing_hypotheses:
            print(f"❌ Hipóteses não testadas: {missing_hypotheses}")
            return False
        
        print("✅ Todas as hipóteses foram testadas")
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes de hipóteses: {e}")
        return False

def test_visualization():
    """Testa a criação de visualizações."""
    try:
        from data_processing.data_processor import create_sample_data
        from analysis.hypothesis_tester import HypothesisTester
        from visualization.visualizer import Visualizer
        
        # Cria dados e executa testes
        sample_data = create_sample_data(1000)
        tester = HypothesisTester(sample_data)
        results = tester.run_all_tests()
        
        # Cria visualizações
        visualizer = Visualizer(sample_data, results)
        dashboard = visualizer.create_overview_dashboard()
        hypothesis_viz = visualizer.create_hypothesis_visualizations()
        summary_plot = visualizer.create_statistical_summary_plot()
        
        print("✅ Visualizações criadas com sucesso")
        print(f"   • Dashboard de visão geral")
        print(f"   • {len(hypothesis_viz)} visualizações de hipóteses")
        print(f"   • Gráfico de resumo estatístico")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na criação de visualizações: {e}")
        return False

def test_reporting():
    """Testa a geração de relatórios."""
    try:
        from data_processing.data_processor import create_sample_data
        from analysis.hypothesis_tester import HypothesisTester
        from reporting.powerpoint_reporter import PowerPointReporter
        
        # Cria dados e executa testes
        sample_data = create_sample_data(1000)
        tester = HypothesisTester(sample_data)
        results = tester.run_all_tests()
        
        # Cria relatório
        reporter = PowerPointReporter(sample_data, results)
        presentation = reporter.create_presentation()
        detailed_report = reporter.create_detailed_report()
        
        print("✅ Relatórios criados com sucesso")
        print(f"   • Apresentação PowerPoint: {len(presentation.slides)} slides")
        print(f"   • Relatório detalhado: {len(detailed_report)} caracteres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na geração de relatórios: {e}")
        return False

def main():
    """Executa todos os testes."""
    print("🧪 TESTANDO PROJETO DE ANÁLISE DE EQUIDADE EDUCACIONAL")
    print("=" * 60)
    
    tests = [
        ("Importação de Módulos", test_imports),
        ("Processamento de Dados", test_data_processing),
        ("Testes de Hipóteses", test_hypothesis_testing),
        ("Criação de Visualizações", test_visualization),
        ("Geração de Relatórios", test_reporting)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testando: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
        else:
            print(f"❌ Teste falhou: {test_name}")
    
    print(f"\n📊 RESULTADO DOS TESTES")
    print("=" * 30)
    print(f"✅ Testes aprovados: {passed}/{total}")
    print(f"❌ Testes falharam: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! O projeto está funcionando corretamente.")
        print("\n🚀 Para executar a análise completa, execute:")
        print("   python analise_equidade_educacional/main.py")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")
    
    return passed == total

if __name__ == "__main__":
    main()
