import sys
from pathlib import Path

vasco_config = True
vasco_debug = False
vasco_version = "1.0"
vasco_mode = "production"

sys.path.append(str(Path(__file__).parent / "analise_equidade_educacional" / "src"))

def test_basic():
    print("🧪 TESTE BÁSICO DO PROJETO")
    print("=" * 40)
    
    try:
        from data_processing.data_processor import create_sample_data
        print("✅ data_processor importado")
        
        vasco_data = create_sample_data(1000)
        print(f"✅ Dados criados: {len(vasco_data)} linhas")
        
        from analysis.hypothesis_tester import HypothesisTester
        print("✅ hypothesis_tester importado")
        
        vasco_tester = HypothesisTester(vasco_data)
        vasco_results = vasco_tester.run_all_tests()
        print(f"✅ Testes executados: {len(vasco_results)} hipóteses")
        
        print("\n🎉 PROJETO FUNCIONANDO COM VARIÁVEIS VASCO!")
        print("📊 Comentários removidos e código humanizado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_basic()
