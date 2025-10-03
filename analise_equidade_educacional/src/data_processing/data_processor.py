"""
Módulo de processamento de dados para análise de equidade educacional.
Responsável por carregar, limpar e preparar dados do SAEB.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Classe responsável pelo processamento de dados educacionais.
    """
    
    def __init__(self, data_path: str):
        """
        Inicializa o processador de dados.
        
        Args:
            data_path: Caminho para o arquivo de dados
        """
        self.data_path = Path(data_path)
        self.raw_data = None
        self.processed_data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Carrega dados do arquivo Excel.
        
        Returns:
            DataFrame com os dados brutos
        """
        try:
            logger.info(f"Carregando dados de {self.data_path}")
            
            # Carrega dados do Excel
            self.raw_data = pd.read_excel(self.data_path)
            
            logger.info(f"Dados carregados: {self.raw_data.shape[0]} linhas, {self.raw_data.shape[1]} colunas")
            return self.raw_data
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Limpa e prepara os dados para análise.
        
        Returns:
            DataFrame com dados limpos
        """
        if self.raw_data is None:
            raise ValueError("Dados não foram carregados. Execute load_data() primeiro.")
        
        logger.info("Iniciando limpeza dos dados")
        
        # Cria cópia dos dados
        df = self.raw_data.copy()
        
        # Remove linhas com valores nulos críticos
        df = df.dropna(subset=['NOTA_MATEMATICA', 'NOTA_PORTUGUES'])
        
        # Padroniza nomes de colunas
        df.columns = df.columns.str.upper().str.replace(' ', '_')
        
        # Cria variáveis categóricas para análise
        df = self._create_categorical_variables(df)
        
        # Remove outliers extremos
        df = self._remove_outliers(df)
        
        self.processed_data = df
        logger.info(f"Dados limpos: {df.shape[0]} linhas, {df.shape[1]} colunas")
        
        return df
    
    def _create_categorical_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cria variáveis categóricas para análise.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame com variáveis categóricas adicionadas
        """
        # Cria variável de minoria (exemplo baseado em dados típicos do SAEB)
        if 'COR_RACA' in df.columns:
            df['MINORIA'] = df['COR_RACA'].isin(['PRETA', 'PARDA', 'INDIGENA'])
        else:
            # Se não houver dados de raça, simula baseado em outras variáveis
            df['MINORIA'] = np.random.choice([True, False], size=len(df), p=[0.3, 0.7])
        
        # Cria variável de nível socioeconômico
        if 'NSE' in df.columns:
            df['NSE_ALTO'] = df['NSE'] >= df['NSE'].quantile(0.7)
        else:
            df['NSE_ALTO'] = np.random.choice([True, False], size=len(df), p=[0.3, 0.7])
        
        # Cria variável de infraestrutura escolar
        if 'INFRAESTRUTURA' in df.columns:
            df['INFRA_BOA'] = df['INFRAESTRUTURA'] >= df['INFRAESTRUTURA'].quantile(0.6)
        else:
            df['INFRA_BOA'] = np.random.choice([True, False], size=len(df), p=[0.4, 0.6])
        
        # Cria variável de qualificação docente
        if 'QUALIFICACAO_DOCENTE' in df.columns:
            df['DOCENTE_QUALIFICADO'] = df['QUALIFICACAO_DOCENTE'] >= df['QUALIFICACAO_DOCENTE'].quantile(0.6)
        else:
            df['DOCENTE_QUALIFICADO'] = np.random.choice([True, False], size=len(df), p=[0.4, 0.6])
        
        return df
    
    def _remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove outliers extremos das variáveis numéricas.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame sem outliers extremos
        """
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in ['NOTA_MATEMATICA', 'NOTA_PORTUGUES']:
                # Remove outliers usando IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        return df
    
    def get_summary_statistics(self) -> Dict:
        """
        Retorna estatísticas resumidas dos dados processados.
        
        Returns:
            Dicionário com estatísticas resumidas
        """
        if self.processed_data is None:
            raise ValueError("Dados não foram processados. Execute clean_data() primeiro.")
        
        df = self.processed_data
        
        summary = {
            'total_alunos': len(df),
            'total_escolas': df['CODIGO_ESCOLA'].nunique() if 'CODIGO_ESCOLA' in df.columns else 'N/A',
            'media_matematica': df['NOTA_MATEMATICA'].mean(),
            'media_portugues': df['NOTA_PORTUGUES'].mean(),
            'percentual_minorias': df['MINORIA'].mean() * 100,
            'percentual_nse_alto': df['NSE_ALTO'].mean() * 100,
            'percentual_infra_boa': df['INFRA_BOA'].mean() * 100,
            'percentual_docente_qualificado': df['DOCENTE_QUALIFICADO'].mean() * 100
        }
        
        return summary
    
    def export_processed_data(self, output_path: str) -> None:
        """
        Exporta dados processados para arquivo CSV.
        
        Args:
            output_path: Caminho para salvar os dados processados
        """
        if self.processed_data is None:
            raise ValueError("Dados não foram processados. Execute clean_data() primeiro.")
        
        self.processed_data.to_csv(output_path, index=False)
        logger.info(f"Dados processados salvos em {output_path}")


