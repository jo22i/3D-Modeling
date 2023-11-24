from typing import Any
from PIL import Image
import matplotlib.pyplot as plt
from FigureManip import *
import random, time

random.seed(time.time)


class dot:
    def __init__(self, cordX: float, cordY: float, cordZ: float):
        self.x = cordX
        self.y = cordY
        self.z = cordZ


class figure:
    def __init__(self, dotA: dot, dotB: dot, dotC: dot, colour: tuple):
        self.dotA = dotA
        self.dotB = dotB
        self.dotC = dotC
        self.colour = colour
        
    def getZ(self, xi: int, yi: int):
        # Ax + By + Cz + D = 0
        coefA = (self.dotB.y - self.dotA.y)*(self.dotC.z - self.dotA.z) - (self.dotB.z - self.dotA.z)*(self.dotC.y - self.dotA.y)
        coefB = (self.dotB.z - self.dotA.z)*(self.dotC.x - self.dotA.x) - (self.dotB.x - self.dotA.x)*(self.dotC.z - self.dotA.z)
        coefC = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)
        coefD = -self.dotA.x*coefA + self.dotA.y*coefB - self.dotA.z*coefC

        return (-coefA*xi - coefB*yi - coefD)/coefC

    def in_figure(self, xi: int, yi: int):
        # Обход вершин идёт по часовой стрелке (стандарт Blender)
        # Описание векторов фигуры
        abV = tuple([(self.dotB.x - self.dotA.x), (self.dotB.y - self.dotA.y)])
        bcV = tuple([(self.dotC.x - self.dotB.x), (self.dotC.y - self.dotB.y)])
        caV = tuple([(self.dotA.x - self.dotC.x), (self.dotA.y - self.dotC.y)])

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
        figures[i] = figure(dots[figures[i][0]-1], dots[figures[i][1]-1],
                            dots[figures[i][2]-1],
                            tuple([random.randrange(255+1), random.randrange(255+1), random.randrange(255+1)]))
        print(str(i) + " = " + str(figures[i].colour))

    # Проход по всей плоскости и вычисление видимой части фигуры
    for X in range(image.width):
        for Y in range(image.height):
            current_fig = None
            for i in range(len(figures)):
                if figures[i].in_figure(X, Y):
                    if (current_fig is None or current_fig.getZ(X, Y) < figures[i].getZ(X, Y)):
                        current_fig = figures[i]

            if current_fig is not None:
                image.putpixel((X, Y), current_fig.colour)

    plt.imshow(image)
    plt.show()