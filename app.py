#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Flask para el Generador de Planchas de Stickers
Versión: 3.0
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
import shutil
from pdf_generator import GeneradorPlanchasPDF, parsear_ids_texto

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['QRS_FOLDER'] = 'qrs'
app.config['LOGOS_FOLDER'] = 'logos_especiales'
app.config['OUTPUT_FOLDER'] = 'output'

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Crear carpetas necesarias
for folder in [app.config['UPLOAD_FOLDER'], app.config['QRS_FOLDER'], 
               app.config['LOGOS_FOLDER'], app.config['OUTPUT_FOLDER']]:
    Path(folder).mkdir(exist_ok=True)


def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Obtiene el estado actual del sistema"""
    qrs_path = Path(app.config['QRS_FOLDER'])
    logo_principal = Path('logo.png')
    logos_especiales_path = Path(app.config['LOGOS_FOLDER'])
    
    # Contar archivos
    qrs = list(qrs_path.glob('whokey-*.png'))
    logos_especiales = list(logos_especiales_path.glob('*.png'))
    
    # Cargar mapeo de logos especiales si existe
    mapeo_file = Path('logos_especiales_mapeo.json')
    logos_especiales_mapeo = {}
    if mapeo_file.exists():
        try:
            with open(mapeo_file, 'r') as f:
                logos_especiales_mapeo = json.load(f)
        except:
            pass
    
    return jsonify({
        'success': True,
        'qrs_count': len(qrs),
        'logo_principal_exists': logo_principal.exists(),
        'logos_especiales_count': len(logos_especiales),
        'logos_especiales_ids': list(logos_especiales_mapeo.keys()) if logos_especiales_mapeo else [],
        'paginas_estimadas': (len(qrs) + 27) // 28 if qrs else 0
    })


@app.route('/api/upload-qrs', methods=['POST'])
def upload_qrs():
    """Subida masiva de QRs"""
    if 'files[]' not in request.files:
        return jsonify({'success': False, 'error': 'No se enviaron archivos'}), 400
    
    files = request.files.getlist('files[]')
    uploaded = 0
    errors = []
    
    qrs_path = Path(app.config['QRS_FOLDER'])
    
    for file in files:
        if file and file.filename:
            # Verificar que sea un archivo whokey-NNN.png
            filename = secure_filename(file.filename)
            
            if not filename.lower().startswith('whokey-') or not filename.lower().endswith('.png'):
                errors.append(f"{filename}: debe seguir el formato whokey-NNN.png")
                continue
            
            # Guardar o sobrescribir
            filepath = qrs_path / filename
            file.save(str(filepath))
            uploaded += 1
    
    return jsonify({
        'success': True,
        'uploaded': uploaded,
        'errors': errors,
        'total_qrs': len(list(qrs_path.glob('whokey-*.png')))
    })


@app.route('/api/upload-logo-principal', methods=['POST'])
def upload_logo_principal():
    """Subida del logo principal"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Archivo vacío'}), 400
    
    if file and allowed_file(file.filename):
        # Guardar siempre como logo.png
        filepath = Path('logo.png')
        file.save(str(filepath))
        
        return jsonify({
            'success': True,
            'message': 'Logo principal guardado correctamente'
        })
    
    return jsonify({'success': False, 'error': 'Formato de archivo no permitido'}), 400


