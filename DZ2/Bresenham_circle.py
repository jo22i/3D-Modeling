from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def Bresenham_circle(rad):
    #smth
    return

radius = int(input("Введите радиус рисуемой окружности: "))

image = Image.new('RGB', (radius+5+1, radius+5+1))

for x in range(0, image.width):
    for y in range(0, image.height):
        if((x%2 == 0 and y%2 == 0) or (x%2 == 1 and y%2 == 1)):
            image.putpixel((x, y), (54, 54, 54))

Bresenham_circle(radius)

image = ImageOps.flip(image)
plt.imshow(image)
plt.show()