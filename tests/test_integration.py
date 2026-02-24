"""
test_integration.py

Testes de integração entre Python e C.
Valida o correto funcionamento da interface ctypes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mandelbrot_wrapper import MandelbrotCalculator

def test_integration():
    """Executa suite de testes de integração"""
    
    print("\n" + "="*50)
    print("TESTES DE INTEGRAÇÃO PYTHON-C")
    print("="*50 + "\n")
    
    calc = MandelbrotCalculator()
    print("✓ Biblioteca C carregada com sucesso\n")
    
    # Teste 1: Ponto dentro do conjunto
    print("Teste 1: Ponto no conjunto de Mandelbrot")
    value = calc.calculate_point(0.0, 0.0, 100)
    print(f"  Coordenadas (0, 0): {value} iterações")
    assert value == 100, "Ponto deveria estar no conjunto"
    print("  ✓ PASSOU\n")
    
    # Teste 2: Ponto fora do conjunto
    print("Teste 2: Ponto fora do conjunto")
    value = calc.calculate_point(2.0, 2.0, 100)
    print(f"  Coordenadas (2, 2): {value} iterações")
    assert value < 100, "Ponto deveria divergir"
    print("  ✓ PASSOU\n")
    
    # Teste 3: Geração de imagem
    print("Teste 3: Geração de imagem completa")
    data = calc.generate(50, 50, max_iter=50)
    print(f"  Dimensões: {data.shape}")
    assert data.shape == (50, 50), "Dimensões incorretas"
    print("  ✓ PASSOU\n")
    
    # Teste 4: Diferentes resoluções
    print("Teste 4: Diferentes resoluções")
    for w, h in [(10, 10), (100, 50), (50, 100)]:
        data = calc.generate(w, h, max_iter=30)
        assert data.shape == (h, w)
        print(f"  {w}x{h}: ✓")
    print("  ✓ PASSOU\n")
    
    print("="*50)
    print("✓ TODOS OS TESTES PASSARAM")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"\n✗ ERRO: {e}\n")
        sys.exit(1)
