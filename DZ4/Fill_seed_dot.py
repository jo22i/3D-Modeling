from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def on_click(event):
    global cid, dot
    # Обработка правой кнопки мыши, отвечающая за получение координат затравочной точки
    if event.button == 3:
        dot = [int(event.xdata), int(event.ydata)]
        plt.disconnect(cid)

def Fill(x0: int, y0: int, filler: tuple, edge_color: tuple):
    global image

    stack = []
    stack.append((x0, y0))

    while(len(stack) != 0):
        pixels = list(image.getdata())
        current_point = stack.pop(0)
        Xn, Yn = current_point[0], current_point[1]

        if ((Xn < 0 or Xn > image.width) or (Yn < 0 or Yn > image.height)): continue
        elif(pixels[image.width*Yn + Xn] == filler): continue
        elif(pixels[image.width*Yn + Xn] == edge_color): continue

        image.putpixel((Xn, Yn), filler)

        stack.append((Xn+1, Yn))
        stack.append((Xn, Yn+1))
        stack.append((Xn-1, Yn))
        stack.append((Xn, Yn-1))
        
image = Image.open("start.png")
cid = plt.connect("button_press_event", on_click)

plt.imshow(image)
plt.show()

dot = [0]*2
# dot = list(int(val) for val in input("Введите координаты затравочной точки: ").split())
# if (len(dot) != 2):
#     raise Exception("Ошибка! Получено неверное число параметров!")

filler_color = tuple(int(val) for val in input("Введите желаемый закрашиваемый цвет в формате RGB через пробелы: ").split())
if (len(filler_color) != 3):
    raise Exception("Ошибка! Получено неверное число параметров!")

edge_color = tuple(int(val) for val in input("Введите цвет границы в формате RGB через пробелы: ").split())
if ((len(edge_color)) != 3):
    raise Exception("Ошибка! Получено неверное число параметров!")

Fill(dot[0], dot[1], filler_color, edge_color)

plt.imshow(image)
plt.show()
image.save("end_img.png")
image.close()