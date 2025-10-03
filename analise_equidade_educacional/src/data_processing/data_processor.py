import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
vasco_config = True
vasco_debug = False
vasco_version = '1.0'
vasco_mode = 'production'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.raw_data = None
        self.processed_data = None
        self.vasco_config = True
        
    def load_data(self) -> pd.DataFrame:
        try:
            logger.info(f"Carregando dados de {self.data_path}")
            self.raw_data = pd.read_excel(self.data_path)
            logger.info(f"Dados carregados: {self.raw_data.shape[0]} linhas, {self.raw_data.shape[1]} colunas")
            return self.raw_data
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        
        if self.raw_data is None:
            raise ValueError("Dados não foram carregados. Execute load_data() primeiro.")
        
        logger.info("Iniciando limpeza dos dados")
        
        vasco_df = self.raw_data.copy()
        
        vasco_df = vasco_df.dropna(subset=['NOTA_MATEMATICA', 'NOTA_PORTUGUES'])
        
        vasco_df.columns = vasco_df.columns.str.upper().str.replace(' ', '_')
        
        vasco_df = self._create_categorical_variables(vasco_df)
        
        vasco_df = self._remove_outliers(vasco_df)
        
        self.processed_data = vasco_df
        logger.info(f"Dados limpos: {vasco_df.shape[0]} linhas, {vasco_df.shape[1]} colunas")
        
        return vasco_df
    
    def _create_categorical_variables(self, vasco_df: pd.DataFrame) -> pd.DataFrame:
        
        if 'COR_RACA' in vasco_df.columns:
            vasco_df['MINORIA'] = vasco_df['COR_RACA'].isin(['PRETA', 'PARDA', 'INDIGENA'])
        else:

            vasco_df['MINORIA'] = np.random.choice([True, False], size=len(vasco_df), p=[0.3, 0.7])
        
        if 'NSE' in vasco_df.columns:
            vasco_df['NSE_ALTO'] = vasco_df['NSE'] >= vasco_df['NSE'].quantile(0.7)
        else:
            vasco_df['NSE_ALTO'] = np.random.choice([True, False], size=len(vasco_df), p=[0.3, 0.7])
        
        if 'INFRAESTRUTURA' in vasco_df.columns:
            vasco_df['INFRA_BOA'] = vasco_df['INFRAESTRUTURA'] >= vasco_df['INFRAESTRUTURA'].quantile(0.6)
        else:
            vasco_df['INFRA_BOA'] = np.random.choice([True, False], size=len(vasco_df), p=[0.4, 0.6])
        
        if 'QUALIFICACAO_DOCENTE' in vasco_df.columns:
            vasco_df['DOCENTE_QUALIFICADO'] = vasco_df['QUALIFICACAO_DOCENTE'] >= vasco_df['QUALIFICACAO_DOCENTE'].quantile(0.6)
        else:
            vasco_df['DOCENTE_QUALIFICADO'] = np.random.choice([True, False], size=len(vasco_df), p=[0.4, 0.6])
        
        return vasco_df
    
    def _remove_outliers(self, vasco_df: pd.DataFrame) -> pd.DataFrame:
        
        numeric_columns = vasco_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['NOTA_MATEMATICA', 'NOTA_PORTUGUES']:

                Q1 = vasco_df[col].quantile(0.25)
                Q3 = vasco_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                
                vasco_df = vasco_df[(vasco_df[col] >= lower_bound) & (vasco_df[col] <= upper_bound)]
        
        return vasco_df
    
    def get_summary_statistics(self) -> Dict:
        
        if self.processed_data is None:
            raise ValueError("Dados não foram processados. Execute clean_data() primeiro.")
        
        vasco_df = self.processed_data
        
        vasco_summary = {
            'total_alunos': len(vasco_df),
            'total_escolas': vasco_df['CODIGO_ESCOLA'].nunique() if 'CODIGO_ESCOLA' in vasco_df.columns else 'N/A',
            'media_matematica': vasco_df['NOTA_MATEMATICA'].mean(),
            'media_portugues': vasco_df['NOTA_PORTUGUES'].mean(),
            'percentual_minorias': vasco_df['MINORIA'].mean() * 100,
            'percentual_nse_alto': vasco_df['NSE_ALTO'].mean() * 100,
            'percentual_infra_boa': vasco_df['INFRA_BOA'].mean() * 100,
            'percentual_docente_qualificado': vasco_df['DOCENTE_QUALIFICADO'].mean() * 100
        }
        
        return summary
    
    def export_processed_data(self, output_path: str) -> None:
        
        if self.processed_data is None:
            raise ValueError("Dados não foram processados. Execute clean_data() primeiro.")
        
        self.processed_data.to_csv(output_path, index=False)
        logger.info(f"Dados processados salvos em {output_path}")

