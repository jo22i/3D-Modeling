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
        if(len(dots_axes) == 0):
            dots_axes.append([int(event.xdata), int(event.ydata)])
        # Получение координаты второй точки, окончание обработки событий мыши
        else:
            dots_axes.append([int(event.xdata), int(event.ydata)])
            plt.disconnect(cid)


def Cyrus_Beck():
    global dots_axes, polygon_axes

    edited = False
    t_begin, t_end = 0, 1
    AB_vector = [(dots_axes[1][0] - dots_axes[0][0]), (dots_axes[1][1] - dots_axes[0][1])]

    # Обход вершин будет осуществляться по часовой стрелке
    for i in range(-1, len(polygon_axes)-1):
        # xN = (polygon_axes[i+1][0] - polygon_axes[i][0])
        # yN = (polygon_axes[i+1][1] - polygon_axes[i][1])
        normal = [ -(polygon_axes[i+1][1] - polygon_axes[i][1]), (polygon_axes[i+1][0] - polygon_axes[i][0]) ]

        Api_vector = [ (dots_axes[0][0] - polygon_axes[i][0]), (dots_axes[0][1] - polygon_axes[i][1]) ]

        # Скалярное произведение внутренней нормали отрезка и вектора прямой позволят определить
        # как входит прямая в данную сторону: снаружи внутрь или изнутри в наружу
        # Если данный параметр равен нулю, то значит что прямая параллельна данному отрезку
        # и есть 2 возможных варианта:
        # 1) Если прямая лежит внутри фигуры
        # 2) Прямая лежит снаружи фигуры
        Pi = normal[0]*AB_vector[0] + normal[1]*AB_vector[1]

        # Скалярное произведение вектора A_pi на нормаль отрезка, позволяет определить положение прямой
        # относительно отрезка в случае параллельного расположения
        # Если Qi < 0, то это значит что отрезок находится вне фигуры и дальнейшие вычисления не нужны
        Qi = normal[0]*Api_vector[0] + normal[1]*Api_vector[1]

        if Pi == 0:
            if Qi < 0: return None
            continue

        # Вычисляем параметр t. Если он не лежит в промежутке от 0 до 1, то точка пересечения - мнимая
        t = -Qi / Pi

        if not 0 <= t <= 1: continue

        # Если скалярное произведение вектора нормали и вектора отрезка положительно, то
        # вектор входит внутрь фигуры
        # поэтому считаем начальную точку пересечения
        # Иначе отрезок выходит из фигуры и мы считаем конечную точку пересечения
        if Pi > 0:
            t_begin = max(t_begin, t)
        else:
            t_end = min(t_end, t)
    
    return t_begin, t_end


def get_cords(T: float):
    X = int(dots_axes[1][0] * T + (1 - T) * dots_axes[0][0])
    Y = int(dots_axes[1][1] * T + (1 - T) * dots_axes[0][1])
    return X, Y


# [[xA, yA],
#   xB, yB]]
polygon_axes = []
dots_axes = []

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
    Bresenham(image, dots_axes[0][0], dots_axes[0][1], dots_axes[1][0], dots_axes[1][1], (255, 0, 0))

    # Прорисовка многоугольника
    for i in range(-1, len(polygon_axes)-1):
        Bresenham(image, polygon_axes[i][0], polygon_axes[i][1], polygon_axes[i+1][0], polygon_axes[i+1][1], (0, 0, 255))

    answer = Cyrus_Beck()

    if answer is not None:
        if answer[1] < answer[0]:
            print("Отрезок вне окна")
        else:
            x_begin, y_begin, x_end, y_end = 0, 0, 0, 0
            if answer[0] == 0:
                x_begin, y_begin = dots_axes[0][0], dots_axes[0][1]
            else:
                x_begin, y_begin = get_cords(answer[0])
            
            if answer[1] == 1:
                x_end, y_end = dots_axes[1][0], dots_axes[1][1]
            else:
                x_end, y_end = get_cords(answer[1])

            Bresenham(image, x_begin, y_begin, x_end, y_end, (255, 255, 255))        

    plt.imshow(image)
    plt.show()