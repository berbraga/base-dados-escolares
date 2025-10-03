
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind, chi2_contingency, mannwhitneyu
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class HypothesisTester:
    
    def __init__(self, data: pd.DataFrame):
        
        self.vasco_data = data
        self.results = {}
    
    def test_hypothesis_1_segregation(self) -> Dict[str, Any]:
        
        logger.info("Testando Hipótese 1: Segregação Socioespacial")
        
        school_minority_pct = self.data.groupby('CODIGO_ESCOLA').agg({
            'MINORIA': 'mean',
            'INFRA_BOA': 'mean',
            'NOTA_MATEMATICA': 'mean',
            'NOTA_PORTUGUES': 'mean'
        }).reset_index()
        
        median_minority = school_minority_pct['MINORIA'].median()
        high_minority_schools = school_minority_pct[school_minority_pct['MINORIA'] >= median_minority]
        low_minority_schools = school_minority_pct[school_minority_pct['MINORIA'] < median_minority]
        
        t_stat_infra, p_value_infra = ttest_ind(
            high_minority_schools['INFRA_BOA'], 
            low_minority_schools['INFRA_BOA']
        )
        
        t_stat_math, p_value_math = ttest_ind(
            high_minority_schools['NOTA_MATEMATICA'], 
            low_minority_schools['NOTA_MATEMATICA']
        )
        
        t_stat_port, p_value_port = ttest_ind(
            high_minority_schools['NOTA_PORTUGUES'], 
            low_minority_schools['NOTA_PORTUGUES']
        )
        
        correlation_infra = stats.pearsonr(school_minority_pct['MINORIA'], 
                                          school_minority_pct['INFRA_BOA'])[0]
        
        vasco_result = {
            'hypothesis': 'Segregação Socioespacial',
            'description': 'Alunos minoritários concentrados em escolas com menor infraestrutura',
            'tests': {
                'infrastructure_difference': {
                    't_statistic': t_stat_infra,
                    'p_value': p_value_infra,
                    'significant': p_value_infra < 0.05,
                    'effect_size': (high_minority_schools['INFRA_BOA'].mean() - 
                                  low_minority_schools['INFRA_BOA'].mean())
                },
                'math_score_difference': {
                    't_statistic': t_stat_math,
                    'p_value': p_value_math,
                    'significant': p_value_math < 0.05,
                    'effect_size': (high_minority_schools['NOTA_MATEMATICA'].mean() - 
                                  low_minority_schools['NOTA_MATEMATICA'].mean())
                },
                'portuguese_score_difference': {
                    't_statistic': t_stat_port,
                    'p_value': p_value_port,
                    'significant': p_value_port < 0.05,
                    'effect_size': (high_minority_schools['NOTA_PORTUGUES'].mean() - 
                                  low_minority_schools['NOTA_PORTUGUES'].mean())
                },
                'correlation_minority_infra': correlation_infra
            },
            'summary_stats': {
                'high_minority_schools': len(high_minority_schools),
                'low_minority_schools': len(low_minority_schools),
                'avg_infra_high_minority': high_minority_schools['INFRA_BOA'].mean(),
                'avg_infra_low_minority': low_minority_schools['INFRA_BOA'].mean()
            }
        }
        
        self.results['hypothesis_1'] = result
        return result
    
    def test_hypothesis_2_teacher_quality(self) -> Dict[str, Any]:
        
        logger.info("Testando Hipótese 2: Qualidade Docente")
        
        school_minority_pct = self.data.groupby('CODIGO_ESCOLA').agg({
            'MINORIA': 'mean',
            'DOCENTE_QUALIFICADO': 'mean',
            'NOTA_MATEMATICA': 'mean',
            'NOTA_PORTUGUES': 'mean'
        }).reset_index()
        
        median_minority = school_minority_pct['MINORIA'].median()
        high_minority_schools = school_minority_pct[school_minority_pct['MINORIA'] >= median_minority]
        low_minority_schools = school_minority_pct[school_minority_pct['MINORIA'] < median_minority]
        
        t_stat_teacher, p_value_teacher = ttest_ind(
            high_minority_schools['DOCENTE_QUALIFICADO'], 
            low_minority_schools['DOCENTE_QUALIFICADO']
        )
        
        correlation_teacher = stats.pearsonr(school_minority_pct['MINORIA'], 
                                           school_minority_pct['DOCENTE_QUALIFICADO'])[0]
        
        X = school_minority_pct[['DOCENTE_QUALIFICADO', 'MINORIA']].values
        y_math = school_minority_pct['NOTA_MATEMATICA'].values
        y_port = school_minority_pct['NOTA_PORTUGUES'].values
        
        reg_math = LinearRegression().fit(X, y_math)
        reg_port = LinearRegression().fit(X, y_port)
        
        vasco_result = {
            'hypothesis': 'Qualidade Docente',
            'description': 'Professores menos qualificados em escolas com maior concentração de minorias',
            'tests': {
                'teacher_quality_difference': {
                    't_statistic': t_stat_teacher,
                    'p_value': p_value_teacher,
                    'significant': p_value_teacher < 0.05,
                    'effect_size': (high_minority_schools['DOCENTE_QUALIFICADO'].mean() - 
                                  low_minority_schools['DOCENTE_QUALIFICADO'].mean())
                },
                'correlation_minority_teacher': correlation_teacher,
                'regression_math': {
                    'coefficient_teacher': reg_math.coef_[0],
                    'coefficient_minority': reg_math.coef_[1],
                    'r_squared': reg_math.score(X, y_math)
                },
                'regression_portuguese': {
                    'coefficient_teacher': reg_port.coef_[0],
                    'coefficient_minority': reg_port.coef_[1],
                    'r_squared': reg_port.score(X, y_port)
                }
            },
            'summary_stats': {
                'avg_teacher_quality_high_minority': high_minority_schools['DOCENTE_QUALIFICADO'].mean(),
                'avg_teacher_quality_low_minority': low_minority_schools['DOCENTE_QUALIFICADO'].mean()
            }
        }
        
        self.results['hypothesis_2'] = result
        return result
    
    def test_hypothesis_3_cultural_capital(self) -> Dict[str, Any]:
        
        logger.info("Testando Hipótese 3: Capital Cultural")
        
        minority_students = self.data[self.data['MINORIA'] == True]
        non_minority_students = self.data[self.data['MINORIA'] == False]
        
        t_stat_capital, p_value_capital = ttest_ind(
            minority_students['CAPITAL_CULTURAL'], 
            non_minority_students['CAPITAL_CULTURAL']
        )
        
        t_stat_nse, p_value_nse = ttest_ind(
            minority_students['NSE'], 
            non_minority_students['NSE']
        )
        
        correlation_capital_math = stats.pearsonr(self.data['CAPITAL_CULTURAL'], 
                                                self.data['NOTA_MATEMATICA'])[0]
        correlation_capital_port = stats.pearsonr(self.data['CAPITAL_CULTURAL'], 
                                                self.data['NOTA_PORTUGUES'])[0]
        
        X = self.data[['CAPITAL_CULTURAL', 'NSE', 'MINORIA']].values
        y_math = self.data['NOTA_MATEMATICA'].values
        y_port = self.data['NOTA_PORTUGUES'].values
        
        reg_math = LinearRegression().fit(X, y_math)
        reg_port = LinearRegression().fit(X, y_port)
        
        vasco_result = {
            'hypothesis': 'Capital Cultural',
            'description': 'Diferenças no ambiente familiar e recursos educacionais domésticos',
            'tests': {
                'cultural_capital_difference': {
                    't_statistic': t_stat_capital,
                    'p_value': p_value_capital,
                    'significant': p_value_capital < 0.05,
                    'effect_size': (minority_students['CAPITAL_CULTURAL'].mean() - 
                                  non_minority_students['CAPITAL_CULTURAL'].mean())
                },
                'nse_difference': {
                    't_statistic': t_stat_nse,
                    'p_value': p_value_nse,
                    'significant': p_value_nse < 0.05,
                    'effect_size': (minority_students['NSE'].mean() - 
                                  non_minority_students['NSE'].mean())
                },
                'correlation_capital_math': correlation_capital_math,
                'correlation_capital_portuguese': correlation_capital_port,
                'regression_math': {
                    'coefficient_capital': reg_math.coef_[0],
                    'coefficient_nse': reg_math.coef_[1],
                    'coefficient_minority': reg_math.coef_[2],
                    'r_squared': reg_math.score(X, y_math)
                },
                'regression_portuguese': {
                    'coefficient_capital': reg_port.coef_[0],
                    'coefficient_nse': reg_port.coef_[1],
                    'coefficient_minority': reg_port.coef_[2],
                    'r_squared': reg_port.score(X, y_port)
                }
            },
            'summary_stats': {
                'avg_capital_minority': minority_students['CAPITAL_CULTURAL'].mean(),
                'avg_capital_non_minority': non_minority_students['CAPITAL_CULTURAL'].mean(),
                'avg_nse_minority': minority_students['NSE'].mean(),
                'avg_nse_non_minority': non_minority_students['NSE'].mean()
            }
        }
        
        self.results['hypothesis_3'] = result
        return result
    
    def test_hypothesis_4_peer_effect(self) -> Dict[str, Any]:
        
        logger.info("Testando Hipótese 4: Efeito de Pares")
        
        school_minority_pct = self.data.groupby('CODIGO_ESCOLA').agg({
            'MINORIA': 'mean',
            'NOTA_MATEMATICA': 'mean',
            'NOTA_PORTUGUES': 'mean',
            'NSE': 'mean'
        }).reset_index()
        
        self.vasco_data = self.data.merge(
            school_minority_pct[['CODIGO_ESCOLA', 'MINORIA']], 
            on='CODIGO_ESCOLA', 
            suffixes=('', '_ESCOLA')
        )
        
        self.data['PERCENTUAL_MINORIAS_ESCOLA'] = self.data['MINORIA_ESCOLA']
        
        correlation_peer_math = stats.pearsonr(self.data['PERCENTUAL_MINORIAS_ESCOLA'], 
                                             self.data['NOTA_MATEMATICA'])[0]
        correlation_peer_port = stats.pearsonr(self.data['PERCENTUAL_MINORIAS_ESCOLA'], 
                                             self.data['NOTA_PORTUGUES'])[0]
        
        X = self.data[['PERCENTUAL_MINORIAS_ESCOLA', 'NSE', 'CAPITAL_CULTURAL', 'MINORIA']].values
        y_math = self.data['NOTA_MATEMATICA'].values
        y_port = self.data['NOTA_PORTUGUES'].values
        
        reg_math = LinearRegression().fit(X, y_math)
        reg_port = LinearRegression().fit(X, y_port)
        
        quartiles = self.data['PERCENTUAL_MINORIAS_ESCOLA'].quantile([0.25, 0.5, 0.75])
        
        q1_students = self.data[self.data['PERCENTUAL_MINORIAS_ESCOLA'] <= quartiles[0.25]]
        q4_students = self.data[self.data['PERCENTUAL_MINORIAS_ESCOLA'] >= quartiles[0.75]]
        
        t_stat_peer_math, p_value_peer_math = ttest_ind(
            q1_students['NOTA_MATEMATICA'], 
            q4_students['NOTA_MATEMATICA']
        )
        
        t_stat_peer_port, p_value_peer_port = ttest_ind(
            q1_students['NOTA_PORTUGUES'], 
            q4_students['NOTA_PORTUGUES']
        )
        
        vasco_result = {
            'hypothesis': 'Efeito de Pares',
            'description': 'Impacto negativo da composição socioeconômica da turma',
            'tests': {
                'peer_effect_math': {
                    't_statistic': t_stat_peer_math,
                    'p_value': p_value_peer_math,
                    'significant': p_value_peer_math < 0.05,
                    'effect_size': (q1_students['NOTA_MATEMATICA'].mean() - 
                                  q4_students['NOTA_MATEMATICA'].mean())
                },
                'peer_effect_portuguese': {
                    't_statistic': t_stat_peer_port,
                    'p_value': p_value_peer_port,
                    'significant': p_value_peer_port < 0.05,
                    'effect_size': (q1_students['NOTA_PORTUGUES'].mean() - 
                                  q4_students['NOTA_PORTUGUES'].mean())
                },
                'correlation_peer_math': correlation_peer_math,
                'correlation_peer_portuguese': correlation_peer_port,
                'regression_math': {
                    'coefficient_peer': reg_math.coef_[0],
                    'coefficient_nse': reg_math.coef_[1],
                    'coefficient_capital': reg_math.coef_[2],
                    'coefficient_minority': reg_math.coef_[3],
                    'r_squared': reg_math.score(X, y_math)
                },
                'regression_portuguese': {
                    'coefficient_peer': reg_port.coef_[0],
                    'coefficient_nse': reg_port.coef_[1],
                    'coefficient_capital': reg_port.coef_[2],
                    'coefficient_minority': reg_port.coef_[3],
                    'r_squared': reg_port.score(X, y_port)
                }
            },
            'summary_stats': {
                'avg_score_q1_math': q1_students['NOTA_MATEMATICA'].mean(),
                'avg_score_q4_math': q4_students['NOTA_MATEMATICA'].mean(),
                'avg_score_q1_portuguese': q1_students['NOTA_PORTUGUES'].mean(),
                'avg_score_q4_portuguese': q4_students['NOTA_PORTUGUES'].mean()
            }
        }
        
        self.results['hypothesis_4'] = result
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        
        logger.info("Iniciando todos os testes de hipóteses")
        
        self.test_hypothesis_1_segregation()
        self.test_hypothesis_2_teacher_quality()
        self.test_hypothesis_3_cultural_capital()
        self.test_hypothesis_4_peer_effect()
        
        return self.results
    
    def get_summary_report(self) -> str:
        
        if not self.results:
            return "Nenhum teste foi executado ainda."
        
        report = "RELATÓRIO DE ANÁLISE DE EQUIDADE EDUCACIONAL\n"
        report += "=" * 50 + "\n\n"
        
        for key, result in self.results.items():
            report += f"HIPÓTESE: {result['hypothesis']}\n"
            report += f"Descrição: {result['description']}\n"
            report += "-" * 30 + "\n"
            
            for test_name, test_result in result['tests'].items():
                if isinstance(test_result, dict) and 'significant' in test_result:
                    significance = "SIGNIFICATIVO" if test_result['significant'] else "NÃO SIGNIFICATIVO"
                    report += f"{test_name}: {significance} (p = {test_result['p_value']:.4f})\n"
                elif isinstance(test_result, (int, float)):
                    report += f"{test_name}: {test_result:.4f}\n"
            
            report += "\n"
        
        return report

if __name__ == "__main__":

    from data_processing.data_processor import create_sample_data
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

if __name__ == "__main__":
    from data_processing.data_processor import create_sample_data
    
    sample_vasco_data = create_sample_data(5000)
    
    tester = HypothesisTester(sample_vasco_data)
    results = tester.run_all_tests()
    
    print(tester.get_summary_report())
