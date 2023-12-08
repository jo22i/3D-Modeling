from PIL import Image
import matplotlib.pyplot as plt
from DotManip import *
import random, time

random.seed(time.time())

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
        coefD = -self.dotA.x*coefA - self.dotA.y*coefB - self.dotA.z*coefC

        return (-coefA*xi - coefB*yi - coefD)/coefC

    def in_figure(self, xt: int, yt: int):
        # Проверка будет производиться для обоих обходов
        # Описание векторов фигуры
        abV = tuple([(self.dotB.x - self.dotA.x), (self.dotB.y - self.dotA.y)])
        bcV = tuple([(self.dotC.x - self.dotB.x), (self.dotC.y - self.dotB.y)])
        caV = tuple([(self.dotA.x - self.dotC.x), (self.dotA.y - self.dotC.y)])

        # Описание нормалей векторов фигуры
        Nab = tuple([abV[1], -abV[0]])
        Nbc = tuple([bcV[1], -bcV[0]])
        Nca = tuple([caV[1], -caV[0]])

        # Описание векторов от точек фигуры до исходной точки
        atV = tuple([xt - self.dotA.x, yt - self.dotA.y])
        btV = tuple([xt - self.dotB.x, yt - self.dotB.y])
        ctV = tuple([xt - self.dotC.x, yt - self.dotC.y])

        # Проверка на принадлежность исходной точки данной фигуре
        if ((
            (Nab[0]*atV[0] + Nab[1]*atV[1] >= 0) and 
            (Nbc[0]*btV[0] + Nbc[1]*btV[1] >= 0) and 
            (Nca[0]*ctV[0] + Nca[1]*ctV[1] >= 0)
            )

            or

            (
            (Nab[0]*atV[0] + Nab[1]*atV[1] < 0) and 
            (Nbc[0]*btV[0] + Nbc[1]*btV[1] < 0) and 
            (Nca[0]*ctV[0] + Nca[1]*ctV[1] < 0)
            )):
            
            return True

        return False

    def is_visible(self):
        # A = (yb-ya)*(zc-za) - (zb-za)*(yc-ya)
        # B = (xc-xa)*(zb-za) - (xb-xa)*(zc-za)
        # C = (xb-xa)*(yc-ya) - (yb-ya)*(xc-xa)
        C = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)

        if (C < 0): return False

        return True
    

dots = []
figures = []

xmin, xmax = 100, 0
ymin, ymax = 100, 0

with open(input("Введите полный путь к файлу: ")) as file:
    info = file.read().split('\n')

    # TO DO: Найти как экспортировать цвет каждого полигона в формате RGB
    for line in info:
        if (line.find("v") == 0):
            _, *line = line.split()
            line = list(float(dot) for dot in line)
            dots.append( dot(line[0], line[1], line[2]))
        elif (line.find("f") == 0):
            _, *line = line.split()
            figures.append( list(int(fig) for fig in line) )

with Image.new("RGB", (26, 26)) as image:
    for x in range(0, image.width):
        for y in range(0, image.height):
            if(x%2 == y%2):
                image.putpixel((x, y), (54, 54, 54))

    for i in range(len(dots)):
        dots[i] = ChangeDot(get_scale_matrix(15, 15, 15), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_Z(35), get_vector(dots[i]))
        dots[i] = ChangeDot(get_rotate_matrix_X(55), get_vector(dots[i]))
        dots[i] = ChangeDot(get_move_matrix(13, 13), get_vector(dots[i]))
        xmin = int(min(xmin, dots[i].x))
        xmax = int(max(xmax, dots[i].x))
        ymin = int(min(ymin, dots[i].y))
        ymax = int(max(ymax, dots[i].y))

    for i in range(len(figures)):
        fig = figure(dots[figures[i][0]-1], dots[figures[i][1]-1], dots[figures[i][2]-1], tuple([random.randrange(255+1), random.randrange(255+1), random.randrange(255+1)]))
        if fig.is_visible():
            figures[i] = fig
            print(str(i) + " = " + str(figures[i].colour))
        else:
            figures[i] = None
    
    # Проход по всей плоскости и вычисление видимой части фигуры
    for X in range(xmin, xmax+1):
        for Y in range(ymin, ymax+1):
            current_fig = None
            for i in range(len(figures)):
                if figures[i] is not None and figures[i].in_figure(X, Y):
                    if ((current_fig is None) or (current_fig.getZ(X, Y) < figures[i].getZ(X, Y))):
                        current_fig = figures[i]

            if current_fig is not None:
                image.putpixel((X, Y), current_fig.colour)

    plt.imshow(image)
    plt.show()