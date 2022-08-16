from queue import Full
from tkinter import *
from tkinter import ttk, messagebox
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

class Dimension:
    def __init__(self, points=[]):
        self.points = points
        self.length = None
        self.ratio = None
    
    def reset_points(self):
        self.points = []

    def set_length(self,length):
        self.length = length

class FreeDraw:
    def __init__(self, points=[]):
        self.points = points
        self.area = None

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


    def calcula_area_pixel(self):
        if len(self.points)>2:
            
            unique_list = [self.points[0]]
            areas=[]

            for i, ponto in enumerate(self.points[1:]):
                if self.points[i].x != self.points[i-1].x or self.points[i].y != self.points[i-1].y:
                    unique_list.append(ponto)
                else:
                    pass
            for i, ponto in enumerate(unique_list[0:-1]):
                delta_x = unique_list[i+1].x - unique_list[i].x
                print(delta_x)
                if delta_x != 0:
                    #dir = int(abs(delta_x/delta_x))
                    dir = int(abs(delta_x)/delta_x)
                elif delta_x == 0:
                    dir = 0
                areas.append(ponto.y*dir+unique_list[i+1].y*dir)
                # print(ponto.y*dir)
            self.area = sum(tuple(areas))
                

class App:
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1000x500")

        self.imagem = Imagem()

        self.freeDraw = FreeDraw()

        self.dimensionRatio = Dimension()

        # Cria o menu para carregar as imagens
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar,padx=1,pady=1)
        self.file_menu = Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=lambda: self.open_image())
        self.file_menu.add_command(label="Exit", command=lambda: self.root.quit())

        # Cria o frame geral
        self.frame = Frame(self.root)


        # Frame para Botões dos tipos de desenho
        self.frame_buttons = Frame(self.root,relief=RAISED,borderwidth=3)
        self.frame_buttons.pack(side=tkinter.RIGHT,fill=BOTH,expand=False)


        # Frame e componentes para a definição do tamanho da imagem e da razão mm/pixel
        self.frame_img_prop = Frame(self.root,relief=RAISED,borderwidth=3)
        self.frame_img_prop.pack(side=tkinter.LEFT,fill=BOTH,expand=False)

        # Action box
        self.action_box = Message(self.frame_img_prop,text='-Carregue uma imagem\n-Ajuste o zoom\n-Digite o valor do comprimento conhecido\n-Aperte para selecionar os pontos que o definem',bg='light yellow', anchor='n',justify=LEFT)
        self.action_box.pack(side=BOTTOM, fill=BOTH,expand=True)

        # Slider
        self.slider_lable = ttk.Label(self.frame_img_prop,text='Zoom',wraplength=90).pack(side=TOP,anchor='nw')
        self.slider = ttk.Scale(self.frame_img_prop,from_=1, to=100, orient='horizontal', command = lambda event: self.render_image(),length=105)
        self.slider.set(30)
        self.slider.pack(side=TOP,anchor='n')

        # Input
        self.dimension_input_lable = ttk.Label(self.frame_img_prop,text='Comprimento conhecido em mm',wraplength=150).pack(side=TOP)
        
        self.input_value = StringVar(self.root)
        self.dimension_input = Entry(self.frame_img_prop,textvariable=self.input_value).pack(side=TOP)

        self.button_set_dimension = ttk.Button(
            self.frame_img_prop,text='Select points to dimension',
            command= lambda: self.button_get_length_pressed()
        )
        self.button_set_dimension.pack(side=TOP,anchor='n',pady=25)
    
        # Canvas
        self.canvas = Canvas(self.frame)

        
        self.button_free_draw = ttk.Button(
            self.frame_buttons, text ='Desenho Livre', 
            command = lambda: [self.action_box.config(text='Clique duas vezes para começar o desenho e, chegando perto do final do desenho, clique novamente duas vezes'),self.freeDraw.reset_points(),self.root.bind('<Double-Button>', lambda event: self.root.bind('<Motion>',self.free_draw))]
        )

        #self.button_free_draw.pack(anchor='ne',padx=1,pady=1)
        self.button_free_draw.pack(side=tkinter.TOP,pady=25)
        self.slider.pack(side=tkinter.TOP,padx=1,pady=15)

    def free_draw(self,event):
        if self.dimensionRatio.ratio:
            self.root.bind('<Double-Button>', lambda event: [self.root.unbind('<Motion>'),self.freeDraw.closing_points_free_draw(),self.close_free_draw(),self.calcula_area_geom()]) 
            x, y = event.x, event.y
            ponto = Point(x,y)
            print(x,y)
            self.freeDraw.get_point(ponto)
            if len(self.freeDraw.points)>1:
                self.canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y)
        else:
            self.root.unbind('<Motion>')
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')

    def button_get_length_pressed(self):
        if self.input_value.get():
            self.action_box.config(text='-Selecione os pontos do comprimento conhecido\n-Clique em Desenho Livre')
            self.dimensionRatio.reset_points()
            self.dimensionRatio.set_length(float(self.input_value.get()))
            self.root.bind('<Button-1>', lambda event: self.get_point_dimension(event))
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_point_dimension(self, event):   
        ponto=Point(event.x,event.y)
        
        if len(self.dimensionRatio.points)<=1:
            self.dimensionRatio.points.append(ponto)
        elif len(self.dimensionRatio.points) == 2:
            delta_x = abs(self.dimensionRatio.points[1].x - self.dimensionRatio.points[0].x)
            delta_y = abs(self.dimensionRatio.points[1].y - self.dimensionRatio.points[0].y)
            dist_px = (delta_x**2 + delta_y**2)**0.5
            self.dimensionRatio.ratio = self.dimensionRatio.length/dist_px
            self.root.unbind('<Button-1>')
            

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

            self.frame.pack(side=TOP,anchor='n', padx=20,pady=2)
            
            self.canvas.destroy()
                   
            self.canvas = Canvas(self.frame, width=picture_w_resized, height=picture_h_resized)

            self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)
            
            self.canvas.pack(side=LEFT)

        else:
            pass
        
    def close_free_draw(self):
        points_list = [(point.x,point.y) for point in self.freeDraw.points]
        self.canvas.create_line(points_list)

    def calcula_area_geom(self):
        if len(self.freeDraw.points)>2 and self.dimensionRatio.ratio:
            
            unique_list = [self.freeDraw.points[0]]
            #unique_list = self.freeDraw.points
            areas=[]

            for i, ponto in enumerate(self.freeDraw.points[1:]):
                if self.freeDraw.points[i].x != self.freeDraw.points[i-1].x or self.freeDraw.points[i].y != self.freeDraw.points[i-1].y:
                    unique_list.append(ponto)
                else:
                    pass
            for i, ponto in enumerate(unique_list[0:-1]):
                delta_x_px = unique_list[i+1].x - unique_list[i].x
                delta_y_px = unique_list[i+1].y - unique_list[i].y
                delta_x_m = delta_x_px*self.dimensionRatio.ratio
                delta_y_m = abs(delta_y_px*self.dimensionRatio.ratio)
                y_1_m = min(unique_list[i].y,unique_list[i+1].y)*self.dimensionRatio.ratio
                area = delta_x_m * (y_1_m + delta_y_m/2)

                areas.append(area)
            
            

            self.freeDraw.area = abs(sum(tuple(areas)))
            self.action_box.config(text=f'A área da figura é {1e-2*abs(sum(tuple(areas))):.2f} cm²')
            
                 

myApp = App()

myApp.root.mainloop()

# myApp.calcula_area_geom()
# print(myApp.freeDraw.area)
# print('A razao eh:', myApp.dimensionRatio.ratio)