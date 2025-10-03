#!/bin/bash

echo "🚀 INSTALANDO DEPENDÊNCIAS DO PROJETO DE ANÁLISE DE EQUIDADE EDUCACIONAL"
echo "=" * 70

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install python3-pip -y
fi

# Instala as dependências
echo "📦 Instalando dependências Python..."
pip3 install -r requirements.txt

echo ""
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo ""
echo "🧪 Para testar o projeto, execute:"
echo "   python3 analise_equidade_educacional/test_project.py"
echo ""
echo "🚀 Para executar a análise completa, execute:"
echo "   python3 analise_equidade_educacional/main.py"
echo ""
echo "📊 Os resultados serão salvos na pasta 'reports/'"
