"""
mandelbrot_wrapper.py

Wrapper Python para a biblioteca C de cálculo do Mandelbrot.
Este módulo demonstra a integração entre Python e C usando ctypes.
"""

import ctypes
import numpy as np
from pathlib import Path
import os

class MandelbrotCalculator:
    """
    Interface Python para a biblioteca C do Mandelbrot.
    Usa ctypes para carregar e chamar funções C compiladas.
    """
    
    def __init__(self, lib_path=None):
        if lib_path is None:
            base_dir = Path(__file__).parent.parent
            lib_path = base_dir / "src" / "libmandelbrot.so"
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(
                f"Biblioteca não encontrada: {lib_path}\n"
                f"Execute 'make compile' primeiro!"
            )
        
        # Carrega biblioteca C compilada
        self.lib = ctypes.CDLL(str(lib_path))
        
        # Configura assinatura da função mandelbrot_point
        self.lib.mandelbrot_point.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_int
        ]
        self.lib.mandelbrot_point.restype = ctypes.c_int
        
        # Configura assinatura da função generate_mandelbrot
        self.lib.generate_mandelbrot.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        self.lib.generate_mandelbrot.restype = None
    
    def calculate_point(self, cr, ci, max_iter=100):
        """
        Calcula o valor do Mandelbrot para um único ponto.
        
        Args:
            cr: Parte real da coordenada complexa
            ci: Parte imaginária da coordenada complexa
            max_iter: Número máximo de iterações
            
        Returns:
            Número de iterações antes da divergência
        """
        return self.lib.mandelbrot_point(cr, ci, max_iter)
    
    def generate(self, width, height, x_min=-2.5, x_max=1.5, 
                y_min=-2.0, y_max=2.0, max_iter=100):
        """
        Gera uma imagem completa do conjunto de Mandelbrot.
        
        Demonstra a passagem de arrays entre Python e C.
        
        Args:
            width: Largura da imagem em pixels
            height: Altura da imagem em pixels
            x_min, x_max: Intervalo no eixo real
            y_min, y_max: Intervalo no eixo imaginário
            max_iter: Número máximo de iterações
            
        Returns:
            Array numpy 2D com valores calculados
        """
        size = width * height
        output_array = (ctypes.c_int * size)()
        
        # Chama função C que preenche o array
        self.lib.generate_mandelbrot(
            width, height,
            x_min, x_max,
            y_min, y_max,
            max_iter,
            output_array
        )
        
        # Converte array C para numpy
        np_array = np.frombuffer(output_array, dtype=np.int32)
        return np_array.reshape(height, width)


if __name__ == "__main__":
    print("=== Teste de Integração Python-C ===\n")
    
    calc = MandelbrotCalculator()
    print("✓ Biblioteca C carregada\n")
    
    value = calc.calculate_point(0.0, 0.0, 100)
    print(f"Ponto (0,0): {value} iterações")
    
    data = calc.generate(50, 50, max_iter=50)
    print(f"Imagem 50x50: {data.shape}")
    print("\n✓ Integração funcionando!")
