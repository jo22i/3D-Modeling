from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from Bresenham import Bresenham


class dot:
    def __init__(self, cordX: float, cordY: float):
        self.x = cordX
        self.y = cordY


class side:
    def __init__(self, dotA: dot, dotB: dot):
        self.A = dotA
        self.B = dotB


def on_click(event):
    global cid, points

    # Левая кнопка мыши - построение многоугольника (Обязательно последовательно)
    if event.button == 1:
        points.append(dot(int(event.xdata), int(event.ydata)))


# def Fill_BPM(begin: int, end: int, filler_color: tuple):
#     global sides

#     for Y in range(begin, end+1):
#         current_layer = []

#         for side in sides:
#             # Проверка на прересечение
#             if min(side[0][1], side[1][1]) <= Y <= max(side[0][1], side[1][1])+1:
#                 X = round( side[0][0] + (((Y - side[0][1]) * (side[1][0] - side[0][0])) / (side[1][1] - side[0][1])) )
#                 current_layer.append((X, Y))
        
#         current_layer.sort()

#         for i in range(0, len(current_layer), 2):
#             if (i+1 == len(current_layer)): break
#             for X in range(current_layer[i][0], current_layer[i+1][0]):
#                 image.putpixel((X, Y), filler_color)

def Fill_BPM(begin: int, end: int, filler_color: tuple):
    global sides, image

    for Y in range(begin, end+1):
        current_layer_x = []

        for side in sides:
            if min(side.A.y, side.B.y) < Y <= max(side.A.y, side.B.y):
                x1, x2 = side.A.x, side.B.x
                y1, y2 = side.A.y, side.B.y
                xi = Y*((x2 - x1) / (y2 - y1)) - y1*((x2 - x1) / (y2 - y1)) + x1
                current_layer_x.append(xi)

        current_layer_x.sort()

        for i in range(0, len(current_layer_x), 2):
            if i + 1 == len(current_layer_x): break
            Bresenham(image, round(current_layer_x[i]), Y, round(current_layer_x[i+1]), Y, filler_color)



points = []
sides = []

with Image.new("RGB", (25, 25)) as image:
    cid = plt.connect("button_press_event", on_click)

    for x in range(0, image.width):
        for y in range(0, image.height):
            if (x%2 == y%2): image.putpixel((x, y), (54, 54, 54))

    plt.imshow(image)
    plt.show()

    filler_color = tuple(int(val) for val in input("Введите цвет заполнения в формате <RRR GGG BBB>: ").strip().split())

    y_begin, y_end = image.height, 0

    for i in range(-1, len(points)-1):
        sides.append(side(points[i], points[i+1]))
        y_begin = int(min(y_begin, points[i].y, points[i+1].y))
        y_end = int(max(y_end, points[i].y, points[i+1].y))

    Fill_BPM(y_begin, y_end, filler_color)

    for i in range(len(sides)):
        Bresenham(image, sides[i].A.x, sides[i].A.y, sides[i].B.x, sides[i].B.y)

    plt.imshow(image)
    plt.show()
