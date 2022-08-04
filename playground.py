from tkinter import *
from tkinter import ttk
from urllib.request import AbstractDigestAuthHandler
from PIL import ImageTk, Image

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Rectangle:

    def __init__(self, points=[]):
        self.points = points
        
    def get_point(self,ponto=Point()):

        if len(self.points) < 4:
            self.points.append(ponto)
        else:
            pass  

def get_coordinates_for_rectangle(event):
    
    if len(newRec.points)<4:
        x, y = event.x, event.y
        point = Point(x,y)
        newRec.get_point(point)
        print(x,y)
    else:
        print('4 points were already selected')
        root.unbind('<Button-1>')

def create_rectangle(root):
    
    if len(newRec.points)>4:

        root.unbind('<Button>')
    
    #elif len(newRec.points)<3:
    else:
        root.bind('<Button-1>', get_coordinates_for_rectangle)
    


def draw_rectangle(event):
    
    canvas.create_line(newRec.points[0].x, newRec.points[0].y, newRec.points[3].x, newRec.points[3].y)
    
    for i in range(3):
        canvas.create_line(newRec.points[i].x, newRec.points[i].y, newRec.points[i+1].x, newRec.points[i+1].y)


root = Tk()

canvas = Canvas(root, width=600, height=600)

canvas.pack()

picture = Image.open("images/dresden.jpg")

picture_RGB = picture.convert('RGB')

img_tk = ImageTk.PhotoImage(picture)

canvas.create_image(5, 5, anchor=NW, image=img_tk)

newRec = Rectangle()

button = ttk.Button(root,text ='Select Points', command=lambda: root.bind('<Button-1>', get_coordinates_for_rectangle))
button2 = ttk.Button(root,text ='Draw Rectangle', command=lambda: root.unbind('<Button-1>'))
#button3 = ttk.Button(root, text='Draw Rectangle')

#button.bind('<Button>', create_rectangle)
#button.bind('<Return>', lambda: root.unbind('<Button-1>', get_coordinates_for_rectangle), add='+')
button2.bind('<Button>', draw_rectangle)

button.pack()
button2.pack()
#button3.pack()


#root.update()
root.mainloop()

print(f'As coordendas do segundo ponto são {newRec.points[1].x} e {newRec.points[1].y}')