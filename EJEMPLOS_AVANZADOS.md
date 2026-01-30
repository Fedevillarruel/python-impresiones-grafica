# 🎓 Ejemplos de Uso Avanzado

## Ejemplo 1: Uso Básico con Archivos de Prueba

```bash
# Paso 1: Generar archivos de prueba (50 QRs)
python crear_archivos_prueba.py

# Paso 2: Generar el PDF
python generar_planchas_stickers.py

# Paso 3: Abrir el PDF
open planchas_stickers.pdf  # macOS
# o
xdg-open planchas_stickers.pdf  # Linux
# o
start planchas_stickers.pdf  # Windows
```

## Ejemplo 2: Verificar el Proyecto Antes de Generar

```bash
# Verificar que todo esté correcto
python verificar_proyecto.py

# Si todo está bien, generar
python generar_planchas_stickers.py
```

## Ejemplo 3: Generar con Archivos Reales

```bash
# 1. Crear la estructura
mkdir qrs

# 2. Copiar tu logo
cp /ruta/a/tu/logo.png .

# 3. Copiar tus QRs
cp /ruta/a/tus/qrs/whokey-*.png qrs/

# 4. Verificar
python verificar_proyecto.py

# 5. Generar
python generar_planchas_stickers.py
```

## Ejemplo 4: Personalizar Rutas en el Script

```python
# En generar_planchas_stickers.py, modificar main():

def main():
    generador = GeneradorPlanchasStickers(
        carpeta_qrs="mis_codigos_qr",           # Carpeta personalizada
        archivo_logo="branding/logo_empresa.png", # Logo en subcarpeta
        archivo_salida="salida/planchas_enero.pdf" # PDF en subcarpeta
    )
    generador.generar_pdf()
```

## Ejemplo 5: Generar Múltiples Lotes

```bash
# Lote 1: IDs 1-100
mkdir qrs_lote1
cp qrs/whokey-{001..100}.png qrs_lote1/
python generar_planchas_stickers.py  # Modificar script para usar qrs_lote1
mv planchas_stickers.pdf planchas_lote1.pdf

# Lote 2: IDs 101-200
mkdir qrs_lote2
cp qrs/whokey-{101..200}.png qrs_lote2/
python generar_planchas_stickers.py  # Modificar script para usar qrs_lote2
mv planchas_stickers.pdf planchas_lote2.pdf
```

## Ejemplo 6: Script Personalizado para Múltiples Lotes

Crear archivo `generar_lotes.py`:

```python
#!/usr/bin/env python3
from generar_planchas_stickers import GeneradorPlanchasStickers

# Configuración de lotes
lotes = [
    {"nombre": "Lote A", "carpeta": "qrs_enero", "salida": "planchas_enero.pdf"},
    {"nombre": "Lote B", "carpeta": "qrs_febrero", "salida": "planchas_febrero.pdf"},
    {"nombre": "Lote C", "carpeta": "qrs_marzo", "salida": "planchas_marzo.pdf"},
]

for lote in lotes:
    print(f"\n{'='*60}")
    print(f"Procesando: {lote['nombre']}")
    print(f"{'='*60}")
    
    generador = GeneradorPlanchasStickers(
        carpeta_qrs=lote['carpeta'],
        archivo_logo="logo.png",
        archivo_salida=lote['salida']
    )
    
    try:
        generador.generar_pdf()
        print(f"✅ {lote['nombre']} completado")
    except Exception as e:
        print(f"❌ Error en {lote['nombre']}: {e}")
```

## Ejemplo 7: Generar Solo con QRs Específicos

```python
#!/usr/bin/env python3
# generar_seleccion.py

import shutil
from pathlib import Path
from generar_planchas_stickers import GeneradorPlanchasStickers

# IDs específicos que quieres imprimir
ids_seleccionados = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

# Crear carpeta temporal
temp_qrs = Path("qrs_temp")
temp_qrs.mkdir(exist_ok=True)

# Copiar solo los QRs seleccionados
for id_num in ids_seleccionados:
    origen = Path(f"qrs/whokey-{id_num:03d}.png")
    if origen.exists():
        destino = temp_qrs / origen.name
        shutil.copy(origen, destino)
        print(f"✓ Copiado: {origen.name}")

# Generar PDF solo con los seleccionados
generador = GeneradorPlanchasStickers(
    carpeta_qrs=str(temp_qrs),
    archivo_logo="logo.png",
    archivo_salida="planchas_seleccion.pdf"
)

generador.generar_pdf()

# Limpiar carpeta temporal
shutil.rmtree(temp_qrs)
print(f"\n✅ PDF generado: planchas_seleccion.pdf")
```

## Ejemplo 8: Validar Archivos Antes de Generar

