#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generación de planchas de stickers para llaveros
Formato: A3 (29.7cm x 42cm) a 300 DPI
Compatible con Adobe Illustrator para impresión profesional

ESPECIFICACIONES:
- Márgenes de seguridad: 1.5cm en todos los lados
- ID fuera de los stickers (separado 0.8cm del primer círculo)
- Troqueles en Magenta (RGB: 1,0,1) de 0.5pts
- Logo: 2.5cm, QR: 2.1cm, Troquel: 2.6cm
- 32 filas por página (2 columnas × 16 filas)

Autor: Desarrollador Senior Python
Fecha: 2026-01-30
Versión: 2.0
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, magenta


class GeneradorPlanchasStickers:
    """Clase para generar planchas de stickers en formato A3"""
    
    # Dimensiones de la página A3
    ANCHO_PAGINA = 29.7 * cm
    ALTO_PAGINA = 42 * cm
    
    # Especificaciones de stickers
    TAMANO_LOGO = 2.5 * cm
    TAMANO_QR = 2.1 * cm
    DIAMETRO_TROQUEL = 2.6 * cm
    GROSOR_LINEA_CORTE = 0.5
    
    # Color de línea de corte (Magenta)
    COLOR_TROQUEL = Color(1, 0, 1)  # RGB: 1, 0, 1
    
    # Configuración de grilla
    COLUMNAS = 2
    FILAS_POR_COLUMNA = 16
    FILAS_TOTALES_POR_HOJA = COLUMNAS * FILAS_POR_COLUMNA  # 32 filas
    
    # Márgenes y espaciado (actualizados para seguridad de impresión)
    MARGEN_SUPERIOR = 1.5 * cm
    MARGEN_INFERIOR = 1.5 * cm
    MARGEN_IZQUIERDO = 1.5 * cm
    MARGEN_DERECHO = 1.5 * cm
    ESPACIO_ENTRE_ELEMENTOS = 0.3 * cm
    ESPACIO_ENTRE_FILAS = 0.5 * cm
    ANCHO_ZONA_ID = 1.5 * cm  # Espacio reservado para el número ID (fuera de stickers)
    SEPARACION_ID_STICKER = 0.8 * cm  # Separación mínima entre ID y primer círculo
    
    def __init__(self, carpeta_qrs="qrs", archivo_logo="logo.png", 
                 archivo_salida="planchas_stickers.pdf"):
        """
        Inicializa el generador de planchas
        
        Args:
            carpeta_qrs: Ruta a la carpeta con los archivos QR
            archivo_logo: Ruta al archivo del logo
            archivo_salida: Nombre del archivo PDF de salida
        """
        self.carpeta_qrs = Path(carpeta_qrs)
        self.archivo_logo = Path(archivo_logo)
        self.archivo_salida = archivo_salida
        self.qrs_ordenados = []
        
    def validar_archivos(self):
        """Valida que existan los archivos necesarios"""
        errores = []
        
        # Validar logo
        if not self.archivo_logo.exists():
            errores.append(f"❌ No se encontró el archivo del logo: {self.archivo_logo}")
        
        # Validar carpeta de QRs
        if not self.carpeta_qrs.exists():
            errores.append(f"❌ No se encontró la carpeta de QRs: {self.carpeta_qrs}")
        else:
            # Obtener y ordenar QRs
            self.qrs_ordenados = self._obtener_qrs_ordenados()
            if not self.qrs_ordenados:
                errores.append(f"❌ No se encontraron archivos QR en: {self.carpeta_qrs}")
        
        if errores:
            raise FileNotFoundError("\n".join(errores))
        
        print(f"✓ Logo encontrado: {self.archivo_logo}")
        print(f"✓ Carpeta QRs encontrada: {self.carpeta_qrs}")
        print(f"✓ Total de QRs encontrados: {len(self.qrs_ordenados)}")
        
    def _obtener_qrs_ordenados(self):
        """
        Obtiene y ordena los archivos QR por número (NNN)
        
        Returns:
            Lista de tuplas (numero_id, ruta_archivo)
        """
        qrs = []
        patron = re.compile(r'whokey-(\d+)\.png', re.IGNORECASE)
        
        for archivo in self.carpeta_qrs.glob("*.png"):
            match = patron.match(archivo.name)
            if match:
                numero = int(match.group(1))
                qrs.append((numero, archivo))
        
        # Ordenar por número
        qrs.sort(key=lambda x: x[0])
        return qrs
    
    def _dibujar_circulo_troquel(self, c, x_centro, y_centro):
        """
        Dibuja el círculo de troquel (línea de corte)
        
        Args:
            c: Canvas de reportlab
            x_centro: Coordenada X del centro
            y_centro: Coordenada Y del centro
        """
        c.setStrokeColor(self.COLOR_TROQUEL)
        c.setLineWidth(self.GROSOR_LINEA_CORTE)
        c.circle(x_centro, y_centro, self.DIAMETRO_TROQUEL / 2, stroke=1, fill=0)
    
    def _dibujar_imagen_centrada(self, c, ruta_imagen, x_centro, y_centro, tamano):
        """
        Dibuja una imagen centrada en las coordenadas especificadas
        
        Args:
            c: Canvas de reportlab
            ruta_imagen: Ruta al archivo de imagen
            x_centro: Coordenada X del centro
            y_centro: Coordenada Y del centro
            tamano: Tamaño de la imagen (ancho y alto)
        """
        x = x_centro - (tamano / 2)
        y = y_centro - (tamano / 2)
        
        try:
            c.drawImage(str(ruta_imagen), x, y, 
                       width=tamano, height=tamano, 
                       preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"⚠️  Error al cargar imagen {ruta_imagen}: {e}")
    
    def _dibujar_texto_id(self, c, numero_id, x, y):
        """
        Dibuja el número de ID a la izquierda de la fila (fuera de los stickers)
        
        Args:
            c: Canvas de reportlab
            numero_id: Número identificador
            x: Coordenada X (posición del texto)
            y: Coordenada Y (centro vertical de la fila)
        """
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(0, 0, 0)  # Negro
        # Alinear verticalmente el texto con el centro de la fila
        # drawString dibuja desde la baseline, ajustamos para centrar
        c.drawString(x, y - 3, str(numero_id))
    
    def _calcular_posicion_fila(self, indice_fila_global):
        """
        Calcula la posición de una fila en la página
        
        Args:
            indice_fila_global: Índice de fila (0-31)
            
        Returns:
            Tupla (x_inicio, y_centro) para la fila
        """
        # Determinar columna (0 o 1)
        columna = indice_fila_global // self.FILAS_POR_COLUMNA
        # Fila dentro de la columna (0-15)
        fila_en_columna = indice_fila_global % self.FILAS_POR_COLUMNA
        
        # Calcular ancho disponible por columna (descontando márgenes izquierdo y derecho)
        ancho_disponible = self.ANCHO_PAGINA - self.MARGEN_IZQUIERDO - self.MARGEN_DERECHO
        ancho_columna = ancho_disponible / self.COLUMNAS
        
        # Posición X inicial de la columna (incluye margen izquierdo + zona para ID)
        x_columna = self.MARGEN_IZQUIERDO + (columna * ancho_columna)
        
        # Posición Y (desde arriba hacia abajo, con margen superior)
        altura_fila = self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_FILAS
        y_centro = (self.ALTO_PAGINA - self.MARGEN_SUPERIOR - 
                   (fila_en_columna * altura_fila) - (self.DIAMETRO_TROQUEL / 2))
        
        return x_columna, y_centro
    
    def _dibujar_fila_stickers(self, c, numero_id, ruta_qr, indice_fila):
        """
        Dibuja una fila completa de stickers
        
        Estructura: [ID] (espacio) [Logo] [Logo] [QR] [QR]
        El ID está completamente fuera de los círculos de corte
        
        Args:
            c: Canvas de reportlab
            numero_id: Número identificador
            ruta_qr: Ruta al archivo QR
            indice_fila: Índice de la fila en la página (0-31)
        """
        x_inicio, y_centro = self._calcular_posicion_fila(indice_fila)
        
        # Dibujar número de ID a la izquierda (FUERA de los stickers)
        x_id = x_inicio + 0.2 * cm  # Pequeño margen desde el borde de la columna
        self._dibujar_texto_id(c, numero_id, x_id, y_centro)
        
        # Posición X donde comienzan los stickers (después del ID + separación)
        x_actual = x_inicio + self.ANCHO_ZONA_ID + self.SEPARACION_ID_STICKER
        
        # 1. Primer Logo con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, self.archivo_logo, x_actual, y_centro, 
                                     self.TAMANO_LOGO)
        x_actual += self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_ELEMENTOS
        
        # 2. Segundo Logo con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, self.archivo_logo, x_actual, y_centro, 
                                     self.TAMANO_LOGO)
        x_actual += self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_ELEMENTOS
        
        # 3. Primer QR con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, ruta_qr, x_actual, y_centro, 
                                     self.TAMANO_QR)
        x_actual += self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_ELEMENTOS
        
        # 4. Segundo QR (mismo) con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, ruta_qr, x_actual, y_centro, 
                                     self.TAMANO_QR)
    
    def generar_pdf(self):
        """Genera el archivo PDF con todas las planchas necesarias"""
        self.validar_archivos()
        
        # Crear canvas
        c = canvas.Canvas(self.archivo_salida, pagesize=A3)
        c.setTitle("Planchas de Stickers - Llaveros WhoKey")
        c.setAuthor("Sistema Automatizado")
        
        total_qrs = len(self.qrs_ordenados)
        total_paginas = (total_qrs + self.FILAS_TOTALES_POR_HOJA - 1) // self.FILAS_TOTALES_POR_HOJA
        
        print(f"\n📄 Generando PDF con {total_paginas} página(s) A3...")
        print(f"   Total de filas: {total_qrs}")
        print(f"   Filas por página: {self.FILAS_TOTALES_POR_HOJA}")
        
        # Procesar cada QR
        for idx, (numero_id, ruta_qr) in enumerate(self.qrs_ordenados):
            # Índice de fila en la página actual (0-31)
            indice_fila_en_pagina = idx % self.FILAS_TOTALES_POR_HOJA
            
            # Si es la primera fila de una nueva página (y no es la primera página)
            if idx > 0 and indice_fila_en_pagina == 0:
                c.showPage()  # Nueva página
                pagina_actual = (idx // self.FILAS_TOTALES_POR_HOJA) + 1
                print(f"   ✓ Página {pagina_actual} completada")
            
            # Dibujar la fila
            self._dibujar_fila_stickers(c, numero_id, ruta_qr, indice_fila_en_pagina)
        
        # Guardar PDF
        c.save()
        print(f"\n✅ PDF generado exitosamente: {self.archivo_salida}")
        print(f"   Tamaño: A3 (29.7cm x 42cm)")
        print(f"   Total de páginas: {total_paginas}")
        print(f"   Total de stickers de logo: {total_qrs * 2}")
        print(f"   Total de stickers de QR: {total_qrs * 2}")


def main():
    """Función principal"""
    print("=" * 60)
    print("GENERADOR DE PLANCHAS DE STICKERS - WHOKEY")
    print("=" * 60)
    print()
    
    try:
        # Crear instancia del generador
        generador = GeneradorPlanchasStickers(
            carpeta_qrs="qrs",
            archivo_logo="logo.png",
            archivo_salida="planchas_stickers.pdf"
        )
        
        # Generar el PDF
        generador.generar_pdf()
        
        print("\n" + "=" * 60)
        print("PROCESO COMPLETADO CON ÉXITO")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Archivos faltantes\n{e}")
        print("\nVerifica que:")
        print("  - El archivo 'logo.png' esté en la carpeta actual")
        print("  - La carpeta 'qrs' exista y contenga archivos whokey-NNN.png")
        return 1
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
