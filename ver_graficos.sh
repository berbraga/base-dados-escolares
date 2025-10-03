#!/bin/bash

echo "📊 VISUALIZADOR DE GRÁFICOS - ANÁLISE DE EQUIDADE EDUCACIONAL"
echo "=" * 60

echo ""
echo "🎯 GRÁFICOS DISPONÍVEIS:"
echo ""

# Lista os gráficos disponíveis
for i in {1..5}; do
    case $i in
        1) echo "📈 $i - Distribuição das Notas por Grupo" ;;
        2) echo "📊 $i - Comparação por Grupos (Box Plot)" ;;
        3) echo "🔗 $i - Matriz de Correlação" ;;
        4) echo "📋 $i - Resultados das Hipóteses" ;;
        5) echo "🎯 $i - Resumo Executivo" ;;
    esac
done

echo ""
echo "🚀 COMO VISUALIZAR:"
echo ""
echo "Opção 1 - Abrir com visualizador de imagens:"
echo "   eog graficos_estaticos/01_distribuicao_notas.png"
echo ""
echo "Opção 2 - Abrir com navegador web:"
echo "   firefox graficos_estaticos/01_distribuicao_notas.png"
echo ""
echo "Opção 3 - Abrir pasta no explorador:"
echo "   nautilus graficos_estaticos/"
echo ""
echo "Opção 4 - Ver todos os gráficos:"
echo "   for img in graficos_estaticos/*.png; do eog \"\$img\" & done"
echo ""

# Verifica se há visualizadores disponíveis
if command -v eog &> /dev/null; then
    echo "✅ Eye of GNOME (eog) disponível"
elif command -v feh &> /dev/null; then
    echo "✅ feh disponível"
elif command -v firefox &> /dev/null; then
    echo "✅ Firefox disponível"
else
    echo "⚠️  Nenhum visualizador de imagens encontrado"
fi

echo ""
echo "📁 LOCALIZAÇÃO DOS GRÁFICOS:"
echo "   $(pwd)/graficos_estaticos/"
echo ""
echo "🎨 Os gráficos estão em alta resolução (300 DPI) e prontos para apresentações!"
