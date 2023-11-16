from PIL import Image
import matplotlib.pyplot as plt
from Bresenham import Bresenham
from FigureManip import *


class dot:
    def __init__(self, cordX: int, cordY: int, cordZ: int):
        self.x = cordX
        self.y = cordY
        self.z = cordZ


def get_normal(A: dot, B: dot, C: dot):
    coefA = (B.y-A.y)*(C.z-A.z) - (B.z-A.z)*(C.y-A.y)
    coefB = (C.x-A.x)*(B.z-A.z) - (B.x-A.x)*(C.z-A.z)
    coefC = (B.x-A.x)*(C.y-A.y) - (B.y-A.y)*(C.x-A.x)

    return tuple([coefA, coefB, coefC])


class figure:
    def __init__(self, dotA: dot, dotB: dot, dotC: dot, colour: tuple):
        self.dotA = dotA
        self.dotB = dotB
        self.dotC = dotC
        self.colour = colour
        self.normalV = get_normal(self.dotA, self.dotB, self.dotC)


def is_in_figure(xi: int, yi: int, fig: figure):
    # Обход вершин идёт по часовой стрелке (стандарт Blender)
    abV = tuple((fig.dotB.x - fig.dotA.x), (fig.dotB.y - fig.dotA.y))
    bcV = tuple((fig.dotC.x - fig.dotB.x), (fig.dotC.y - fig.dotB.y))
    caV = tuple((fig.dotA.x - fig.dotC.x), (fig.dotA.y - fig.dotC.y))

    Nab = tuple(abV[1], -abV[0])
    Nbc = tuple(bcV[1], -bcV[0])
    Nca = tuple(caV[1], -caV[0])

    atV = tuple(xi - abV[0], yi - abV[1])
    btV = tuple(xi - bcV[0], yi - bcV[1])
    ctV = tuple(xi - caV[0], yi - caV[1])

    if ((Nab[0]*atV[0] + Nab[1]+atV[1] >= 0) and (Nbc[0]*btV[0] + Nbc[1]*btV[1] >= 0) and (Nca[0]*ctV[0] + Nca[1]+ctV[1] >= 0)): return True

    return False

# def is_visible(xi: int, yi: int):
#     global dots, figures, image

#     xa, ya, za = dots[fig[0]-1][0], dots[fig[0]-1][1], dots[fig[0]-1][2]
#     xb, yb, zb = dots[fig[1]-1][0], dots[fig[1]-1][1], dots[fig[1]-1][2]
#     xc, yc, zc = dots[fig[2]-1][0], dots[fig[2]-1][1], dots[fig[2]-1][2]

#     xa, ya, za = int(xa), int(ya), int(za)
#     xb, yb, zb = int(xb), int(yb), int(zb)
#     xc, yc, zc = int(xc), int(yc), int(zc)

#     # TO DO: Сделать расчёт принадлежности точки плоскости с помощью векторов нормалей

#     pass


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
        dots[i] = ChangeVector(get_rotate_matrix_Z(180+445), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(55), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(150, 150), get_vector(dots[i]))[:-1]

    for i in range(len(figures)):
        fig = figures[i]
        for j in range(-1, len(fig)-1):
            Bresenham(int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))

    plt.imshow(image)
    plt.show()