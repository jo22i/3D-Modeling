from PIL import Image
import matplotlib.pyplot as plt
from FigureManip import *
import random
import time

random.seed(time.time)


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
    # Описание векторов фигуры
    abV = tuple([(fig.dotB.x - fig.dotA.x), (fig.dotB.y - fig.dotA.y)])
    bcV = tuple([(fig.dotC.x - fig.dotB.x), (fig.dotC.y - fig.dotB.y)])
    caV = tuple([(fig.dotA.x - fig.dotC.x), (fig.dotA.y - fig.dotC.y)])

    # Описание нормалей векторов фигуры
    Nab = tuple([abV[1], -abV[0]])
    Nbc = tuple([bcV[1], -bcV[0]])
    Nca = tuple([caV[1], -caV[0]])

    # Описание векторов от точек фигуры до исходной точки
    atV = tuple([xi - abV[0], yi - abV[1]])
    btV = tuple([xi - bcV[0], yi - bcV[1]])
    ctV = tuple([xi - caV[0], yi - caV[1]])

    # Проверка на принадлежность исходной точки данной фигуре
    if ((Nab[0]*atV[0] + Nab[1]+atV[1] >= 0) and 
        (Nbc[0]*btV[0] + Nbc[1]*btV[1] >= 0) and 
        (Nca[0]*ctV[0] + Nca[1]+ctV[1] >= 0)): return True

    return False


dots = []
figures = []

with open(input("Введите полный путь к файлу: ")) as file:
    info = file.read().split('\n')

    # TO DO: Найти как экспортировать цвет каждого полигона в формате RGB
    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            dots.append( list(float(dot) for dot in line) )
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )

with Image.new("RGB", (100, 100)) as image:
    for i in range(len(dots)):
        dots[i] = ChangeVector(get_scale_matrix(30, 30, 30), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_Z(30), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_rotate_matrix_X(70), get_vector(dots[i]))[:-1]
        dots[i] = ChangeVector(get_move_matrix(50, 50), get_vector(dots[i]))[:-1]
        dots[i] = dot(int(dots[i][0]), int(dots[i][1]), int(dots[i][2]))

    for i in range(len(figures)):
        # TO DO: Понять как подвязать цвет из TO DO выше
        figures[i] = figure(dots[figures[i][0]-1], dots[figures[i][1]-1],
                            dots[figures[i][2]-1],
                            tuple([random.randrange(255+1), random.randrange(255+1), random.randrange(255+1)]))
        # fig = figures[i]
        # for j in range(-1, len(fig)-1):
        #     Bresenham(int(dots[fig[j]-1][0]), int(dots[fig[j]-1][1]), int(dots[fig[j+1]-1][0]), int(dots[fig[j+1]-1][1]))


    # Z-буфер с доступом к элементам по схеме [y*width + x]
    Zbuff = [None]*image.width*image.height
    for X in range(image.width):
        for Y in range(image.height):
            for i in range(len(figures)):
                if (is_in_figure(X, Y, figures[i])): 
                    if (Zbuff[image.width*Y + X] is None or Zbuff[image.width*Y + X].z < figures[i].z):
                        Zbuff[image.width*Y + X] = figures[i]

    for i in range(len(Zbuff)):
        if Zbuff[i] is not None:
            image.putpixel((Zbuff[i].x, Zbuff[i].y), Zbuff[i].colour)

    plt.imshow(image)
    plt.show()