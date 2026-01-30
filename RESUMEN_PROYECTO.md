# 📦 RESUMEN DEL PROYECTO

## Generador de Planchas de Stickers - WhoKey

Sistema profesional para generación automatizada de planchas de impresión A3 para llaveros.

---

## 📁 Estructura de Archivos

```
impresiones whokey/
│
├── 🐍 SCRIPTS PRINCIPALES
│   ├── generar_planchas_stickers.py    ⭐ Script principal
│   ├── crear_archivos_prueba.py        🧪 Generador de archivos de prueba
│   └── verificar_proyecto.py           🔍 Diagnóstico y validación
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md                       📖 Documentación completa
│   ├── GUIA_RAPIDA.md                 🚀 Guía rápida de inicio
│   └── EJEMPLOS_AVANZADOS.md          🎓 Casos de uso avanzados
│
├── ⚙️ CONFIGURACIÓN
│   ├── requirements.txt                📦 Dependencias Python
│   └── .gitignore                      🚫 Archivos a ignorar en Git
│
├── 📂 ARCHIVOS DE TRABAJO (generados)
│   ├── logo.png                        🎨 Logo de la empresa
│   ├── qrs/                            📁 Carpeta con códigos QR
│   │   ├── whokey-001.png
│   │   ├── whokey-002.png
│   │   └── ...
│   └── planchas_stickers.pdf          📄 PDF generado (salida)
│
└── 📝 ESTE ARCHIVO
    └── RESUMEN_PROYECTO.md
```

---

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar
```bash
pip install reportlab
```

### 2️⃣ Generar archivos de prueba
```bash
python crear_archivos_prueba.py
```

### 3️⃣ Generar PDF
```bash
python generar_planchas_stickers.py
```

---

## 🎯 Características Principales

| Característica | Descripción |
|----------------|-------------|
| 📐 **Formato** | A3 (29.7cm × 42cm) |
| 🎨 **Compatibilidad** | Adobe Illustrator |
| 🔄 **Paginación** | Automática |
| 📊 **Capacidad** | 32 filas/página (128 stickers) |
| ✂️ **Troqueles** | Magenta RGB(1,0,1) |
| 🔢 **Ordenamiento** | Numérico automático |
| ⚠️ **Validación** | Manejo robusto de errores |

---

## 📐 Especificaciones Técnicas

### Dimensiones de Stickers
- **Logo**: 2.5 × 2.5 cm
- **QR**: 2.1 × 2.1 cm
- **Troquel**: ⌀ 2.6 cm

### Distribución por Página
- **Columnas**: 2
- **Filas/columna**: 16
- **Total/página**: 32 filas = 64 logos + 64 QRs

### Estructura de Fila
```
[ID] [Logo] [Logo] [QR] [QR]
 ↓     ↓      ↓     ↓    ↓
NNN   2.5cm  2.5cm 2.1cm 2.1cm
```

---

## 🔧 Herramientas Disponibles

### Script Principal
```bash
python generar_planchas_stickers.py
```
Genera el PDF con todas las planchas necesarias.

### Generador de Prueba
```bash
python crear_archivos_prueba.py
```
Crea logo + 50 QRs de ejemplo para testing.

### Verificador
```bash
python verificar_proyecto.py
```
Diagnóstico completo del proyecto:
- ✅ Valida archivos
- 📊 Muestra estadísticas
- 🔍 Detecta problemas
- 💡 Sugiere soluciones

---

## 📊 Ejemplos de Capacidad

| QRs | Páginas A3 | Logos | QRs totales | Tiempo aprox. |
|-----|-----------|-------|-------------|---------------|
| 32  | 1         | 64    | 64          | < 5 seg       |
| 100 | 4         | 200   | 200         | < 10 seg      |
| 500 | 16        | 1,000 | 1,000       | < 30 seg      |
| 1000| 32        | 2,000 | 2,000       | < 1 min       |

---

## 🎨 Formato de Archivos

### Logo (logo.png)
- **Formato**: PNG
- **Resolución mínima**: 250×250 px
- **Resolución óptima**: 500×500 px o superior
- **Fondo**: Transparente o blanco

