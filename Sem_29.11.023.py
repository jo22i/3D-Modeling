from PIL import Image
import matplotlib.pyplot as plt
from FigureManip import *
from math import sqrt

dots = []
figures = []

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

    def zCoord(self, xi: int, yi: int):
        coefA = (self.dotB.y - self.dotA.y)*(self.dotC.z - self.dotA.z) - (self.dotB.z - self.dotA.z)*(self.dotC.y - self.dotA.y)
        coefB = (self.dotB.z - self.dotA.z)*(self.dotC.x - self.dotA.x) - (self.dotB.x - self.dotA.x)*(self.dotC.z - self.dotA.z)
        coefC = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)
        coefD = -self.dotA.x*coefA + self.dotA.y*coefB - self.dotA.z*coefC

        return (-coefA*xi - coefB*yi - coefD)/coefC

    def isIn(self, xt: int, yt: int):
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
        atV = tuple([xt - abV[0], yt - abV[1]])
        btV = tuple([xt - bcV[0], yt - bcV[1]])
        ctV = tuple([xt - caV[0], yt - caV[1]])

        # Проверка на принадлежность исходной точки данной фигуре
        if ((Nab[0]*atV[0] + Nab[1]+atV[1] >= 0) and 
            (Nbc[0]*btV[0] + Nbc[1]*btV[1] >= 0) and 
            (Nca[0]*ctV[0] + Nca[1]+ctV[1] >= 0)): return True

        return False

    def is_visible(self):
        # A = (yb-ya)*(zc-za) - (zb-za)*(yc-ya)
        # B = (xc-xa)*(zb-za) - (xb-xa)*(zc-za)
        # C = (xb-xa)*(yc-ya) - (yb-ya)*(xc-xa)
        C = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)

        if (C < 0): return False

        return True
    
    def getNormal(self):
        coefA = (self.dotB.y - self.dotA.y)*(self.dotC.z - self.dotA.z) - (self.dotB.z - self.dotA.z)*(self.dotC.y - self.dotA.y)
        coefB = (self.dotB.z - self.dotA.z)*(self.dotC.x - self.dotA.x) - (self.dotB.x - self.dotA.x)*(self.dotC.z - self.dotA.z)
        coefC = (self.dotB.x - self.dotA.x)*(self.dotC.y - self.dotA.y) - (self.dotB.y - self.dotA.y)*(self.dotC.x - self.dotA.x)
        
        return dot(coefA, coefB, coefC)

def lightFactor(F: figure, P: dot, L: dot):
    N = F.getNormal()

    LP = sqrt((P.x - L.x)**2 + (P.y - L.y)**2 + (P.z - L.z)**2)
    NP = sqrt((N.x)**2 + (N.y)**2 + (N.z)**2)
    vec_prod = (L.x - P.x)*(N.x) + (L.y - P.y)*(N.y) + (L.z - P.z)*(N.z)

    # IL = vec_prod / (NP * LP)
    return abs(vec_prod / (NP * LP))


A = dot(7, 4, 3)
B = dot(19, 7, 5)
C = dot(9, 0, 2)

L = dot(10, 10, 20)

F = figure(A, B, C, (255, 0, 0))

with Image.new("RGB", (100, 100)) as image:
    for X in range(image.height):
        for Y in range(image.width):
            if F.isIn(X, Y):
                Z = F.zCoord(X, Y)
                I = lightFactor(F, dot(X, Y, Z), L)
                # new_colour = 
                image.putpixel((X, Y), tuple( [int(C*I) for C in F.colour] ) )

    plt.imshow(image)
    plt.show()