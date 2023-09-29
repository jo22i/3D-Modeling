from PIL import Image, ImageOps
import matplotlib.pyplot as plt

image = Image.new('RGB', (13+1, 13+1))

# Заполнение координатной плоскости серыми квадратами для лучшего визуального наблюдения
for x in range(0, image.width):
    for y in range(0, image.height):
        if(x%2 == y%2):
            image.putpixel((x, y), (54, 54, 54))

def normal_vector(p_x0, p_y0, p_x1, p_y1):
    pass

def Cirus_beck(line_cords, points_cords):
    if(points_cords.count() < 6):
        print("Error! Points less than 3!")
        return -1
    
    t_params = []

    for i in range(0, len(points_cords)-1):
        pass

image = ImageOps.flip(image)
plt.imshow(image)
plt.show()