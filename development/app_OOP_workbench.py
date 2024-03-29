from tkinter import *
from tkinter import ttk
import tkinter
from tkinter.filedialog import askopenfilename
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

        self.slider = ttk.Scale(self.frame_buttons,from_=1, to=200, orient='horizontal', command = lambda event: self.render_image())
        self.slider.set(30)
        
        self.button_free_draw = ttk.Button(
            self.frame_buttons, text ='Free Draw', 
            command = lambda: [self.freeDraw.reset_points(),self.root.bind('<Double-Button>', lambda event: self.root.bind('<Motion>',free_draw))]
        )

        #self.button_free_draw.pack(anchor='ne',padx=1,pady=1)
        self.button_free_draw.pack(side=tkinter.TOP,pady=25)
        self.slider.pack(side=tkinter.TOP,padx=1,pady=15)

        def free_draw(event):
            
            #self.root.bind('<Double-Button>', lambda event: self.root.unbind('<Motion>')) # Não fecha o desenho
            self.root.bind(
                '<Double-Button>', 
                lambda event: [self.canvas.create_line(self.freeDraw.points[-1].x, self.freeDraw.points[-1].y, self.freeDraw.points[-0].x, self.freeDraw.points[-0].y),
                self.root.unbind('<Motion>')]
            ) # Fecha o desenho

            x, y = event.x, event.y
            ponto = Point(x,y)
            print(x,y)
            self.freeDraw.get_point(ponto)
    
            if len(self.freeDraw.points)>1:
                self.canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y)


    def open_image(self):

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

            self.frame.pack(anchor='nw', padx=20,pady=2)
            
            self.canvas.destroy()
                   
            self.canvas = Canvas(self.frame, width=picture_w_resized, height=picture_h_resized)

            self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)

            self.canvas.pack()
        else:
            pass
        
    
myApp = App()

myApp.root.mainloop()