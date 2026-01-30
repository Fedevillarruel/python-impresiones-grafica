# 🚀 WebApp Generador de Planchas de Stickers v3.0

Sistema web profesional para generar planchas de stickers en formato A3 con logos dinámicos.

## 🎯 Nuevas Características v3.0

### ✅ Correcciones Críticas
- **14 filas por columna** (28 totales por hoja) en lugar de 16
- **Sin cortes**: Todas las filas caben perfectamente en el A3
- **Márgenes optimizados**: 1.5cm en los 4 lados
- **ID fuera de stickers**: Completamente separado de los círculos de corte

### ✨ Funcionalidades Nuevas
- **WebApp local**: Interfaz gráfica moderna y fácil de usar
- **Logos dinámicos**: Asigna logos diferentes a IDs específicos
- **Drag & Drop**: Sube 500 QRs arrastrándolos
- **Sobrescritura automática**: Los QRs se actualizan automáticamente
- **Asignación por rangos**: Usa "1-10, 20-30" para logos especiales

---

## 📦 Instalación Rápida

```bash
# 1. Instalar dependencias Python
pip3 install -r requirements.txt

# O con npm
npm run install-deps

# 2. Iniciar servidor
npm run dev

# O directamente con Python
python3 app.py
```

El servidor se iniciará en: **http://localhost:5000**

---

## 🎨 Uso de la WebApp

### 1️⃣ Subir Códigos QR
- Arrastra todos los archivos `whokey-NNN.png` a la zona de subida
- O haz clic para seleccionarlos
- Se sobrescriben automáticamente si existen

### 2️⃣ Subir Logo Principal
- Arrastra tu logo PNG/JPG
- Se usará en todos los stickers por defecto
- Tamaño recomendado: 500×500 px mínimo

### 3️⃣ Logos Especiales (Opcional)
- Sube un logo diferente
- Especifica los IDs donde se usará:
  - Individual: `1, 5, 10`
  - Rangos: `1-10, 20-30`
  - Mixto: `1-5, 8, 10-15`

### 4️⃣ Generar y Descargar
- Haz clic en "Generar y Descargar PDF"
- El archivo se descarga automáticamente
- Listo para enviar a la imprenta

---

## 📐 Especificaciones Técnicas

### Formato de Salida
- **Tamaño**: A3 (29.7cm × 42cm)
- **Resolución**: 300 DPI
- **Filas por página**: 28 (2 columnas × 14 filas)
- **Compatible**: Adobe Illustrator

### Dimensiones de Stickers
- **Logo**: 2.5cm × 2.5cm
- **QR**: 2.1cm × 2.1cm
- **Círculo de troquel**: ⌀ 2.6cm
- **Color troquel**: Magenta RGB(1, 0, 1)
- **Grosor línea**: 0.5 puntos

### Layout por Fila
```
[ID] [0.8cm] [Logo] [Logo] [QR] [QR]
 ↓             ↓      ↓     ↓    ↓
NNN           2.5cm  2.5cm 2.1cm 2.1cm
(fuera)      (troquel 2.6cm cada uno)
```

### Márgenes de Seguridad
- **Superior**: 1.5cm
- **Inferior**: 1.5cm
- **Izquierdo**: 1.5cm
- **Derecho**: 1.5cm

---

## 🔧 API Endpoints

La WebApp expone los siguientes endpoints:

### GET `/api/status`
Obtiene el estado actual del sistema.

**Respuesta**:
```json
{
  "success": true,
  "qrs_count": 515,
  "logo_principal_exists": true,
  "logos_especiales_count": 3,
  "logos_especiales_ids": ["1", "5", "10"],
  "paginas_estimadas": 19
}
```

### POST `/api/upload-qrs`
Sube códigos QR masivamente.

**Form Data**:
- `files[]`: Múltiples archivos PNG

**Respuesta**:
```json
{
  "success": true,
  "uploaded": 500,
  "errors": [],
  "total_qrs": 500
}
```

### POST `/api/upload-logo-principal`
Sube el logo principal.

**Form Data**:
- `file`: Archivo PNG/JPG

### POST `/api/upload-logo-especial`
Sube logo especial con asignación de IDs.

**Form Data**:
- `file`: Archivo PNG/JPG
- `ids`: String "1, 5, 10-20"

**Respuesta**:
```json
{
  "success": true,
  "message": "Logo especial asignado a 12 ID(s)",
  "ids": [1, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
  "filename": "logo_especial_123456_custom.png"
}
```

### POST `/api/generar-pdf`
Genera el PDF con las planchas.

**Respuesta**:
```json
{
  "success": true,
  "message": "PDF generado exitosamente",
  "estadisticas": {
    "total_paginas": 19,
    "total_filas": 515,
    "total_logos": 1030,
    "total_qrs": 1030,
    "filas_por_pagina": 28,
    "logos_especiales": 3
  },
  "download_url": "/api/download-pdf"
}
```

### GET `/api/download-pdf`
Descarga el PDF generado.

### POST `/api/clear-logos-especiales`
Elimina todos los logos especiales.

### POST `/api/limpiar-todo`
Elimina todos los archivos (QRs, logos, PDFs).

---

## 📂 Estructura del Proyecto