### QRs (qrs/whokey-NNN.png)
- **Formato**: PNG
- **Nomenclatura**: `whokey-NNN.png` (NNN = número)
- **Resolución mínima**: 210×210 px
- **Resolución óptima**: 420×420 px o superior
- **Ejemplos válidos**:
  - ✅ `whokey-1.png`
  - ✅ `whokey-001.png`
  - ✅ `whokey-042.png`
  - ✅ `WHOKEY-100.PNG`

---

## 🚀 Flujo de Trabajo Típico

### Para Testing (Primera Vez)
```bash
# 1. Instalar
pip install reportlab

# 2. Generar archivos de prueba
python crear_archivos_prueba.py

# 3. Verificar
python verificar_proyecto.py

# 4. Generar PDF
python generar_planchas_stickers.py

# 5. Abrir resultado
open planchas_stickers.pdf
```

### Para Producción
```bash
# 1. Preparar archivos
# - Colocar logo.png
# - Copiar QRs a carpeta qrs/

# 2. Verificar
python verificar_proyecto.py

# 3. Generar
python generar_planchas_stickers.py

# 4. Validar visualmente el PDF

# 5. Enviar a imprenta
```

---

## 🛠️ Personalización

### Cambiar Rutas
Editar en `generar_planchas_stickers.py`:
```python
generador = GeneradorPlanchasStickers(
    carpeta_qrs="ruta/personalizada/qrs",
    archivo_logo="ruta/personalizada/logo.png",
    archivo_salida="salida/mi_plancha.pdf"
)
```

### Cambiar Cantidad de Prueba
Editar en `crear_archivos_prueba.py`:
```python
crear_archivos_prueba(cantidad_qrs=100)  # Cambiar número
```

---

## 📋 Checklist Pre-Impresión

Antes de enviar a la imprenta, verificar:

- [ ] ✅ PDF generado sin errores
- [ ] ✅ Círculos de troquel visibles en Magenta
- [ ] ✅ Todos los QRs son legibles
- [ ] ✅ Logo se ve nítido
- [ ] ✅ Numeración de IDs correcta
- [ ] ✅ Total de páginas esperado
- [ ] ✅ Tamaño A3 confirmado
- [ ] ✅ Abrir en Adobe Illustrator sin problemas

---

## ❓ Solución de Problemas

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### Error: "No se encontró el archivo del logo"
```bash
# Opción 1: Generar archivo de prueba
python crear_archivos_prueba.py

# Opción 2: Copiar tu logo
cp /ruta/a/tu/logo.png .
```

### Error: "No se encontraron archivos QR"
```bash
# Crear carpeta y archivos de prueba
python crear_archivos_prueba.py
```

### QRs no se ordenan correctamente
- Verifica que sigan el formato `whokey-NNN.png`
- Usa números consistentes (ej: `001` en vez de `1`)

---

## 📚 Documentación Adicional

- **README.md**: Documentación técnica completa
- **GUIA_RAPIDA.md**: Referencia rápida
- **EJEMPLOS_AVANZADOS.md**: Casos de uso complejos

---

## 🏆 Ventajas del Sistema

✅ **Automatización total** - Sin intervención manual
✅ **Escalable** - Desde 1 hasta miles de QRs
✅ **Preciso** - Medidas exactas en cm
✅ **Profesional** - Compatible con software de diseño
✅ **Robusto** - Manejo de errores y validaciones
✅ **Documentado** - Guías completas
✅ **Flexible** - Fácilmente personalizable

---

## 📞 Soporte

Para problemas o preguntas:
1. Ejecutar `python verificar_proyecto.py`
2. Revisar la documentación en `README.md`
3. Consultar ejemplos en `EJEMPLOS_AVANZADOS.md`

---

## 📊 Métricas del Código

- **Lenguaje**: Python 3.x
- **Librería principal**: ReportLab
- **Líneas de código**: ~350 (script principal)
- **Comentarios**: Alto nivel de documentación
- **Estructura**: Orientada a objetos
- **Manejo de errores**: Completo

---

## 🎯 Próximos Pasos Sugeridos

1. ✅ Instalar dependencias
2. ✅ Ejecutar verificación
3. ✅ Generar archivos de prueba
4. ✅ Revisar PDF generado
5. ✅ Reemplazar con archivos reales
6. ✅ Generar producción
7. ✅ Enviar a imprenta

---

**Versión**: 1.0.0
**Fecha**: Enero 2026
**Desarrollado para**: WhoKey Llaveros
**Tecnología**: Python + ReportLab

---

🎉 **¡Listo para usar!** 🎉
