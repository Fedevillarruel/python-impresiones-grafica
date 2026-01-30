# 🖨️ Generador de Planchas de Stickers para Llaveros

Sistema automatizado para generar planchas de impresión profesional en formato A3 compatibles con Adobe Illustrator.

**Versión**: 2.0 | **Última actualización**: 30/01/2026

## 📋 Características

- ✅ Formato A3 (29.7cm x 42cm) a 300 DPI
- ✅ Medidas precisas en centímetros
- ✅ ID fuera de stickers (separado 0.8cm mínimo)
- ✅ Márgenes de seguridad de 1.5cm en los 4 lados
- ✅ Líneas de troquel en Magenta (RGB: 1, 0, 1)
- ✅ Paginación automática
- ✅ Ordenamiento numérico automático de QRs
- ✅ Compatible con Adobe Illustrator
- ✅ Manejo robusto de errores

## 🎯 Especificaciones Técnicas

### Dimensiones
- **Stickers de Logo**: 2.5cm x 2.5cm
- **Stickers de QR**: 2.1cm x 2.1cm
- **Círculo de Troquel**: 2.6cm de diámetro
- **Grosor de línea de corte**: 0.5 puntos

### Distribución por Hoja
- **Columnas**: 2
- **Filas por columna**: 16
- **Total de filas por hoja**: 32
- **Total de stickers por hoja**: 128 (64 logos + 64 QRs)

### Estructura de cada Fila
```
[ID] (espacio 0.8cm) [Logo] [Logo] [QR] [QR]
 ↓                     ↓      ↓     ↓    ↓
NNN                   2.5cm  2.5cm 2.1cm 2.1cm
(fuera)              (troquel 2.6cm cada uno)
```
- 1 número identificador (NNN) **fuera** de los círculos de corte
- 2 stickers de logo idénticos (centrados en troqueles)
- 2 stickers de QR idénticos (único por fila, centrados en troqueles)

## 📦 Requisitos

### Instalación de Dependencias

```bash
pip install reportlab
```

o con el archivo requirements.txt:

```bash
pip install -r requirements.txt
```

### Estructura de Archivos Requerida

```
impresiones whokey/
│
├── generar_planchas_stickers.py   # Script principal
├── logo.png                       # Archivo del logo (estático)
├── qrs/                           # Carpeta con códigos QR
│   ├── whokey-001.png
│   ├── whokey-002.png
│   ├── whokey-003.png
│   └── ...
└── planchas_stickers.pdf          # Archivo de salida (generado)
```

## 🚀 Uso

### Modo Básico

```bash
python generar_planchas_stickers.py
```

Este comando:
1. Lee el archivo `logo.png`
2. Lee todos los QRs de la carpeta `qrs/`
3. Los ordena numéricamente por NNN
4. Genera `planchas_stickers.pdf`

### Personalización en Código

Puedes modificar los parámetros en la función `main()`:

```python
generador = GeneradorPlanchasStickers(
    carpeta_qrs="ruta/a/qrs",           # Carpeta con QRs
    archivo_logo="ruta/a/logo.png",     # Archivo del logo
    archivo_salida="mi_plancha.pdf"     # Nombre del PDF de salida
)
```

## 📊 Ejemplos de Salida

### Ejemplo con 32 QRs (1 página)
```
✓ Logo encontrado: logo.png
✓ Carpeta QRs encontrada: qrs
✓ Total de QRs encontrados: 32

📄 Generando PDF con 1 página(s) A3...
   Total de filas: 32
   Filas por página: 32

✅ PDF generado exitosamente: planchas_stickers.pdf
   Tamaño: A3 (29.7cm x 42cm)
   Total de páginas: 1
   Total de stickers de logo: 64
   Total de stickers de QR: 64
```

### Ejemplo con 500 QRs (16 páginas)
```
✓ Logo encontrado: logo.png
✓ Carpeta QRs encontrada: qrs
✓ Total de QRs encontrados: 500

📄 Generando PDF con 16 página(s) A3...
   Total de filas: 500
   Filas por página: 32
   ✓ Página 1 completada
   ✓ Página 2 completada
   ...
   ✓ Página 16 completada

✅ PDF generado exitosamente: planchas_stickers.pdf
   Tamaño: A3 (29.7cm x 42cm)
   Total de páginas: 16
   Total de stickers de logo: 1000
   Total de stickers de QR: 1000
```

## 🛠️ Características Avanzadas

### Ordenamiento Automático
El script ordena los QRs numéricamente:
- `whokey-5.png` va antes que `whokey-10.png`
- `whokey-99.png` va antes que `whokey-100.png`

### Manejo de Errores
El script valida:
- ✅ Existencia del archivo logo
- ✅ Existencia de la carpeta de QRs
- ✅ Presencia de archivos QR válidos
- ✅ Formato correcto de nombres (whokey-NNN.png)

### Compatibilidad
- ✅ Compatible con Adobe Illustrator
- ✅ Troqueles en Magenta para separación de color
- ✅ Resolución preservada de imágenes
- ✅ Formato PDF estándar

## 🎨 Formato de Nombres de Archivo

Los QRs deben seguir el patrón:
```
whokey-NNN.png
```

Donde:
- `NNN` es un número (puede tener cualquier cantidad de dígitos)
- La extensión debe ser `.png`
- No es sensible a mayúsculas/minúsculas

Ejemplos válidos:
- ✅ `whokey-1.png`
- ✅ `whokey-001.png`
- ✅ `whokey-42.png`
- ✅ `WHOKEY-100.PNG`
- ✅ `WhoKey-999.png`

## 🔧 Solución de Problemas

### Error: "No se encontró el archivo del logo"
- Verifica que `logo.png` esté en la misma carpeta que el script
- Verifica que el nombre sea exactamente `logo.png`

### Error: "No se encontró la carpeta de QRs"
- Crea la carpeta `qrs` en la misma ubicación que el script
- Verifica los permisos de lectura

### Error: "No se encontraron archivos QR"
- Verifica que los archivos sigan el formato `whokey-NNN.png`
- Verifica que los archivos sean `.png`

## 📝 Notas Técnicas

### Centrado de Imágenes
- Los logos (2.5cm) se centran dentro del círculo de troquel (2.6cm)
- Los QRs (2.1cm) se centran dentro del círculo de troquel (2.6cm)
- El centrado es automático y preciso

### Sistema de Coordenadas
- ReportLab usa coordenadas desde la esquina inferior izquierda
- Todas las medidas se convierten automáticamente de cm a puntos
- El script calcula posiciones con precisión milimétrica

### Optimización
- Las imágenes mantienen su relación de aspecto
- Se usa máscara automática para transparencias
- El PDF se genera progresivamente (eficiente en memoria)

## 📄 Licencia

Script desarrollado para uso interno en producción de llaveros WhoKey.

---

**Desarrollado por**: Equipo de Automatización
**Fecha**: Enero 2026
**Versión**: 1.0.0
