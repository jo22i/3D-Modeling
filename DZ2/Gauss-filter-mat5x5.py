from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt

def Gauss(x0, y0, width, height, pix_vals):
    rgb = [0]*3

    for i in range(3):
        for X in range(x0-2, x0+2+1):
            for Y in range(y0-2, y0+2+1):
                if(X < 0 or Y < 0 or X >= width or Y >= height): continue

                coef = 1
                if(X == x0 and Y == y0): coef *= 41
                elif((Y == y0 and X == (x0-1 or x0+1)) or (X == x0 and Y == (y0-1 or y0+1))): coef *= 26
                elif((Y == y0 and X == (x0-2 or x0+2)) or (X == x0 and Y == (y0-2 or y0+2))): coef *= 7
                elif(X == (x0-1 or x0+1) or Y == (y0-1 or y0+1)):
                    if((Y == (y0-1 or y0+1)) or (X == (x0-1 or x0+1))): coef *= 16
                    else: coef *= 4

                rgb[i] += coef*pix_vals[width*Y + X][i]

        rgb[i] = int(rgb[i] / 273)
        rgb[i] = 255 if rgb[i] > 255 else rgb[i]

    return tuple(rgb)

with Image.open("valve.png") as image:
    new_image = Image.new('RGB', (image.width, image.height))
    pixel_values = list(image.getdata())

    for x in range(image.width):
        for y in range(image.height):
            new_color = Gauss(x, y, image.width, image.height, pixel_values)
            new_image.putpixel((x, y), new_color)
    
    new_image.save("new_valve_Gauss_5x5.png")

    plt.imshow(image)
    plt.show()

    plt.imshow(new_image)
    plt.show()
