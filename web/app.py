"""
app.py

Servidor web Flask para interface do Mandelbrot.
Demonstra a camada de apresentação em Python.
"""

from flask import Flask, render_template, request, send_file, jsonify
import numpy as np
from PIL import Image
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from mandelbrot_wrapper import MandelbrotCalculator

app = Flask(__name__)

try:
    calculator = MandelbrotCalculator()
    print("✓ Biblioteca C carregada com sucesso")
except Exception as e:
    print(f"✗ Erro ao carregar biblioteca: {e}")
    print("Execute 'make compile' primeiro!")
    sys.exit(1)


def create_colormap(iterations, max_iter):
    """
    Cria um mapa de cores para visualização do fractal.
    
    Pontos que convergem são pretos.
    Pontos que divergem recebem cores baseadas na velocidade.
    """
    normalized = iterations.astype(float) / max_iter
    
    height, width = iterations.shape
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    
    mask = iterations < max_iter
    
    rgb[:, :, 0] = (normalized * 255).astype(np.uint8)
    rgb[:, :, 1] = (np.sin(normalized * np.pi) * 255).astype(np.uint8)
    rgb[:, :, 2] = ((1 - normalized) * 255).astype(np.uint8)
    
    rgb[~mask] = [0, 0, 0]
    
    return rgb


@app.route('/')
def index():
    """Página principal da aplicação"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint que gera a imagem do Mandelbrot.
    Recebe parâmetros, chama código C e retorna imagem PNG.
    """
    try:
        data = request.get_json()
        
        width = int(data.get('width', 800))
        height = int(data.get('height', 600))
        x_min = float(data.get('x_min', -2.5))
        x_max = float(data.get('x_max', 1.5))
        y_min = float(data.get('y_min', -2.0))
        y_max = float(data.get('y_max', 2.0))
        max_iter = int(data.get('max_iter', 100))
        
        if width > 2000 or height > 2000:
            return jsonify({'error': 'Resolução muito alta (max: 2000x2000)'}), 400
        
        if max_iter > 1000:
            return jsonify({'error': 'Iterações muito altas (max: 1000)'}), 400
        
        # Chama código C para cálculo
        print(f"Gerando: {width}x{height}, iterações={max_iter}")
        iterations = calculator.generate(
            width, height,
            x_min, x_max,
            y_min, y_max,
            max_iter
        )
        
        # Cria visualização colorida em Python
        rgb_data = create_colormap(iterations, max_iter)
        image = Image.fromarray(rgb_data, mode='RGB')
        
        # Retorna imagem PNG
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return send_file(img_buffer, mimetype='image/png')
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/presets')
def presets():
    """Retorna configurações pré-definidas interessantes"""
    return jsonify([
        {
            'name': 'Visão Completa',
            'x_min': -2.5, 'x_max': 1.5,
            'y_min': -2.0, 'y_max': 2.0,
            'max_iter': 100
        },
        {
            'name': 'Espiral',
            'x_min': -0.8, 'x_max': -0.4,
            'y_min': -0.2, 'y_max': 0.2,
            'max_iter': 200
        },
        {
            'name': 'Zoom Profundo',
            'x_min': -0.7463, 'x_max': -0.7453,
            'y_min': 0.1102, 'y_max': 0.1112,
            'max_iter': 500
        }
    ])


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  MANDELBROT - INTEGRAÇÃO PYTHON + C")
    print("="*50)
    print("\nServidor rodando em: http://localhost:5000")
    print("Pressione Ctrl+C para parar")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
