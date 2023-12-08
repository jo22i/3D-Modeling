from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt

def Gauss(x0, y0, width, height, pix_vals):
    rgb = [0]*3

    for i in range(3):
        for X in range(x0-1, x0+1+1):
            for Y in range(y0-1, y0+1+1):
                if(X < 0 or Y < 0 or X > width or Y > height): continue

                coef = 1
                if(X == x0 and Y == y0): coef *= 4
                elif(X == x0 or Y == y0): coef *= 2

                rgb[i] += coef*pix_vals[width*Y + X][i]

        rgb[i] = int(rgb[i] / 16)
        rgb[i] = 255 if rgb[i] > 255 else rgb[i]

    # return tuple(rgb)
    return tuple([int(sum(rgb) / 3)]*3)

with Image.open("valve.png") as image:
    new_image = Image.new('RGB', (image.width, image.height))
    pixel_values = list(image.getdata())

    for x in range(0, image.width-1):
        for y in range(0, image.height-1):
            new_color = Gauss(x, y, image.width, image.height, pixel_values)
            new_image.putpixel((x, y), new_color)
    
    new_image.save("new_valve_Gauss_medium.png")

    plt.imshow(image)
    plt.show()

    plt.imshow(new_image)
    plt.show()
