from PIL import Image
import matplotlib.pyplot as plt
from DotManip_3D import *
from Bresenham import Bresenham

dots = []
figures = []

with open(input("Введите полный путь к файлу: ")) as file:
    info = file.read().split('\n')

    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            line = list(float(dot) for dot in line)
            D = dot(line[0], line[1], line[2])
            dots.append(D)
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )

    
with Image.new("RGB", (100, 100)) as image:
    for i in range(len(dots)):
        dots[i] = ChangeDot(get_scale_matrix(50, 50, 50), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_Z(25), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_X(55), get_vector(dots[i]))
        dots[i] = ChangeDot(get_move_matrix(50, 50), get_vector(dots[i]))

    for i in range(len(figures)):
        fig = figures[i]
        for j in range(-1, len(fig)-1):
            Bresenham(image, int(dots[fig[j]-1].x), int(dots[fig[j]-1].y), int(dots[fig[j+1]-1].x), int(dots[fig[j+1]-1].y))

    plt.imshow(image)
    plt.show()