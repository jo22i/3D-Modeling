from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def F_S(y):
    return 4*y + 6

def F_D(x, y):
    return 4*x + 4*y + 10

def Bresenham_circle(rad):
    x0, y0 = -rad, 0
    F = 1 - 2*rad

    while True:
        if(x0 == 0): break
        # Отрисовка пикселя в левой верхней полуполскости
        image.putpixel((x0+rad, y0+rad), (255, 255, 255))

        # Отрисовка пикселей в 3-х других полуплоскостях
        image.putpixel((x0+rad, -y0+rad), (255, 255, 255))
        image.putpixel((-x0+rad, y0+rad), (255, 255, 255))
        image.putpixel((-x0+rad, -y0+rad), (255, 255, 255))
        
        if(abs(x0) < abs(y0)):
            break
            # if(F < 0):
            #     F += F_S(y0)
            # else:
            #     y0 += 1
            #     F += F_D(x0, y0)
            # x0 += 1
        else:
            # Ошибка меньше нуля -> смещение по х по вертикали, y += 1
            if (F < 0):
                F += F_S(y0)
            else:
                x0 += 1
                F += F_D(x0, y0)
            y0 += 1

    return

radius = int(input("Введите радиус рисуемой окружности: "))

image = Image.new('RGB', (2*radius+1, 2*radius+1))

for x in range(0, image.width):
    for y in range(0, image.height):
        if(x%2 == y%2):
            image.putpixel((x, y), (54, 54, 54))

Bresenham_circle(radius)

image = ImageOps.flip(image)
plt.imshow(image)
plt.show()