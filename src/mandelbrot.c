/**
 * mandelbrot.c
 * 
 * Implementação do cálculo do conjunto de Mandelbrot em C.
 * Este módulo é responsável pelo processamento matemático intensivo.
 * 
 * O conjunto de Mandelbrot é definido pela iteração:
 * z(n+1) = z(n)² + c
 * onde z e c são números complexos.
 */

#include "mandelbrot.h"
#include <math.h>

/**
 * Calcula o número de iterações para um ponto do conjunto de Mandelbrot
 * 
 * @param cr Parte real da coordenada complexa
 * @param ci Parte imaginária da coordenada complexa
 * @param max_iter Número máximo de iterações a testar
 * @return Número de iterações antes da divergência (ou max_iter se convergir)
 */
int mandelbrot_point(double cr, double ci, int max_iter) {
    double zr = 0.0;
    double zi = 0.0;
    int iter = 0;
    
    while (iter < max_iter) {
        double zr_temp = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci;
        zr = zr_temp;
        
        if (zr * zr + zi * zi > 4.0) {
            return iter;
        }
        
        iter++;
    }
    
    return max_iter;
}

/**
 * Gera uma imagem completa do conjunto de Mandelbrot
 * 
 * @param width Largura da imagem em pixels
 * @param height Altura da imagem em pixels
 * @param x_min Coordenada x mínima no plano complexo
 * @param x_max Coordenada x máxima no plano complexo
 * @param y_min Coordenada y mínima no plano complexo
 * @param y_max Coordenada y máxima no plano complexo
 * @param max_iter Número máximo de iterações
 * @param output Array de saída (deve ter width*height elementos)
 */
void generate_mandelbrot(int width, int height,
                        double x_min, double x_max,
                        double y_min, double y_max,
                        int max_iter, int* output) {
    
    double x_step = (x_max - x_min) / width;
    double y_step = (y_max - y_min) / height;
    
    for (int py = 0; py < height; py++) {
        for (int px = 0; px < width; px++) {
            double cr = x_min + px * x_step;
            double ci = y_min + py * y_step;
            
            int value = mandelbrot_point(cr, ci, max_iter);
            output[py * width + px] = value;
        }
    }
}