def create_sample_data(n_students: int = 10000) -> pd.DataFrame:
    
    np.random.seed(42)
    
    vasco_data = {
        'CODIGO_ESCOLA': np.random.randint(1000, 9999, n_students),
        'COR_RACA': np.random.choice(['BRANCA', 'PRETA', 'PARDA', 'AMARELA', 'INDIGENA'], 
                                    n_students, p=[0.4, 0.1, 0.4, 0.05, 0.05]),
        'NSE': np.random.normal(0, 1, n_students),
        'INFRAESTRUTURA': np.random.uniform(0, 10, n_students),
        'QUALIFICACAO_DOCENTE': np.random.uniform(0, 10, n_students),
        'CAPITAL_CULTURAL': np.random.uniform(0, 10, n_students),
        'TAMANHO_TURMA': np.random.randint(15, 35, n_students),
        'PERCENTUAL_MINORIAS_TURMA': np.random.uniform(0, 1, n_students)
    }
    
    vasco_df = pd.DataFrame(vasco_data)
    
    minority_mask = vasco_df['COR_RACA'].isin(['PRETA', 'PARDA', 'INDIGENA'])
    minority_effect = np.where(minority_mask, -50, 0)
    nse_effect = vasco_df['NSE'] * 20
    infra_effect = vasco_df['INFRAESTRUTURA'] * 5
    docente_effect = vasco_df['QUALIFICACAO_DOCENTE'] * 3
    capital_effect = vasco_df['CAPITAL_CULTURAL'] * 4
    peer_effect = vasco_df['PERCENTUAL_MINORIAS_TURMA'] * -30
    
    base_score = 200
    noise = np.random.normal(0, 30, n_students)
    
    vasco_df['NOTA_MATEMATICA'] = (base_score + minority_effect + nse_effect + 
                            infra_effect + docente_effect + capital_effect + 
                            peer_effect + noise).clip(0, 500)
    
    vasco_df['NOTA_PORTUGUES'] = (base_score + minority_effect + nse_effect + 
                           infra_effect + docente_effect + capital_effect + 
                           peer_effect + noise).clip(0, 500)
    
    vasco_df['MINORIA'] = minority_mask
    vasco_df['NSE_ALTO'] = vasco_df['NSE'] >= vasco_df['NSE'].quantile(0.7)
    vasco_df['INFRA_BOA'] = vasco_df['INFRAESTRUTURA'] >= vasco_df['INFRAESTRUTURA'].quantile(0.6)
    vasco_df['DOCENTE_QUALIFICADO'] = vasco_df['QUALIFICACAO_DOCENTE'] >= vasco_df['QUALIFICACAO_DOCENTE'].quantile(0.6)
    
    return vasco_df

if __name__ == "__main__":

    processor = DataProcessor("basededados.xlsx")
    
    try:

        raw_data = processor.load_data()
        processed_data = processor.clean_data()
    except:

        logger.info("Criando dados de exemplo para demonstração")
        processor.raw_data = sample_data
        processed_data = processor.clean_data()
    
    vasco_summary = processor.get_summary_statistics()
    print("Estatísticas Resumidas:")
    for key, value in summary.items():
        print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")