@app.route('/api/upload-logo-especial', methods=['POST'])
def upload_logo_especial():
    """Subida de logo especial con asignación de IDs"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió archivo'}), 400
    
    file = request.files['file']
    ids_texto = request.form.get('ids', '')
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Archivo vacío'}), 400
    
    if not ids_texto:
        return jsonify({'success': False, 'error': 'Debe especificar al menos un ID'}), 400
    
    # Parsear IDs
    ids = parsear_ids_texto(ids_texto)
    
    if not ids:
        return jsonify({'success': False, 'error': 'No se pudieron parsear los IDs'}), 400
    
    if file and allowed_file(file.filename):
        # Guardar archivo con nombre único
        filename = secure_filename(file.filename)
        timestamp = int(Path('logos_especiales_mapeo.json').stat().st_mtime if Path('logos_especiales_mapeo.json').exists() else 0)
        unique_filename = f"logo_especial_{timestamp}_{filename}"
        
        logos_path = Path(app.config['LOGOS_FOLDER'])
        filepath = logos_path / unique_filename
        file.save(str(filepath))
        
        # Cargar mapeo existente
        mapeo_file = Path('logos_especiales_mapeo.json')
        mapeo = {}
        if mapeo_file.exists():
            try:
                with open(mapeo_file, 'r') as f:
                    mapeo = json.load(f)
            except:
                mapeo = {}
        
        # Actualizar mapeo
        for id_num in ids:
            mapeo[str(id_num)] = str(filepath)
        
        # Guardar mapeo
        with open(mapeo_file, 'w') as f:
            json.dump(mapeo, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Logo especial asignado a {len(ids)} ID(s)',
            'ids': ids,
            'filename': unique_filename
        })
    
    return jsonify({'success': False, 'error': 'Formato de archivo no permitido'}), 400


@app.route('/api/clear-logos-especiales', methods=['POST'])
def clear_logos_especiales():
    """Limpia todos los logos especiales"""
    logos_path = Path(app.config['LOGOS_FOLDER'])
    mapeo_file = Path('logos_especiales_mapeo.json')
    
    # Eliminar archivos
    for logo_file in logos_path.glob('*.png'):
        logo_file.unlink()
    
    # Eliminar mapeo
    if mapeo_file.exists():
        mapeo_file.unlink()
    
    return jsonify({
        'success': True,
        'message': 'Logos especiales eliminados'
    })


@app.route('/api/generar-pdf', methods=['POST'])
def generar_pdf():
    """Genera el PDF con las planchas"""
    try:
        # Verificar que existan los archivos necesarios
        logo_principal = Path('logo.png')
        qrs_path = Path(app.config['QRS_FOLDER'])
        
        if not logo_principal.exists():
            return jsonify({
                'success': False,
                'error': 'Falta el logo principal. Por favor, súbelo primero.'
            }), 400
        
        qrs = list(qrs_path.glob('whokey-*.png'))
        if not qrs:
            return jsonify({
                'success': False,
                'error': 'No hay códigos QR. Por favor, súbelos primero.'
            }), 400
        
        # Cargar mapeo de logos especiales
        mapeo_file = Path('logos_especiales_mapeo.json')
        logos_especiales = {}
        if mapeo_file.exists():
            try:
                with open(mapeo_file, 'r') as f:
                    mapeo_str = json.load(f)
                    # Convertir keys de string a int
                    logos_especiales = {int(k): v for k, v in mapeo_str.items()}
            except Exception as e:
                print(f"⚠️  Error al cargar mapeo de logos: {e}")
        
        # Generar PDF
        output_path = Path(app.config['OUTPUT_FOLDER']) / 'planchas_stickers.pdf'
        
        generador = GeneradorPlanchasPDF(
            carpeta_qrs=str(qrs_path),
            logo_principal=str(logo_principal),
            logos_especiales=logos_especiales
        )
        
        archivo_pdf, estadisticas = generador.generar_pdf(
            archivo_salida=str(output_path),
            verbose=True
        )
        
        return jsonify({
            'success': True,
            'message': 'PDF generado exitosamente',
            'estadisticas': estadisticas,
            'download_url': f'/api/download-pdf'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar PDF: {str(e)}'
        }), 500


@app.route('/api/download-pdf', methods=['GET'])
def download_pdf():
    """Descarga el PDF generado"""
    pdf_path = Path(app.config['OUTPUT_FOLDER']) / 'planchas_stickers.pdf'
    
    if not pdf_path.exists():
        return jsonify({
            'success': False,
            'error': 'No hay PDF generado. Genera uno primero.'
        }), 404
    
    return send_file(
        str(pdf_path),
        as_attachment=True,
        download_name='planchas_stickers_whokey.pdf',
        mimetype='application/pdf'
    )


@app.route('/api/limpiar-todo', methods=['POST'])
def limpiar_todo():
    """Limpia todos los archivos subidos (útil para empezar de cero)"""
    try:
        # Limpiar QRs
        qrs_path = Path(app.config['QRS_FOLDER'])
        for qr_file in qrs_path.glob('*.png'):
            qr_file.unlink()
        
        # Limpiar logos especiales
        logos_path = Path(app.config['LOGOS_FOLDER'])
        for logo_file in logos_path.glob('*.png'):
            logo_file.unlink()
        
        # Limpiar mapeo
        mapeo_file = Path('logos_especiales_mapeo.json')
        if mapeo_file.exists():
            mapeo_file.unlink()
        
        # Limpiar PDFs generados
        output_path = Path(app.config['OUTPUT_FOLDER'])
        for pdf_file in output_path.glob('*.pdf'):
            pdf_file.unlink()
        
        return jsonify({
            'success': True,
            'message': 'Todos los archivos han sido eliminados'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al limpiar archivos: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 GENERADOR DE PLANCHAS DE STICKERS - WEBAPP v3.0")
    print("=" * 70)
    print("\n📍 Servidor iniciado en: http://localhost:5000")
    print("🌐 Abre tu navegador y visita la URL")
    print("\n💡 Presiona Ctrl+C para detener el servidor\n")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
