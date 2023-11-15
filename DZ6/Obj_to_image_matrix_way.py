from PIL import Image
import matplotlib.pyplot as plt
import Bresenham
from FigureManip import *


def is_visible(fig: list):
    global dots

    xa, ya, za = dots[fig[0]-1][0], dots[fig[0]-1][1], dots[fig[0]-1][2]
    xb, yb, zb = dots[fig[1]-1][0], dots[fig[1]-1][1], dots[fig[1]-1][2]
    xc, yc, zc = dots[fig[2]-1][0], dots[fig[2]-1][1], dots[fig[2]-1][2]

    C = (-xb*yc+yb*xc-ya*xc+xa*yc-xa*yb+ya*xb) / (xa*(yb*zc-zb*yc) - ya*(xb*zc-zb*xc) + za*(xb*yc-yb*xc))

    if (C <= 0): return False

    return True


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


with Image.new("RGB", (150, 150)) as image:
    for i in range(len(dots)):
        # dots[i] = ChangeVector(get_scale_matrix(20, 20, 20), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Z(0), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(55), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(75, 75, 75), get_vector(dots[i]))[:-1]

    for i in range(len(figures)):
        fig = figures[i]
        if (is_visible(fig)):
            for j in range(-1, len(fig)-1):
                Bresenham(int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))

    plt.imshow(image)
    plt.show()