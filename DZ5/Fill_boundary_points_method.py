from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def on_click(event):
    global cid, points

    # Левая кнопка мыши - построение многоугольника (Обязательно последовательно)
    if event.button == 1:
        points.append((int(event.xdata), int(event.ydata)))

def Bresenham(x0: int, y0: int, x1: int, y1: int, color: tuple = (255, 255, 255)):
    global image
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    error = 0
    diff = 1

    # Смена координат в случае, если начальная координата дальше по оси х, чем конечная
    if(x0 - x1 > 0):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Проверка на убывание
    if(y0 - y1 > 0):
        diff = -1

    # Если угол меньше или равно 45, то увеличиваем/уменьшаем координату y
    if(delta_x >= delta_y):
        y_i = y0
        for x in range(x0, x1 + 1):
            image.putpixel((x, y_i), color)
            error = error + 2 * delta_y
            if error >= delta_x:
                y_i += diff
                error -= 2 * delta_x
    # Иначе - по координате x
    elif(delta_x < delta_y):
        # Обработка особого случая
        if(diff == -1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        x_i = x0
        for y in range(y0, y1 + 1):
            image.putpixel((x_i, y), color)
            error = error + 2 * delta_x
            if error >= delta_y:
                x_i += diff
                error -= 2 * delta_y

def Fill_BPM(begin: int, end: int, filler_color: tuple):
    global sides

    for Y in range(begin, end+1):
        current_layer = []

        for side in sides:
            # Проверка на прересечение
            if min(side[0][1], side[1][1]) <= Y <= max(side[0][1], side[1][1])+1:
                X = round( side[0][0] + (((Y - side[0][1]) * (side[1][0] - side[0][0])) / (side[1][1] - side[0][1])) )
                current_layer.append((X, Y))
        
        current_layer.sort()

        for i in range(0, len(current_layer), 2):
            if (i + 1 == len(current_layer)): continue
            for X in range(current_layer[i][0], current_layer[i+1][0]+1):
                image.putpixel((X, Y), filler_color)


points = []
sides = []

with Image.new("RGB", (10, 10)) as image:
    cid = plt.connect("button_press_event", on_click)

    for x in range(0, image.width):
        for y in range(0, image.height):
            if (x%2 == y%2): image.putpixel((x, y), (54, 54, 54))

    plt.imshow(image)
    plt.show()

    filler_color = tuple(int(val) for val in input("Введите цвет заполнения в формате <RRR GGG BBB>: ").strip().split())

    y_begin, y_end = image.height, 0

    for i in range(-1, len(points)-1):
        if (points[i][1] != points[i+1][1]):
            sides.append(((points[i][0], points[i][1]), (points[i+1][0], points[i+1][1])))
        y_begin = min(y_begin, points[i][1])
        y_end = max(y_end, points[i][0])

    Fill_BPM(y_begin, y_end, filler_color)

    for i in range(len(sides)):
        Bresenham(sides[i][0][0], sides[i][0][1], sides[i][1][0], sides[i][1][1], filler_color)

    plt.imshow(image)
    plt.show()
