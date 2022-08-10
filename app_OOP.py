from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

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

    def __init__(self, file=''):

        self.file = file
        self.img = PhotoImage(file=file)

class FreeDraw:

    def __init__(self, points=[]):
        self.points = points

    def get_point(self,ponto=Point()):   
        self.points.append(ponto)

    def reset_points(self):
        self.points = []

class App:

    def __init__(self):
        
        #Cria a interface gráfica
        self.root = Tk()
        self.root.geometry("1000x500")
        
        # Instancia o objeto imagem
        self.imagem = Imagem()
        
        # Instancia o objeto desenho livre
        self.freeDraw = FreeDraw()

        # Cria o menu
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=lambda: self.open_image())
        self.file_menu.add_command(label="Exit", command=lambda: self.root.quit())
        
        # Instancia o frame onde a imagem estará contida
        self.frame = Frame(self.root)

        # Instancia o canvas onde serão feitos os desenhos
        self.canvas = Canvas(self.frame, width=self.imagem.img.width(), height=self.imagem.img.height())
        
        def __call_free_draw(event):
            def __free_draw(event):
                
                x, y = event.x, event.y
                ponto = Point(x,y)
                print(x,y)
                if len(self.freeDraw.points)==0 or x != self.freeDraw.points[-1].x or y != self.freeDraw.points[-1].y:
                    self.freeDraw.get_point(ponto)

            self.freeDraw.points=[]
            self.root.bind('<Motion>',__free_draw)
            self.root.bind('<Double-Button>', lambda event: self.root.unbind('<Motion>'))

        self.button_free_draw = ttk.Button(self.root,text ='Free Draw', command=lambda: self.root.bind('<Double-Button>',__call_free_draw) )
        #self.button_free_draw = ttk.Button(self.root,text ='Free Draw', command=lambda: self.root.bind('<Double-Button>',lambda event: self.root.bind('<Motion>',__free_draw) ))

        self.button_free_draw.pack(anchor='e',padx=10,pady=10)


        # if len(self.freeDraw.points)>1:
        #     canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y)

        
    def open_image(self):

        #self.imagem.img= PhotoImage()

        self.imagem.file = askopenfilename(filetypes=[("all files","*"),("Bitmap Files","*.bmp; *.dib"), ("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),("PNG", "*.png"), ("TIFF", "*.tiff; *.tif")])
        
        self.imagem.img= PhotoImage(file=self.imagem.file)

        picture_w, picture_h = self.imagem.img.width(), self.imagem.img.height()

        img_container = self.frame

        img_container.pack(side=LEFT, padx=50,pady=50)

        self.canvas = Canvas(img_container, width=picture_w, height=picture_h)

        self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)

        self.canvas.pack()
        
myApp = App()

myApp.root.mainloop()

print(myApp.freeDraw.points[3].x)