# 🚀 Guía Rápida de Uso

## Instalación (Primera vez)

```bash
# 1. Instalar dependencias
pip install reportlab

# 2. (OPCIONAL) Para crear archivos de prueba, instalar:
pip install Pillow qrcode[pil]
```

## Uso con Archivos Reales

```bash
# 1. Asegúrate de tener la estructura:
#    - logo.png (en la carpeta principal)
#    - qrs/whokey-001.png, qrs/whokey-002.png, etc.

# 2. Ejecutar el generador
python generar_planchas_stickers.py

# 3. El archivo planchas_stickers.pdf se generará automáticamente
```

## Uso con Archivos de Prueba

```bash
# 1. Generar archivos de prueba (logo + 50 QRs)
python crear_archivos_prueba.py

# 2. Ejecutar el generador
python generar_planchas_stickers.py

# 3. Abrir el PDF generado
open planchas_stickers.pdf
```

## Personalización Rápida

### Cambiar cantidad de QRs de prueba

Edita `crear_archivos_prueba.py`, última línea:

```python
exit(crear_archivos_prueba(cantidad_qrs=100))  # Cambiar 50 por 100
```

### Cambiar rutas de archivos

Edita `generar_planchas_stickers.py`, función `main()`:

```python
generador = GeneradorPlanchasStickers(
    carpeta_qrs="mi_carpeta_qrs",      # Cambiar ruta
    archivo_logo="mi_logo.png",         # Cambiar nombre
    archivo_salida="mi_plancha.pdf"     # Cambiar salida
)
```

## Solución de Problemas Rápida

❌ **"No module named 'reportlab'"**
```bash
pip install reportlab
```

❌ **"No se encontró el archivo del logo"**
- Ejecuta primero: `python crear_archivos_prueba.py`
- O coloca tu `logo.png` en la carpeta

❌ **"No se encontraron archivos QR"**
- Crea la carpeta `qrs/`
- Coloca archivos con formato `whokey-NNN.png`

## Especificaciones Técnicas Resumidas

| Elemento | Medida |
|----------|--------|
| Página | A3 (29.7 × 42 cm) |
| Logo | 2.5 × 2.5 cm |
| QR | 2.1 × 2.1 cm |
| Troquel | ⌀ 2.6 cm |
| Filas/página | 32 (2 columnas × 16 filas) |
| Color troquel | Magenta (RGB: 1, 0, 1) |

## Estructura de Fila

```
[ID] [🔵Logo] [🔵Logo] [⬛QR] [⬛QR]
```

Cada fila = 2 logos + 2 QRs idénticos

---

¿Dudas? Consulta el **README.md** completo.
