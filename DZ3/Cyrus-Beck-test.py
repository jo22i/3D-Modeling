from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from Bresenham import Bresenham


# Функция обработки кнопок мыши, отключается как только пользователь введёт координаты отрезка
def on_click(event):
    global polygon_axes, dots_axes, cid

    # Обработка левой кнопки мыши, отвечающая за получение координат многоугольника
    if event.button == 1:
        # image.putpixel((round(event.xdata), round(event.ydata)), (255, 0, 0))
        polygon_axes.append([int(event.xdata), int(event.ydata)])

    # Обработка правой кнопки мыши, отвечающая за получение координат отрезка
    elif event.button == 3:
        # image.putpixel((round(event.xdata), round(event.ydata)), (0, 255, 0))
        # Получение координат первой точки
        if(dots_axes[0][0] == None):
            dots_axes[0][0], dots_axes[0][1] = int(event.xdata), int(event.ydata)
        # Получение координаты второй точки, окончание обработки событий мыши
        else:
            dots_axes[1][0], dots_axes[1][1] = int(event.xdata), int(event.ydata)
            plt.disconnect(cid)


def Cyrus_Beck():
    global dots_axes, polygon_axes

    t_begin, t_end = 0, 1
    AB_vector = [(dots_axes[1][0] - dots_axes[0][0]), (dots_axes[1][1] - dots_axes[0][1])]

    # Обход вершин будет осуществляться по часовой стрелке
    for i in range(-1, len(polygon_axes)-1):
        # xN = (polygon_axes[i+1][0] - polygon_axes[i][0])
        # yN = (polygon_axes[i+1][1] - polygon_axes[i][1])
        normal = [ -(polygon_axes[i+1][1] - polygon_axes[i][1]), (polygon_axes[i+1][0] - polygon_axes[i][0]) ]

        # TO DO: продолжить расчёты
        pass

    pass


polygon_axes = []
# [[xA, yA],
#   xB, yB]]
dots_axes = [[None]*2]*2

with Image.new('RGB', (50, 50)) as image:
    image = ImageOps.flip(image)
    cid = plt.connect("button_press_event", on_click)

    # Заполнение координатной плоскости серыми квадратами для лучшего визуального наблюдения
    for x in range(0, image.width):
        for y in range(0, image.height):
            if(x%2 == y%2):
                image.putpixel((x, y), (54, 54, 54))

    plt.imshow(image)
    plt.show()

    # Прорисовка изначального положения прямой
    Bresenham(image, dots_axes[0], dots_axes[1], dots_axes[2], dots_axes[3], (255, 0, 0))

    # Прорисовка многоугольника
    for i in range(-1, len(polygon_axes)-1):
        Bresenham(polygon_axes[i][0], polygon_axes[i][1], polygon_axes[i+1][0], polygon_axes[i+1][1], (0, 0, 255))

    fklal

    plt.imshow(image)
    plt.show()