```
impresiones whokey/
│
├── 🌐 WEBAPP
│   ├── app.py                          ⭐ Backend Flask
│   ├── pdf_generator.py                ⭐ Motor PDF corregido
│   ├── templates/
│   │   └── index.html                  ⭐ Frontend
│   └── package.json                    📦 Scripts npm
│
├── 📁 CARPETAS DE TRABAJO
│   ├── qrs/                            📂 Códigos QR
│   ├── logos_especiales/               📂 Logos personalizados
│   ├── uploads/                        📂 Archivos temporales
│   ├── output/                         📂 PDFs generados
│   └── logo.png                        🎨 Logo principal
│
├── 🐍 SCRIPTS LEGACY (Consola)
│   ├── generar_planchas_stickers.py    📜 Script v2.0
│   ├── crear_archivos_prueba.py        🧪 Generador de pruebas
│   └── verificar_proyecto.py           🔍 Diagnóstico
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                       📖 Documentación completa
│   ├── README_WEBAPP.md                🌐 Esta guía
│   ├── CHANGELOG.md                    📝 Historial de cambios
│   ├── GUIA_RAPIDA.md                 🚀 Guía rápida
│   └── EJEMPLOS_AVANZADOS.md          🎓 Casos avanzados
│
└── ⚙️ CONFIGURACIÓN
    ├── requirements.txt                📦 Dependencias Python
    └── .gitignore                      🚫 Archivos ignorados
```

---

## 🎯 Ejemplos de Uso

### Caso 1: Planchas Estándar (Sin Logos Especiales)
1. Sube todos los QRs
2. Sube el logo principal
3. Haz clic en "Generar y Descargar"

### Caso 2: Con Logos Especiales para Clientes VIP
1. Sube todos los QRs
2. Sube el logo principal
3. Sube un logo VIP y asigna: `1-50`
4. Sube otro logo especial y asigna: `100, 200, 300`
5. Genera el PDF

### Caso 3: Actualizar QRs Existentes
1. Simplemente arrastra los nuevos QRs
2. Se sobrescriben automáticamente
3. Regenera el PDF

---

## 🔄 Migración desde v2.0

La v3.0 es **totalmente compatible** con archivos de v2.0:

```bash
# Si tienes logo.png y carpeta qrs/ de v2.0
# Solo necesitas:

1. Instalar Flask: pip3 install flask werkzeug
2. Iniciar la webapp: python3 app.py
3. Acceder a http://localhost:5000
4. ¡Los archivos ya estarán cargados!
```

---

## 🛠️ Solución de Problemas

### Puerto 5000 ocupado
```bash
# Cambiar puerto en app.py (última línea):
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Error al subir archivos grandes
```bash
# Aumentar límite en app.py:
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1GB
```

### Logos no se ven
- Verificar que sean PNG/JPG
- Resolución mínima: 250×250 px
- Resolución óptima: 500×500 px o mayor

---

## 📊 Comparación v2.0 vs v3.0

| Característica | v2.0 | v3.0 |
|----------------|------|------|
| **Interfaz** | ❌ Línea de comandos | ✅ WebApp moderna |
| **Filas/página** | ❌ 32 (se cortaban) | ✅ 28 (perfectas) |
| **Filas/columna** | ❌ 16 (overflow) | ✅ 14 (ajustadas) |
| **Logos dinámicos** | ❌ No soportado | ✅ Sí (por ID) |
| **Drag & Drop** | ❌ No | ✅ Sí |
| **Sobrescritura QRs** | ❌ Manual | ✅ Automática |
| **Rangos de IDs** | ❌ No | ✅ "1-10, 20-30" |
| **API REST** | ❌ No | ✅ Sí |
| **Uso** | Técnico | Usuario final |

---

## 🚀 Comandos Útiles

```bash
# Iniciar servidor (modo desarrollo)
npm run dev

# Iniciar servidor (modo producción)
npm start

# Instalar dependencias
npm run install-deps

# Ver logs del servidor
python3 app.py

# Limpiar archivos temporales
rm -rf uploads/* logos_especiales/* output/*
```

---

## 📝 Notas Importantes

### Para Desarrolladores
- El motor PDF está en `pdf_generator.py`
- La clase `GeneradorPlanchasPDF` es reutilizable
- Función `parsear_ids_texto()` para parsear rangos

### Para Producción
- Cambiar `debug=True` a `debug=False` en `app.py`
- Usar WSGI server (gunicorn, uWSGI)
- Configurar HTTPS para producción
- Limitar tamaño de archivos según necesidad

### Para Imprentas
- Los círculos magenta son líneas de corte
- Los números ID NO deben cortarse
- Respetar márgenes de 1.5cm
- Configuración: 28 filas por hoja A3

---

## 🎉 Características Destacadas

✨ **Interfaz Intuitiva**: Drag & drop, visual, sin comandos
✨ **Logos Dinámicos**: Personaliza stickers por cliente
✨ **Sin Cortes**: Layout perfecto para 28 filas
✨ **Automatización**: Sobrescritura y validación automática
✨ **Profesional**: Compatible con Adobe Illustrator 300 DPI
✨ **Escalable**: Maneja desde 10 hasta 1000+ QRs

---

## 📞 Soporte

- **Repositorio**: https://github.com/Fedevillarruel/python-impresiones-grafica
- **Documentación**: Ver archivos .md en el proyecto
- **Versión**: 3.0.0
- **Estado**: ✅ Producción

---

**Desarrollado por**: Desarrollador Fullstack Senior
**Fecha**: 30 de Enero de 2026
**Tecnologías**: Python 3 + Flask + ReportLab + HTML5 + CSS3 + JavaScript

---

## 🎊 ¡Disfruta de la Nueva WebApp!
