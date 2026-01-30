#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de generación de planchas PDF con logos dinámicos
Versión: 3.0 - WebApp Compatible
Fecha: 2026-01-30
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import A3
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color


class GeneradorPlanchasPDF:
    """Motor de generación de planchas de stickers en formato A3"""
    
    # Dimensiones de la página A3
    ANCHO_PAGINA = 29.7 * cm
    ALTO_PAGINA = 42 * cm
    
    # Especificaciones de stickers
    TAMANO_LOGO = 2.5 * cm
    TAMANO_QR = 2.1 * cm
    DIAMETRO_TROQUEL = 2.6 * cm
    GROSOR_LINEA_CORTE = 0.5
    
    # Color de línea de corte (Magenta)
    COLOR_TROQUEL = Color(1, 0, 1)
    
    # Configuración de grilla (CORREGIDA: 14 filas por columna)
    COLUMNAS = 2
    FILAS_POR_COLUMNA = 14  # Reducido de 16 a 14 para evitar cortes
    FILAS_TOTALES_POR_HOJA = COLUMNAS * FILAS_POR_COLUMNA  # 28 filas
    
    # Márgenes y espaciado
    MARGEN_SUPERIOR = 1.5 * cm
    MARGEN_INFERIOR = 1.5 * cm
    MARGEN_IZQUIERDO = 1.5 * cm
    MARGEN_DERECHO = 1.5 * cm
    ESPACIO_ENTRE_ELEMENTOS = 0.3 * cm
    ESPACIO_ENTRE_FILAS = 0.5 * cm
    ANCHO_ZONA_ID = 1.5 * cm
    SEPARACION_ID_STICKER = 0.8 * cm
    
    def __init__(self, carpeta_qrs="qrs", logo_principal="logo.png", 
                 logos_especiales=None):
        """
        Inicializa el generador de planchas
        
        Args:
            carpeta_qrs: Ruta a la carpeta con los archivos QR
            logo_principal: Ruta al logo por defecto
            logos_especiales: Dict {id_numero: ruta_logo} para logos personalizados
        """
        self.carpeta_qrs = Path(carpeta_qrs)
        self.logo_principal = Path(logo_principal)
        self.logos_especiales = logos_especiales or {}
        self.qrs_ordenados = []
        
    def validar_archivos(self):
        """Valida que existan los archivos necesarios"""
        errores = []
        advertencias = []
        
        # Validar logo principal
        if not self.logo_principal.exists():
            errores.append(f"No se encontró el logo principal: {self.logo_principal}")
        
        # Validar logos especiales
        for id_num, ruta_logo in self.logos_especiales.items():
            if not Path(ruta_logo).exists():
                advertencias.append(f"Logo especial para ID {id_num} no encontrado: {ruta_logo}")
        
        # Validar carpeta de QRs
        if not self.carpeta_qrs.exists():
            errores.append(f"No se encontró la carpeta de QRs: {self.carpeta_qrs}")
        else:
            self.qrs_ordenados = self._obtener_qrs_ordenados()
            if not self.qrs_ordenados:
                errores.append(f"No se encontraron archivos QR en: {self.carpeta_qrs}")
        
        if errores:
            raise FileNotFoundError("\n".join(errores))
        
        return advertencias
    
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
        
        qrs.sort(key=lambda x: x[0])
        return qrs
    
    def _obtener_logo_para_id(self, numero_id):
        """
        Obtiene la ruta del logo correspondiente a un ID
        
        Args:
            numero_id: Número identificador
            
        Returns:
            Path del logo a usar (especial o principal)
        """
        if numero_id in self.logos_especiales:
            ruta_especial = Path(self.logos_especiales[numero_id])
            if ruta_especial.exists():
                return ruta_especial
        
        return self.logo_principal
    
    def _dibujar_circulo_troquel(self, c, x_centro, y_centro):
        """Dibuja el círculo de troquel (línea de corte)"""
        c.setStrokeColor(self.COLOR_TROQUEL)
        c.setLineWidth(self.GROSOR_LINEA_CORTE)
        c.circle(x_centro, y_centro, self.DIAMETRO_TROQUEL / 2, stroke=1, fill=0)
    
    def _dibujar_imagen_centrada(self, c, ruta_imagen, x_centro, y_centro, tamano):
        """Dibuja una imagen centrada en las coordenadas especificadas"""
        x = x_centro - (tamano / 2)
        y = y_centro - (tamano / 2)
        
        try:
            c.drawImage(str(ruta_imagen), x, y, 
                       width=tamano, height=tamano, 
                       preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"⚠️  Error al cargar imagen {ruta_imagen}: {e}")
    
    def _dibujar_texto_id(self, c, numero_id, x, y):
        """Dibuja el número de ID a la izquierda de la fila (fuera de stickers)"""
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y - 3, str(numero_id))
    
    def _calcular_posicion_fila(self, indice_fila_global):
        """
        Calcula la posición de una fila en la página
        
        Args:
            indice_fila_global: Índice de fila (0-27 para 28 filas)
            
        Returns:
            Tupla (x_inicio, y_centro) para la fila
        """
        # Determinar columna (0 o 1)
        columna = indice_fila_global // self.FILAS_POR_COLUMNA
        # Fila dentro de la columna (0-13 para 14 filas)
        fila_en_columna = indice_fila_global % self.FILAS_POR_COLUMNA
        
        # Calcular ancho disponible por columna
        ancho_disponible = self.ANCHO_PAGINA - self.MARGEN_IZQUIERDO - self.MARGEN_DERECHO
        ancho_columna = ancho_disponible / self.COLUMNAS
        
        # Posición X inicial de la columna
        x_columna = self.MARGEN_IZQUIERDO + (columna * ancho_columna)
        
        # Posición Y (desde arriba hacia abajo, con margen superior)
        altura_fila = self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_FILAS
        y_centro = (self.ALTO_PAGINA - self.MARGEN_SUPERIOR - 
                   (fila_en_columna * altura_fila) - (self.DIAMETRO_TROQUEL / 2))
        
        return x_columna, y_centro
    
    def _dibujar_fila_stickers(self, c, numero_id, ruta_qr, indice_fila):
        """
        Dibuja una fila completa de stickers con logo dinámico
        
        Estructura: [ID] (espacio) [Logo] [Logo] [QR] [QR]
        
        Args:
            c: Canvas de reportlab
            numero_id: Número identificador
            ruta_qr: Ruta al archivo QR
            indice_fila: Índice de la fila en la página (0-27)
        """
        x_inicio, y_centro = self._calcular_posicion_fila(indice_fila)
        
        # Dibujar número de ID (FUERA de los stickers)
        x_id = x_inicio + 0.2 * cm
        self._dibujar_texto_id(c, numero_id, x_id, y_centro)
        
        # Obtener logo para este ID (dinámico)
        ruta_logo = self._obtener_logo_para_id(numero_id)
        
        # Posición X donde comienzan los stickers
        x_actual = x_inicio + self.ANCHO_ZONA_ID + self.SEPARACION_ID_STICKER
        
        # 1. Primer Logo con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, ruta_logo, x_actual, y_centro, 
                                     self.TAMANO_LOGO)
        x_actual += self.DIAMETRO_TROQUEL + self.ESPACIO_ENTRE_ELEMENTOS
        
        # 2. Segundo Logo con troquel
        self._dibujar_circulo_troquel(c, x_actual, y_centro)
        self._dibujar_imagen_centrada(c, ruta_logo, x_actual, y_centro, 
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
    
    def generar_pdf(self, archivo_salida="planchas_stickers.pdf", verbose=True):
        """
        Genera el archivo PDF con todas las planchas necesarias
        
        Args:
            archivo_salida: Nombre del archivo PDF de salida
            verbose: Si True, muestra mensajes en consola
            
        Returns:
            Tuple (ruta_pdf, estadisticas_dict)
        """
        advertencias = self.validar_archivos()
        
        # Crear canvas
        c = canvas.Canvas(archivo_salida, pagesize=A3)
        c.setTitle("Planchas de Stickers - WhoKey")
        c.setAuthor("Sistema Automatizado v3.0")
        
        total_qrs = len(self.qrs_ordenados)
        total_paginas = (total_qrs + self.FILAS_TOTALES_POR_HOJA - 1) // self.FILAS_TOTALES_POR_HOJA
        
        if verbose:
            print(f"📄 Generando PDF con {total_paginas} página(s) A3...")
            print(f"   Total de filas: {total_qrs}")
            print(f"   Filas por página: {self.FILAS_TOTALES_POR_HOJA} (14 por columna)")
        
        # Procesar cada QR
        for idx, (numero_id, ruta_qr) in enumerate(self.qrs_ordenados):
            # Índice de fila en la página actual (0-27)
            indice_fila_en_pagina = idx % self.FILAS_TOTALES_POR_HOJA
            
            # Si es la primera fila de una nueva página (y no es la primera página)
            if idx > 0 and indice_fila_en_pagina == 0:
                c.showPage()
                if verbose:
                    pagina_actual = (idx // self.FILAS_TOTALES_POR_HOJA)
                    print(f"   ✓ Página {pagina_actual} completada")
            
            # Dibujar la fila
            self._dibujar_fila_stickers(c, numero_id, ruta_qr, indice_fila_en_pagina)
        
        # Guardar PDF
        c.save()
        
        # Estadísticas
        estadisticas = {
            'total_paginas': total_paginas,
            'total_filas': total_qrs,
            'total_logos': total_qrs * 2,
            'total_qrs': total_qrs * 2,
            'filas_por_pagina': self.FILAS_TOTALES_POR_HOJA,
            'logos_especiales': len(self.logos_especiales),
            'advertencias': advertencias
        }
        
        if verbose:
            print(f"\n✅ PDF generado exitosamente: {archivo_salida}")
            print(f"   Tamaño: A3 (29.7cm x 42cm)")
            print(f"   Total de páginas: {total_paginas}")
            print(f"   Total de stickers: {total_qrs * 4}")
            if self.logos_especiales:
                print(f"   Logos especiales: {len(self.logos_especiales)} IDs personalizados")
        
        return archivo_salida, estadisticas


def parsear_ids_texto(texto):
    """
    Convierte un texto con IDs en una lista de números
    Soporta: "1, 5, 10" o "1-5, 10, 20-25"
    
    Args:
        texto: String con IDs separados por comas y/o rangos
        
    Returns:
        Lista de números enteros
    """
    if not texto or not texto.strip():
        return []
    
    ids = set()
    partes = texto.replace(' ', '').split(',')
    
    for parte in partes:
        if '-' in parte:
            # Es un rango
            try:
                inicio, fin = parte.split('-')
                ids.update(range(int(inicio), int(fin) + 1))
            except ValueError:
                continue
        else:
            # Es un número individual
            try:
                ids.add(int(parte))
            except ValueError:
                continue
    
    return sorted(list(ids))
