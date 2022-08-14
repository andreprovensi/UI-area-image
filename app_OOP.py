from distutils.cmd import Command
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter.filedialog import askopenfilename
from typing import final
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

class Imagem:
    def __init__(self):
        self.file = None
        self.img = None
        self.src_img = None

class FreeDraw:
    def __init__(self, points=[]):
        self.points = points

    def get_point(self,ponto=Point()):   
        self.points.append(ponto)

    def reset_points(self):
        self.points = []
    
    def closing_points_free_draw(self):
        
        if len(self.points)>1:
            final_point = self.points[-1]
            initial_point = self.points[0]

            delta_x = initial_point.x - final_point.x
            delta_y = initial_point.y - final_point.y

            if delta_x > 0:
                x_dir = 1
            elif delta_x < 0:
                x_dir = -1
            elif delta_x == 0:
                x_dir = 0

            if delta_y > 0:
                y_dir = 1
            elif delta_y < 0:
                y_dir = -1
            elif delta_y == 0:
                y_dir = 0

            points_list = []

            for i in range(1,abs(delta_x)+1):
                ponto = Point(final_point.x+i*x_dir,final_point.y)
                points_list.append(ponto)
            for j in range(1,abs(delta_y)+1):
                ponto = Point(initial_point.x,initial_point.y-j*y_dir)
                points_list.append(ponto)
            
            for k in points_list:
                self.get_point(k)

        else:
            pass


    def calcula_area(self):
        if len(self.points)>2:
            pass

class App:
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1000x500")

        self.imagem = Imagem()

        self.freeDraw = FreeDraw()

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar,padx=1,pady=1)
        self.file_menu = Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=lambda: self.open_image())
        self.file_menu.add_command(label="Exit", command=lambda: self.root.quit())

        self.frame = Frame(self.root)

        self.frame_buttons = Frame(self.root,relief=RAISED,borderwidth=3)
        self.frame_buttons.pack(side=tkinter.RIGHT,fill=BOTH,expand=False)

        self.canvas = Canvas(self.frame)

        self.slider = ttk.Scale(self.frame_buttons,from_=1, to=100, orient='horizontal', command = lambda event: self.render_image())
        self.slider.set(30)
        
        self.button_free_draw = ttk.Button(
            self.frame_buttons, text ='Free Draw', 
            command = lambda: [self.freeDraw.reset_points(),self.root.bind('<Double-Button>', lambda event: self.root.bind('<Motion>',free_draw))]
        )

        #self.button_free_draw.pack(anchor='ne',padx=1,pady=1)
        self.button_free_draw.pack(side=tkinter.TOP,pady=25)
        self.slider.pack(side=tkinter.TOP,padx=1,pady=15)

        def free_draw(event):
            
            self.root.bind('<Double-Button>', lambda event: [self.root.unbind('<Motion>'),self.freeDraw.closing_points_free_draw(),self.close_free_draw()]) 

            x, y = event.x, event.y
            ponto = Point(x,y)

            print(x,y)
            self.freeDraw.get_point(ponto)
    
            if len(self.freeDraw.points)>1:
                self.canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y)

    def open_image(self):

        #self.root.update()

        self.imagem.file = askopenfilename(filetypes=[("all files","*"),("Bitmap Files","*.bmp; *.dib"), ("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),("PNG", "*.png"), ("TIFF", "*.tiff; *.tif")])
        
        self.imagem.src_img = Image.open(self.imagem.file)

        self.render_image()

    def render_image(self):

        if self.imagem.src_img:

            picture=self.imagem.src_img

            picture_w, picture_h = picture.size

            picture_w_resized, picture_h_resized = int(picture_w * self.slider.get()/100), int(picture_h * self.slider.get()/100) 

            self.imagem.img = ImageTk.PhotoImage(picture.resize((picture_w_resized, picture_h_resized),resample=Image.LANCZOS))

            self.frame.destroy()
            
            self.frame = Frame(self.root,width=picture_w_resized,height=picture_h_resized)

            self.frame.pack(side=LEFT,anchor='n', padx=20,pady=2)
            
            self.canvas.destroy()
                   
            self.canvas = Canvas(self.frame, width=picture_w_resized, height=picture_h_resized)

            self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)
            
            self.canvas.pack(side=LEFT)

        else:
            pass
        
    def close_free_draw(self):
        points_list = [(point.x,point.y) for point in self.freeDraw.points]
        self.canvas.create_line(points_list)

myApp = App()

myApp.root.mainloop()

