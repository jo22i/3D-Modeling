from PIL import Image
import matplotlib.pyplot as plt
from math import sqrt

def Sobel_Operator(x0, y0, width, height, pix_list):
    Sx = [0]*3
    Sy = [0]*3
    rgb = [0]*3
    
    for i in range(3):
        if(x0 == y0 == 0):
            Sx[i] += pix_list[width*(y0+1) + x0+1][i] + 2*pix_list[width*y0 + x0+1][i]
            Sy[i] -= 2*pix_list[width*(y0+1) + x0][i] + pix_list[width*(y0+1) + x0+1][i]
        elif(x0 == 0 and y0 == height):
            Sx[i] += 2*pix_list[width*y0 + x0+1][i] + pix_list[width*(y0-1) + x0+1][i]
            Sy[i] += 2*pix_list[width*(y0-1) + x0][i] + pix_list[width*(y0-1) + x0+1][i]
        elif(x0 == width and y0 == 0):
            Sx[i] -= pix_list[width*(y0+1) + x0-1][i] + 2*pix_list[width*y0 + x0-1][i]
            Sy[i] -= pix_list[width*(y0+1) + x0-1][i] + 2*pix_list[width*(y0+1) + x0][i]
        elif(x0 == width and y0 == height):
            Sx[i] -= 2*pix_list[width*y0 + x0-1][i] + pix_list[width*(y0-1) + x0-1][i]
            Sy[i] += pix_list[width*(y0-1) + x0-1][i] + 2*pix_list[width*(y0-1) + x0][i]
        else:
            for Y in range(y0-1, y0+2):
                if(Y < 0 or Y >= height):
                    continue
                coef = 2 if (Y == y0) else 1
                Sx[i] += coef*(pix_list[width*Y + x0+1][i] - pix_list[width*Y + x0-1][i])

            for X in range(x0-1, x0+2):
                if(X < 0 or X >= width):
                    continue
                coef = 2 if (X == x0) else 1
                Sy[i] += coef*(pix_list[width*(y0-1) + X][i] - pix_list[width*(y0+1) + X][i])


    for i in range(3):
        rgb[i] += int(sqrt(Sx[i]*Sx[i] + Sy[i]*Sy[i]))
        rgb[i] = 255 if(rgb[i] >= 255) else rgb[i]

    #return tuple(Cij)
    return tuple( [ int( sum(rgb) / 3 ) ]*3 )


with Image.open("valve.png") as image:
    new_image = Image.new('RGB', (image.width, image.height))
    pixel_values = list(image.getdata())

    for x in range(0, image.width-1):
        for y in range(0, image.height-1):
            new_color = Sobel_Operator(x, y, image.width, image.height, pixel_values)
            new_image.putpixel((x, y), new_color)
    
    new_image.save("new_valve_medium.png")

    plt.imshow(image)
    plt.show()

    plt.imshow(new_image)
    plt.show()