from PIL import Image
import matplotlib.pyplot as plt
from Bresenham import Bresenham
from FigureManip import *


def is_visible(fig: list):
    global dots

    xa, ya, za = dots[fig[0]-1][0], dots[fig[0]-1][1], dots[fig[0]-1][2]
    xb, yb, zb = dots[fig[1]-1][0], dots[fig[1]-1][1], dots[fig[1]-1][2]
    xc, yc, zc = dots[fig[2]-1][0], dots[fig[2]-1][1], dots[fig[2]-1][2]

    # A = (yb-ya)*(zc-za) - (zb-za)*(yc-ya)
    # B = (xc-xa)*(zb-za) - (xb-xa)*(zc-za)
    C = (xb-xa)*(yc-ya) - (yb-ya)*(xc-xa)

    if (C < 0): return False

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


with Image.new("RGB", (26, 26)) as image:
    for x in range(0, image.width):
        for y in range(0, image.height):
            if(x%2 == y%2):
                image.putpixel((x, y), (54, 54, 54))

    for i in range(len(dots)):
        dots[i] = ChangeVector(get_scale_matrix(15, 15, 15), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Z(35), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(55), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(13, 13), get_vector(dots[i]))[:-1]

    for i in range(len(figures)):
        fig = figures[i]
        if (is_visible(fig)):
            for j in range(-1, len(fig)-1):
                Bresenham(image, int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))

    plt.imshow(image)
    plt.show()