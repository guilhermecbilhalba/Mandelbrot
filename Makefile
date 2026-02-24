# Makefile - Projeto Mandelbrot
# Integração entre Python e C

CC = gcc
CFLAGS = -O3 -Wall -fPIC -shared
LDFLAGS = -lm

SRC_DIR = src
WEB_DIR = web

C_SOURCE = $(SRC_DIR)/mandelbrot.c
SHARED_LIB = $(SRC_DIR)/libmandelbrot.so

.PHONY: all compile test run clean help

all: compile

compile:
	@echo "=== Compilando código C ==="
	$(CC) $(CFLAGS) $(C_SOURCE) -o $(SHARED_LIB) $(LDFLAGS)
	@echo "✓ Compilação concluída: $(SHARED_LIB)"
	@echo ""

test: compile
	@echo "=== Testando integração Python-C ==="
	@cd $(SRC_DIR) && python3 mandelbrot_wrapper.py
	@echo ""

run: compile
	@echo "=== Iniciando servidor web ==="
	@echo "Acesse: http://localhost:5000"
	@echo ""
	@cd $(WEB_DIR) && python3 app.py

clean:
	@echo "=== Removendo arquivos compilados ==="
	@rm -f $(SHARED_LIB)
	@rm -rf $(SRC_DIR)/__pycache__
	@rm -rf $(WEB_DIR)/__pycache__
	@echo "✓ Limpeza concluída"
	@echo ""

help:
	@echo "=========================================="
	@echo "  Mandelbrot - Python + C"
	@echo "=========================================="
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make compile  - Compila código C"
	@echo "  make test     - Testa integração"
	@echo "  make run      - Executa servidor web"
	@echo "  make clean    - Remove arquivos compilados"
	@echo "  make help     - Mostra esta ajuda"
	@echo ""
