# Fractal de Mandelbrot - Integração Python e C

Projeto de integração entre Python e C para geração e visualização do conjunto de Mandelbrot através de interface web.

## Descrição

Aplicação gráfica que demonstra integração entre duas linguagens de programação:
- **C**: Processamento matemático intensivo (cálculo do fractal)
- **Python**: Interface web e orquestração (servidor e visualização)
- **ctypes**: Mecanismo de integração entre as linguagens

## Estrutura do Projeto

```
mandelbrot/
├── README.md
├── Makefile
├── src/
│   ├── mandelbrot.c           # Implementação C do algoritmo
│   ├── mandelbrot.h           # Declarações das funções C
│   └── mandelbrot_wrapper.py  # Wrapper Python (ctypes)
├── web/
│   ├── app.py                 # Servidor Flask
│   └── templates/
│       └── index.html         # Interface web
├── docs/
│   └── documentacao.pdf       # Documentação técnica
├── tests/
│   └── test_integration.py    # Testes de integração
└── examples/
    └── exemplo.png            # Imagem de exemplo
```

## Dependências

### Compilador C
- gcc ou clang

### Python 3.8+
- flask
- pillow
- numpy

## Instalação

### Instalação de Dependências Python

```bash
pip install flask pillow numpy
```

Nota: Caso necessário, use a flag `--break-system-packages` dependendo da configuração do sistema.

## Compilação

### Usando Makefile (recomendado)

```bash
make compile
```

### Manualmente

```bash
gcc -O3 -Wall -fPIC -shared src/mandelbrot.c -o src/libmandelbrot.so -lm
```

## Execução

### Testar Integração

```bash
make test
```

### Executar Servidor Web

```bash
make run
```

Acesse no navegador: `http://localhost:5000`

## Uso da Interface

A interface web permite:
- Configurar resolução da imagem (largura e altura)
- Definir região do plano complexo (coordenadas x e y)
- Ajustar número máximo de iterações
- Usar configurações pré-definidas (presets)
- Gerar e visualizar fractais em tempo real

## Integração entre Linguagens

### Método: ctypes

O projeto utiliza **ctypes** para integração Python-C:

1. **Compilação**: Código C é compilado como biblioteca compartilhada (.so)
2. **Carregamento**: Python carrega a biblioteca usando ctypes.CDLL
3. **Configuração**: Tipos de argumentos e retorno são definidos
4. **Invocação**: Funções C são chamadas diretamente do Python

### Exemplo de Integração

```python
# Carrega biblioteca
lib = ctypes.CDLL("libmandelbrot.so")

# Configura tipos
lib.mandelbrot_point.argtypes = [c_double, c_double, c_int]
lib.mandelbrot_point.restype = c_int

# Chama função C
resultado = lib.mandelbrot_point(0.0, 0.0, 100)
```

### Vantagens da Abordagem

- Performance nativa do C para cálculos intensivos
- Produtividade do Python para interface e orquestração
- Integração direta sem overhead de serialização
- Passagem eficiente de arrays entre linguagens

## Performance

Testes demonstram speedup significativo (15-20x) do código C comparado a implementação equivalente em Python puro, especialmente para resoluções maiores e maior número de iterações.

## Comandos do Makefile

```bash
make compile   # Compila biblioteca C
make test      # Testa integração Python-C
make run       # Inicia servidor web
make clean     # Remove arquivos compilados
make help      # Mostra ajuda
```

## Documentação Técnica

Consulte `docs/documentacao.pdf` para:
- Explicação detalhada do algoritmo de Mandelbrot
- Análise da arquitetura do sistema
- Descrição dos métodos de integração
- Comparação de abordagens alternativas
- Resultados e análise de performance

## Conceitos Demonstrados

- Integração entre linguagens via Foreign Function Interface (FFI)
- Compilação de bibliotecas compartilhadas
- Passagem de dados entre Python e C
- Servidor web com Flask
- Interface HTML/CSS/JavaScript
- Build automation com Makefile
- Testes de integração

## Licença

MIT License - Uso educacional
