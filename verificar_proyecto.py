#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación y diagnóstico del proyecto
Muestra información sobre archivos, configuración y validaciones
"""

import os
from pathlib import Path
import re


class DiagnosticoProyecto:
    """Clase para diagnosticar el estado del proyecto"""
    
    def __init__(self):
        self.carpeta_qrs = Path("qrs")
        self.archivo_logo = Path("logo.png")
        self.errores = []
        self.advertencias = []
        
    def verificar_estructura(self):
        """Verifica la estructura del proyecto"""
        print("=" * 70)
        print("🔍 DIAGNÓSTICO DEL PROYECTO - PLANCHAS DE STICKERS")
        print("=" * 70)
        print()
        
        # Verificar logo
        print("📸 LOGO")
        print("-" * 70)
        if self.archivo_logo.exists():
            tamano = self.archivo_logo.stat().st_size
            print(f"✅ Logo encontrado: {self.archivo_logo}")
            print(f"   Tamaño: {tamano:,} bytes ({tamano/1024:.2f} KB)")
        else:
            print(f"❌ Logo NO encontrado: {self.archivo_logo}")
            self.errores.append("Falta el archivo logo.png")
            print("   💡 Ejecuta: python crear_archivos_prueba.py")
        print()
        
        # Verificar carpeta QRs
        print("🔲 CÓDIGOS QR")
        print("-" * 70)
        if self.carpeta_qrs.exists():
            qrs = self._obtener_qrs()
            if qrs:
                print(f"✅ Carpeta de QRs encontrada: {self.carpeta_qrs}")
                print(f"   Total de archivos QR: {len(qrs)}")
                print(f"   Rango de IDs: {min(n for n, _ in qrs)} - {max(n for n, _ in qrs)}")
                
                # Calcular páginas necesarias
                paginas = (len(qrs) + 31) // 32
                print(f"   Páginas A3 necesarias: {paginas}")
                print(f"   Total de stickers: {len(qrs) * 4} (Logo: {len(qrs)*2}, QR: {len(qrs)*2})")
                
                # Mostrar primeros y últimos
                print(f"\n   Primeros 5 QRs:")
                for num, path in qrs[:5]:
                    print(f"      • {path.name} (ID: {num})")
                
                if len(qrs) > 5:
                    print(f"   ...")
                    print(f"   Últimos 5 QRs:")
                    for num, path in qrs[-5:]:
                        print(f"      • {path.name} (ID: {num})")
                
                # Verificar huecos en la numeración
                self._verificar_huecos(qrs)
                
            else:
                print(f"⚠️  Carpeta existe pero NO contiene QRs válidos")
                self.advertencias.append("No hay archivos QR con formato whokey-NNN.png")
                print("   💡 Los archivos deben llamarse: whokey-001.png, whokey-002.png, etc.")
        else:
            print(f"❌ Carpeta de QRs NO encontrada: {self.carpeta_qrs}")
            self.errores.append("Falta la carpeta qrs/")
            print("   💡 Ejecuta: python crear_archivos_prueba.py")
        print()
        
        # Verificar scripts
        print("🐍 SCRIPTS")
        print("-" * 70)
        scripts = {
            "generar_planchas_stickers.py": "Script principal (generador)",
            "crear_archivos_prueba.py": "Generador de archivos de prueba",
            "verificar_proyecto.py": "Este script de verificación"
        }
        
        for script, descripcion in scripts.items():
            if Path(script).exists():
                print(f"✅ {script}")
                print(f"   {descripcion}")
            else:
                print(f"⚠️  {script} - No encontrado")
        print()
        
        # Verificar dependencias
        print("📦 DEPENDENCIAS")
        print("-" * 70)
        self._verificar_dependencias()
        print()
        
        # Resumen
        self._mostrar_resumen()
        
    def _obtener_qrs(self):
        """Obtiene lista de QRs ordenados"""
        qrs = []
        patron = re.compile(r'whokey-(\d+)\.png', re.IGNORECASE)
        
        for archivo in self.carpeta_qrs.glob("*.png"):
            match = patron.match(archivo.name)
            if match:
                numero = int(match.group(1))
                qrs.append((numero, archivo))
        
        qrs.sort(key=lambda x: x[0])
        return qrs
    
    def _verificar_huecos(self, qrs):
        """Verifica si hay huecos en la numeración"""
        if not qrs:
            return
        
        numeros = [n for n, _ in qrs]
        min_num = min(numeros)
        max_num = max(numeros)
        
        esperados = set(range(min_num, max_num + 1))
        encontrados = set(numeros)
        faltantes = esperados - encontrados
        
        if faltantes:
            print(f"\n   ⚠️  ADVERTENCIA: Hay huecos en la numeración")
            print(f"      IDs faltantes: {sorted(faltantes)[:10]}", end="")
            if len(faltantes) > 10:
                print(f"... ({len(faltantes)} en total)")
            else:
                print()
            self.advertencias.append(f"{len(faltantes)} IDs faltantes en la secuencia")
    
    def _verificar_dependencias(self):
        """Verifica las dependencias de Python"""
        dependencias = {
            "reportlab": "Requerida (generación de PDF)",
            "PIL": "Opcional (solo para crear_archivos_prueba.py)",
            "qrcode": "Opcional (solo para crear_archivos_prueba.py)"
        }
        
        for modulo, descripcion in dependencias.items():
            try:
                if modulo == "PIL":
                    __import__("PIL")
                else:
                    __import__(modulo)
                print(f"✅ {modulo:15} - Instalada")
                print(f"   {descripcion}")
            except ImportError:
                if modulo == "reportlab":
                    print(f"❌ {modulo:15} - NO instalada (REQUERIDA)")
                    self.errores.append(f"Falta instalar {modulo}")
                    print(f"   💡 Ejecuta: pip install {modulo}")
                else:
                    print(f"⚠️  {modulo:15} - NO instalada (OPCIONAL)")
                    print(f"   {descripcion}")
                    print(f"   💡 Ejecuta: pip install {modulo}")
    
    def _mostrar_resumen(self):
        """Muestra resumen del diagnóstico"""
        print("📊 RESUMEN")
        print("=" * 70)
        
        if not self.errores and not self.advertencias:
            print("✅ ¡Todo listo! El proyecto está correctamente configurado.")
            print()
            print("Puedes ejecutar:")
            print("   python generar_planchas_stickers.py")
            print()
        else:
            if self.errores:
                print(f"❌ Errores encontrados: {len(self.errores)}")
                for i, error in enumerate(self.errores, 1):
                    print(f"   {i}. {error}")
                print()
            
            if self.advertencias:
                print(f"⚠️  Advertencias: {len(self.advertencias)}")
                for i, adv in enumerate(self.advertencias, 1):
                    print(f"   {i}. {adv}")
                print()
            
            if self.errores:
                print("🔧 ACCIONES RECOMENDADAS:")
                print("   1. Instalar dependencias: pip install reportlab")
                print("   2. Generar archivos de prueba: python crear_archivos_prueba.py")
                print("   3. Volver a ejecutar este diagnóstico")
                print()
        
        print("=" * 70)


def main():
    """Función principal"""
    diagnostico = DiagnosticoProyecto()
    diagnostico.verificar_estructura()
    
    return 0 if not diagnostico.errores else 1


if __name__ == "__main__":
    exit(main())
