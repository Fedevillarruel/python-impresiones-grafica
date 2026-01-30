#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar archivos de prueba (logo y QRs de ejemplo)
Útil para probar el generador de planchas sin tener los archivos reales
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode


def crear_logo_prueba(ruta="logo.png", tamano=250):
    """
    Crea un logo de prueba
    
    Args:
        ruta: Ruta donde guardar el logo
        tamano: Tamaño en píxeles (250px = ~2.5cm a 254dpi)
    """
    # Crear imagen con fondo blanco
    img = Image.new('RGB', (tamano, tamano), color='white')
    draw = ImageDraw.Draw(img)
    
    # Dibujar un círculo azul
    margen = 20
    draw.ellipse([margen, margen, tamano-margen, tamano-margen], 
                 fill='#2196F3', outline='#1976D2', width=5)
    
    # Dibujar texto "LOGO"
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
    except:
        # Si falla, usar fuente por defecto
        font = ImageFont.load_default()
    
    # Calcular posición centrada del texto
    texto = "LOGO"
    bbox = draw.textbbox((0, 0), texto, font=font)
    ancho_texto = bbox[2] - bbox[0]
    alto_texto = bbox[3] - bbox[1]
    x = (tamano - ancho_texto) // 2
    y = (tamano - alto_texto) // 2 - 10
    
    # Dibujar texto blanco
    draw.text((x, y), texto, fill='white', font=font)
    
    # Guardar
    img.save(ruta, 'PNG')
    print(f"✓ Logo de prueba creado: {ruta}")


def crear_qr_prueba(numero, carpeta="qrs", tamano=210):
    """
    Crea un código QR de prueba
    
    Args:
        numero: Número identificador (NNN)
        carpeta: Carpeta donde guardar el QR
        tamano: Tamaño en píxeles (210px = ~2.1cm a 254dpi)
    """
    # Crear carpeta si no existe
    Path(carpeta).mkdir(exist_ok=True)
    
    # Generar QR con datos de prueba
    datos = f"https://whokey.com/verify/{numero:03d}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(datos)
    qr.make(fit=True)
    
    # Crear imagen
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Redimensionar al tamaño deseado
    img = img.resize((tamano, tamano), Image.Resampling.LANCZOS)
    
    # Guardar
    ruta = Path(carpeta) / f"whokey-{numero:03d}.png"
    img.save(ruta, 'PNG')
    
    return ruta


def crear_archivos_prueba(cantidad_qrs=50):
    """
    Crea todos los archivos de prueba necesarios
    
    Args:
        cantidad_qrs: Cantidad de QRs a generar
    """
    print("=" * 60)
    print("GENERADOR DE ARCHIVOS DE PRUEBA")
    print("=" * 60)
    print()
    
    try:
        # Crear logo
        print("📸 Generando logo de prueba...")
        crear_logo_prueba()
        
        # Crear QRs
        print(f"\n🔲 Generando {cantidad_qrs} códigos QR de prueba...")
        for i in range(1, cantidad_qrs + 1):
            crear_qr_prueba(i)
            if i % 10 == 0:
                print(f"   ✓ {i} QRs generados...")
        
        print(f"   ✓ {cantidad_qrs} QRs generados en total")
        
        print("\n" + "=" * 60)
        print("ARCHIVOS DE PRUEBA CREADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nAhora puedes ejecutar:")
        print("  python generar_planchas_stickers.py")
        print()
        
    except ImportError as e:
        print(f"\n❌ ERROR: Faltan librerías")
        print(f"   {e}")
        print("\nInstala las dependencias:")
        print("  pip install Pillow qrcode[pil]")
        return 1
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    # Generar 50 QRs de prueba (casi 2 páginas A3)
    exit(crear_archivos_prueba(cantidad_qrs=50))
