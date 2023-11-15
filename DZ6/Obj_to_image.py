from PIL import Image
import matplotlib.pyplot as plt
from Bresenham import Bresenham
from FigureManip import *

dots = []
figures = []

with open(input("Введите полный путь к файлу: ")) as file:
    info = file.read().split('\n')

    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            dots.append( list(float(dot) for dot in line) )
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )


with Image.new("RGB", (300, 300)) as image:
    for i in range(len(dots)):
        dots[i] = ChangeVector(get_scale_matrix(20, 20, 20), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Z(180+45), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(45), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Y(10), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(150, 150), get_vector(dots[i]))[:-1]

    for i in range(len(figures)):
        fig = figures[i]
        for j in range(-1, len(fig)-1):
            Bresenham(image, int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))

    plt.imshow(image)
    plt.show()