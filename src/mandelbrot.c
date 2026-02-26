/* mandelbrot.c
 *
 * Implementacao do conjunto de Mandelbrot em C.
 * Responsavel pelo processamento matematico, expondo funcoes
 * que serao chamadas pelo Python via ctypes.
 *
 * O conjunto e definido pela iteracao z(n+1) = z(n)^2 + c,
 * verificando se o modulo de z ultrapassa 2 em ate max_iter iteracoes.
 */

#include "mandelbrot.h"
#include <math.h>

/* Calcula quantas iteracoes um ponto leva para divergir.
 * cr e ci sao as coordenadas real e imaginaria do ponto c.
 * Retorna max_iter se o ponto nao divergir (pertence ao conjunto).
 */
int mandelbrot_point(double cr, double ci, int max_iter) {
    double zr = 0.0;
    double zi = 0.0;
    int iter = 0;
    
    while (iter < max_iter) {
        double zr_temp = zr * zr - zi * zi + cr;
        zi = 2.0 * zr * zi + ci;
        zr = zr_temp;
        
        /* modulo ao quadrado > 4 indica divergencia */
        if (zr * zr + zi * zi > 4.0) {
            return iter;
        }
        
        iter++;
    }
    
    return max_iter;
}

/* Preenche o array output com os valores calculados para cada pixel.
 * Cada posicao do array corresponde a um pixel da imagem (linearizado).
 * O array e alocado em Python e passado por ponteiro para esta funcao.
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
