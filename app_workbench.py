from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

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

class FreeDraw:
    
    def __init__(self, points=[]):
        self.points = points

    def get_point(self,ponto=Point()):   
        self.points.append(ponto)
    
def get_coordinates_for_rectangle(event):
    x, y = event.x, event.y
    point = Point(x,y)
    #print(x,y)
    if len(newRec.points)<3:
        newRec.get_point(point)
        print(x,y)
    else:
        newRec.get_point(point)
        print(x,y)
        print('4 points were already selected')
        root.unbind('<Button-1>')
        #Em vez de  unbind, usar hover como event

def draw_rectangle(event):
    
    canvas.create_line(newRec.points[0].x, newRec.points[0].y, newRec.points[3].x, newRec.points[3].y)
    
    for i in range(3):
        canvas.create_line(newRec.points[i].x, newRec.points[i].y, newRec.points[i+1].x, newRec.points[i+1].y)

    #testar canvas.create_polygon

def call_free_draw(event):
    root.bind('<Motion>',free_draw)

def free_draw(event):
    x, y = event.x, event.y
    ponto = Point(x,y)
    print(x,y)
    if len(newDraw.points)==0 or x != newDraw.points[-1].x and y != newDraw.points[-1].y:
        newDraw.get_point(ponto)
    if len(newDraw.points)>1:
        canvas.create_line(newDraw.points[-2].x, newDraw.points[-2].y, newDraw.points[-1].x, newDraw.points[-1].y)

# Cria a interface gráfica
root = Tk()
root.geometry("1000x500")

# Importa a amagem, altera o tamanho e carrega na interface gráifca
picture = Image.open("images/lesao1.jpeg")  

img_tk = ImageTk.PhotoImage(picture)

picture_w, picture_h = picture.size

picture_w_resized, picture_h_resized = int(picture_w/5), int(picture_w/5)

resized_image= picture.resize((picture_w_resized, picture_h_resized),resample=Image.Resampling.LANCZOS)

new_resized_image= ImageTk.PhotoImage(resized_image)


# Cria o container para a imagem e insere
img_container = Frame(root,width=600, height=400)

img_container.pack(side=LEFT, padx=10,pady=10)

canvas = Canvas(img_container, width=picture_w_resized, height=picture_h_resized)

canvas.create_image(0, 0, anchor=NW, image=new_resized_image)

canvas.pack()

#img_container.place(anchor='e', relx=0.5, rely=0.5)
#label = Label(img_container, image = canvas)
#label.pack()

newRec = Rectangle()
newDraw = FreeDraw()

button = ttk.Button(root,text ='Select Points', command=lambda: root.bind('<Button-1>', get_coordinates_for_rectangle))

button2 = ttk.Button(root,text ='Draw Rectangle', command=lambda: root.unbind('<Button-1>'))

button2.bind('<Button>', draw_rectangle)

button3 = ttk.Button(root,text ='Test Spline', command=lambda: root.bind('<Double-Button>', call_free_draw))
button3.pack()


#button2.bindtags(['Meu botao 1'])

button.pack()

button2.pack()



#print('\n',button2.bindtags())

root.mainloop()

#print(f'As coordendas do segundo ponto são {newRec.points[1].x} e {newRec.points[1].y}')

print(newDraw.points[2].x)