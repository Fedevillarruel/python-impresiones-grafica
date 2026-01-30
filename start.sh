#!/bin/bash
# Script de inicio para el Generador de Planchas WebApp

echo "════════════════════════════════════════════════════════════════"
echo "🚀 GENERADOR DE PLANCHAS DE STICKERS - WEBAPP v3.0"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask no está instalado. Instalando..."
    pip3 install -r requirements.txt
fi

echo "✅ Dependencias verificadas"
echo ""

# Crear carpetas necesarias
echo "📁 Creando carpetas necesarias..."
mkdir -p qrs logos_especiales uploads output
echo "✅ Carpetas creadas"
echo ""

# Iniciar servidor
echo "════════════════════════════════════════════════════════════════"
echo "🌐 Iniciando servidor Flask..."
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📍 URL: http://localhost:5000"
echo "🌐 Abre tu navegador y visita la URL"
echo ""
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

python3 app.py