```python
#!/usr/bin/env python3
# validar_y_generar.py

from pathlib import Path
from PIL import Image
from generar_planchas_stickers import GeneradorPlanchasStickers

def validar_dimensiones():
    """Valida que todos los archivos tengan dimensiones adecuadas"""
    
    print("Validando dimensiones de imágenes...\n")
    
    # Validar logo
    logo = Image.open("logo.png")
    print(f"Logo: {logo.size[0]}x{logo.size[1]} px")
    if logo.size[0] < 200 or logo.size[1] < 200:
        print("⚠️  ADVERTENCIA: Logo tiene baja resolución")
    
    # Validar QRs
    carpeta_qrs = Path("qrs")
    qrs_validos = 0
    qrs_invalidos = []
    
    for qr_file in carpeta_qrs.glob("whokey-*.png"):
        try:
            img = Image.open(qr_file)
            if img.size[0] >= 150 and img.size[1] >= 150:
                qrs_validos += 1
            else:
                qrs_invalidos.append(qr_file.name)
        except Exception as e:
            print(f"❌ Error en {qr_file.name}: {e}")
    
    print(f"\nQRs válidos: {qrs_validos}")
    if qrs_invalidos:
        print(f"QRs con baja resolución: {len(qrs_invalidos)}")
        for qr in qrs_invalidos[:5]:
            print(f"  - {qr}")
    
    return len(qrs_invalidos) == 0

# Validar primero
if validar_dimensiones():
    print("\n✅ Todas las imágenes son válidas. Generando PDF...\n")
    generador = GeneradorPlanchasStickers()
    generador.generar_pdf()
else:
    print("\n⚠️  Hay imágenes con problemas. Revisa los archivos.")
```

## Ejemplo 9: Estadísticas del Proyecto

```bash
# Ver información detallada
python verificar_proyecto.py

# Contar archivos
ls -l qrs/ | wc -l

# Ver espacio usado
du -sh qrs/

# Buscar QRs duplicados (por tamaño)
cd qrs && find . -type f -exec ls -l {} \; | awk '{print $5}' | sort | uniq -c | sort -rn
```

## Ejemplo 10: Automatización con Cron (Linux/macOS)

```bash
# Editar crontab
crontab -e

# Agregar tarea que ejecute cada día a las 8 AM
0 8 * * * cd /ruta/al/proyecto && /usr/bin/python3 generar_planchas_stickers.py

# Agregar tarea que ejecute cada lunes
0 9 * * 1 cd /ruta/al/proyecto && /usr/bin/python3 generar_planchas_stickers.py
```

## Ejemplo 11: Script con Notificación por Email

```python
#!/usr/bin/env python3
import smtplib
from email.message import EmailMessage
from generar_planchas_stickers import GeneradorPlanchasStickers

def enviar_notificacion(archivo_pdf, total_paginas):
    """Envía email con el PDF generado"""
    msg = EmailMessage()
    msg['Subject'] = f'Planchas generadas: {total_paginas} páginas'
    msg['From'] = 'sistema@empresa.com'
    msg['To'] = 'produccion@empresa.com'
    msg.set_content(f'Se han generado {total_paginas} páginas A3.')
    
    # Adjuntar PDF
    with open(archivo_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application',
                          subtype='pdf', filename=archivo_pdf)
    
    # Enviar (configurar SMTP)
    # with smtplib.SMTP('smtp.empresa.com') as s:
    #     s.send_message(msg)

# Generar
generador = GeneradorPlanchasStickers()
generador.generar_pdf()

# Calcular páginas
total_qrs = len(generador.qrs_ordenados)
total_paginas = (total_qrs + 31) // 32

# Notificar
enviar_notificacion("planchas_stickers.pdf", total_paginas)
```

## Ejemplo 12: Integración con Base de Datos

```python
#!/usr/bin/env python3
import sqlite3
from datetime import datetime
from generar_planchas_stickers import GeneradorPlanchasStickers

# Conectar a BD
conn = sqlite3.connect('produccion.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS planchas_generadas (
        id INTEGER PRIMARY KEY,
        fecha TIMESTAMP,
        archivo TEXT,
        total_qrs INTEGER,
        total_paginas INTEGER
    )
''')

# Generar PDF
generador = GeneradorPlanchasStickers()
generador.generar_pdf()

# Registrar en BD
total_qrs = len(generador.qrs_ordenados)
total_paginas = (total_qrs + 31) // 32

cursor.execute('''
    INSERT INTO planchas_generadas (fecha, archivo, total_qrs, total_paginas)
    VALUES (?, ?, ?, ?)
''', (datetime.now(), generador.archivo_salida, total_qrs, total_paginas))

conn.commit()
conn.close()

print(f"✅ Registro guardado en base de datos")
```

---

## 🎯 Tips y Mejores Prácticas

### 1. Nombrado de Archivos
- Usa números con ceros a la izquierda: `whokey-001.png` en vez de `whokey-1.png`
- Mantén consistencia en mayúsculas/minúsculas

### 2. Resolución de Imágenes
- **Logo**: Mínimo 250x250 px (óptimo: 500x500 px)
- **QR**: Mínimo 210x210 px (óptimo: 420x420 px)
- Usar PNG con fondo transparente o blanco

### 3. Organización
- Mantén backups de los QRs originales
- Usa versionado para los PDFs: `planchas_v1.pdf`, `planchas_v2.pdf`
- Documenta cada lote generado

### 4. Validación
- Siempre ejecuta `verificar_proyecto.py` antes de generar
- Verifica visualmente el PDF antes de enviar a imprenta
- Comprueba que los troqueles sean visibles en magenta

### 5. Producción
- Genera PDFs por lotes pequeños para facilitar correcciones
- Mantén un registro de qué IDs están en cada plancha
- Prueba con una página antes de generar 500

---

**¿Más dudas?** Consulta el `README.md` o contacta al equipo de desarrollo.
