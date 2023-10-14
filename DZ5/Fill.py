from PIL import Image, ImageOps
import matplotlib.pyplot as plt

def on_click(event):
    # Обработка левой кнопки мыши, отвечающая за получение координат многоугольника
    if event.button == 1:
        polygon_axes.append([round(event.xdata), round(event.ydata)])

    # Обработка правой кнопки мыши, отвечающая за получение координат затравочной точки
    elif event.button == 3:
        dot = [round(event.xdata), round(event.ydata)]
        plt.disconnect(cid)

polygon_axes = []
image = Image.new('RGB', (100, 100))
image = ImageOps.flip(image)
cid = plt.connect("button_press_event", on_click)
plt.imshow(image)
plt.show()