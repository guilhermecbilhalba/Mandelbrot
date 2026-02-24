/**
 * mandelbrot.h
 * 
 * Declarações das funções para cálculo do conjunto de Mandelbrot
 */

#ifndef MANDELBROT_H
#define MANDELBROT_H

int mandelbrot_point(double cr, double ci, int max_iter);

void generate_mandelbrot(int width, int height,
                        double x_min, double x_max,
                        double y_min, double y_max,
                        int max_iter, int* output);

#endif
