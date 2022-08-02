from tkinter import *
from PIL import ImageTk, Image

root = Tk()


def get_coordinates_on_click(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

canvas = Canvas(root, width=600, height=600)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("images/dresden.jpg"))
canvas.create_image(5, 5, anchor=NW, image=img)

#root.update()

root.bind('<Button-1>', get_coordinates_on_click)


root.mainloop()
