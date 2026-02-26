"""
mandelbrot_wrapper.py

Interface entre Python e C utilizando ctypes.
Carrega a biblioteca compartilhada compilada e define os tipos
dos argumentos e retorno de cada funcao antes de invoca-las.

A definicao de argtypes e restype e obrigatoria para que o ctypes
realize a conversao correta dos tipos entre as duas linguagens.
"""

import ctypes
import numpy as np
from pathlib import Path
import os

class MandelbrotCalculator:

    def __init__(self, lib_path=None):
        if lib_path is None:
            base_dir = Path(__file__).parent.parent
            lib_path = base_dir / "src" / "libmandelbrot.so"

        if not os.path.exists(lib_path):
            raise FileNotFoundError(
                f"Biblioteca não encontrada: {lib_path}\n"
                f"Execute 'make compile' primeiro!"
            )

        # carrega a biblioteca compartilhada (.so) gerada pelo gcc
        self.lib = ctypes.CDLL(str(lib_path))

        # define os tipos dos argumentos de mandelbrot_point
        # sem isso o ctypes assume int para tudo, corrompendo os doubles
        self.lib.mandelbrot_point.argtypes = [
            ctypes.c_double,  # cr: parte real
            ctypes.c_double,  # ci: parte imaginaria
            ctypes.c_int      # max_iter
        ]
        self.lib.mandelbrot_point.restype = ctypes.c_int

        # generate_mandelbrot recebe ponteiro para o array de saida
        # o array e alocado em Python e preenchido diretamente pelo C
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
        # invoca a funcao C diretamente, sem arquivo intermediario
        return self.lib.mandelbrot_point(cr, ci, max_iter)

    def generate(self, width, height, x_min=-2.5, x_max=1.5,
                y_min=-2.0, y_max=2.0, max_iter=100):

        size = width * height
        # aloca array C na memoria para receber os resultados
        output_array = (ctypes.c_int * size)()

        # C preenche o array via ponteiro, sem copia de dados
        self.lib.generate_mandelbrot(
            width, height,
            x_min, x_max,
            y_min, y_max,
            max_iter,
            output_array
        )

        # interpreta o buffer C como array numpy (sem copia adicional)
        np_array = np.frombuffer(output_array, dtype=np.int32)
        return np_array.reshape(height, width)


if __name__ == "__main__":
    calc = MandelbrotCalculator()
    print("Biblioteca C carregada com sucesso")

    value = calc.calculate_point(0.0, 0.0, 100)
    print(f"Ponto (0,0): {value} iteracoes")

    data = calc.generate(50, 50, max_iter=50)
    print(f"Imagem 50x50 gerada: {data.shape}")