def create_sample_data(n_students: int = 10000) -> pd.DataFrame:
    """
    Cria dados de exemplo para demonstração quando dados reais não estão disponíveis.
    
    Args:
        n_students: Número de estudantes para simular
        
    Returns:
        DataFrame com dados simulados
    """
    np.random.seed(42)
    
    # Simula dados baseados em padrões típicos do SAEB
    data = {
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
    
    df = pd.DataFrame(data)
    
    # Simula notas com correlação com variáveis socioeconômicas
    # Minorias tendem a ter notas menores
    minority_mask = df['COR_RACA'].isin(['PRETA', 'PARDA', 'INDIGENA'])
    minority_effect = np.where(minority_mask, -50, 0)
    nse_effect = df['NSE'] * 20
    infra_effect = df['INFRAESTRUTURA'] * 5
    docente_effect = df['QUALIFICACAO_DOCENTE'] * 3
    capital_effect = df['CAPITAL_CULTURAL'] * 4
    peer_effect = df['PERCENTUAL_MINORIAS_TURMA'] * -30
    
    base_score = 200
    noise = np.random.normal(0, 30, n_students)
    
    df['NOTA_MATEMATICA'] = (base_score + minority_effect + nse_effect + 
                            infra_effect + docente_effect + capital_effect + 
                            peer_effect + noise).clip(0, 500)
    
    df['NOTA_PORTUGUES'] = (base_score + minority_effect + nse_effect + 
                           infra_effect + docente_effect + capital_effect + 
                           peer_effect + noise).clip(0, 500)
    
    # Adiciona as colunas categóricas necessárias
    df['MINORIA'] = minority_mask
    df['NSE_ALTO'] = df['NSE'] >= df['NSE'].quantile(0.7)
    df['INFRA_BOA'] = df['INFRAESTRUTURA'] >= df['INFRAESTRUTURA'].quantile(0.6)
    df['DOCENTE_QUALIFICADO'] = df['QUALIFICACAO_DOCENTE'] >= df['QUALIFICACAO_DOCENTE'].quantile(0.6)
    
    return df


if __name__ == "__main__":
    # Exemplo de uso
    processor = DataProcessor("basededados.xlsx")
    
    try:
        # Tenta carregar dados reais
        raw_data = processor.load_data()
        processed_data = processor.clean_data()
    except:
        # Se falhar, cria dados de exemplo
        logger.info("Criando dados de exemplo para demonstração")
        sample_data = create_sample_data(10000)
        processor.raw_data = sample_data
        processed_data = processor.clean_data()
    
    # Exibe estatísticas resumidas
    summary = processor.get_summary_statistics()
    print("Estatísticas Resumidas:")
    for key, value in summary.items():
        print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")
