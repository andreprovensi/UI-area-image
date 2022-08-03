from tkinter import *
from tkinter import ttk
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
button = ttk.Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)

button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)
root.bind('<Button-1>', get_coordinates_on_click)


root.mainloop()

for i in range(4):
    print(i)