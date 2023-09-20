from PIL import Image, ImageOps
import matplotlib.pyplot as plt

image = Image.new('RGB', (25+1, 25+1))

# Заполнение координатной плоскости серыми квадратами для лучшего визуального наблюдения
for x in range(0, image.width):
    for y in range(0, image.height):
        if((x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1)):
            image.putpixel((x, y), (54, 54, 54))
            
def Bresenham(x0, y0, x1, y1):
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
            image.putpixel((x, y_i), (255, 255, 255))
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
            image.putpixel((x_i, y), (255, 255, 255))
            error = error + 2 * delta_x
            if error >= delta_y:
                x_i += diff
                error -= 2 * delta_y

x0 = int(input("Координата x первой точки: "))
y0 = int(input("Координата y первой точки: "))
x1 = int(input("Координата x второй точки: "))
y1 = int(input("Координата y второй точки: "))
Bresenham(x0, y0, x1, y1)

# Зеркальное отражение картинки для естественного отображения координатной плоскости
image = ImageOps.flip(image)
plt.imshow(image)
plt.show()