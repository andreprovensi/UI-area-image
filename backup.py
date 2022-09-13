from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from scipy.interpolate import CubicSpline
import numpy as np


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Polygon:
    def __init__(self, points=[]):
        self.points = points
        self.area_px = None
        self.area_m = None
        
    def get_point(self,ponto=Point()):
        self.points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def reset_points(self):
        self.points = []

class Spline:
    def __init__(self, points=[]):
        self.points = points
        self.area_px = None
        self.area_m = None
        
    def get_point(self,ponto=Point()):
        self.points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def reset_points(self):
        self.points = []

class Imagem:
    def __init__(self):
        self.file = None
        self.img = None
        self.src_img = None

class Dimension:
    def __init__(self, points=[]):
        self.points = points
        self.length = None
        self.px_length = None
    
    def reset_points(self):
        self.points = []

    def set_length(self,length):
        self.length = length

class Area:
    def __init__(self):
        self.area_px_plan = None
        self.area_px_proj = None
        self.area_ratio_px_proj_px_plan = None
        self.area_m_proj = None
        self.area_ratio_m_proj_px_proj = None

class FreeDraw:
    def __init__(self, points=[]):
        self.points = points
        self.area_px = None
        self.area_m = None

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

        self.polygon = Polygon()

        self.spline = Spline()

        self.area = Area()

        self.dimensionRatio_1 = Dimension()

        self.dimensionRatio_2 = Dimension()
        

        # Cria o menu para carregar as imagens
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar,padx=1,pady=1)
        self.file_menu = Menu(self.menubar,tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=lambda: self.open_image())
        self.file_menu.add_command(label="Exit", command=lambda: self.root.quit())

        # FRAMES

        # Cria o frame geral
        self.frame = Frame(self.root)

        # Frame para Botões dos tipos de desenho

        self.frame_buttons = Frame(self.root,relief=RAISED,borderwidth=3)
        self.frame_buttons.pack(side=RIGHT,fill=Y,expand=False)

        # Frame e componentes para a definição do tamanho da imagem e da razão mm/pixel

        self.frame_img_prop = Frame(self.root,relief=GROOVE,borderwidth=2,width=135)
        self.frame_img_prop.pack(side=LEFT,fill=Y,expand=False)

        self.frame_zoom = Frame(self.frame_img_prop,relief=RIDGE,borderwidth=1)

        # FRAME INPUT
        self.frame_input = Frame(self.frame_img_prop,relief=RIDGE,borderwidth=1)

        #FRAME INPUT LABLE
        self.frame_input_lable = Frame(self.frame_input)

        #FRAME INPUT, LENGTH 1 LED
        self.frame_input_led_1 = Frame(self.frame_input)

        #FRAME INPUT, LENGTH 2 LED
        self.frame_input_led_2 = Frame(self.frame_input)

        # FRAME INPUT BUTTON
        self.frame_input_button = Frame(self.frame_input)

        ### INPUTS, LABEL and LEDS
        self.dimension_input_lable = ttk.Label(self.frame_input_lable,text='Comprimentos conhecidos em mm',wraplength=150)

        # LENGTH 1
        self.green_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_1 = ttk.Label(self.frame_input_led_1, image=self.red_led_figure_1 )
        self.C1_button = ttk.Button(self.frame_input_led_1, text='C1', width=4, command=self.C1_button_pressed)
        
        # LENGTH 2
        self.green_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_2 = ttk.Label(self.frame_input_led_2, image=self.red_led_figure_2)
        self.C2_button = ttk.Button(self.frame_input_led_2, text='C2', width=4, command=self.C2_button_pressed)
        
        # SLIDERS
        self.slider_lable = ttk.Label(self.frame_zoom,text='Zoom',wraplength=90)
        self.slider = ttk.Scale(self.frame_zoom,from_=1, to=200, orient='horizontal', command = lambda event: [self.render_image(), self.led_1.config(image=self.red_led_figure_1),self.led_2.config(image=self.red_led_figure_2)],length=125)
        self.slider.set(30)
        
        self.input_value_1 = StringVar(self.root)
        self.dimension_input_1 = Entry(self.frame_input_led_1,textvariable=self.input_value_1, bd=3,width=15)
        
        self.input_value_2 = StringVar(self.root)
        self.dimension_input_2 = Entry(self.frame_input_led_2,textvariable=self.input_value_2, bd=3,width=15)
        
        # Action box
        self.action_box = Message(self.frame_img_prop,text='1 - Carregue uma imagem\n\n2 - Ajuste o zoom\n\n3 - Digite os valores dos comprimentos conhecidos\n\n4 - Aperte C1 para definir os pontos do comprimento 1\n\n5 - Aperte C2 para definir os pontos do comprimento 2\n\n6 - Quando os dois leds ficarem verdes, aperte em desenho livre',bg='light yellow', anchor='nw',justify=LEFT, width=150)
        
    
        #Positioning
        self.frame_zoom.pack(side=TOP,fill=BOTH)
        self.frame_input.pack(side=TOP,fill=BOTH)
        self.action_box.pack(side=TOP, fill=BOTH,expand=True)
        self.frame_input_lable.pack(side=TOP)
        self.frame_input_led_1.pack(side = TOP)
        self.frame_input_led_2.pack(side=TOP,pady=5)
        self.frame_input_button.pack(side=TOP)

        self.slider_lable.pack(side=LEFT,anchor='w',pady=15)
        self.slider.pack(side=LEFT,anchor='n',padx=1,pady=15)

        self.C1_button.pack(side=LEFT,padx=2)
        self.C2_button.pack(side=LEFT,padx=2)

        self.dimension_input_lable.pack(side=TOP,pady=10)
        self.dimension_input_1.pack(side=LEFT)
        self.dimension_input_2.pack(side=LEFT)

        self.led_1.pack(side=RIGHT,anchor='ne')
        self.led_2.pack(side=RIGHT,anchor='ne')
    
        # Canvas
        self.canvas = Canvas(self.frame)

        
        self.button_free_draw = ttk.Button(self.frame_buttons, text ='Desenho Livre', command = self.check_free_draw)

        self.button_polygon = ttk.Button(self.frame_buttons, text ='Polígono', command = self.check_polygon)

        self.button_spline = ttk.Button(self.frame_buttons, text ='Spline', command = self.check_spline)


        # BOTÕES de tipo de desenho
        self.button_free_draw.pack(side=TOP,pady=25,padx=5)
        self.button_polygon.pack(side=TOP,pady=25)
        self.button_spline.pack(side=TOP,pady=25)


        #FRAME CENTRAL
        self.frame = Frame(self.root,relief=RIDGE,border=1)

        self.frame.pack(side=TOP,anchor='n',fill=BOTH, expand=True)

        self.vbar = Scrollbar(self.frame, orient='vertical')
        self.hbar = Scrollbar(self.frame, orient='horizontal')

        self.tag_dimension = 'tagDimension'
        self.tag_freeDraw = 'tagFreeDraw'
        self.tag_polygon = 'tagPolygon'
        self.tag_spline = 'tagSpline'
        self.tag_point_spline = 'tagPointSpline'

        self.vbar.pack(side=LEFT,fill=Y)
        self.hbar.pack(side=BOTTOM,fill=X)
        
        self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.clear_drawings()])
    
    def check_polygon(self):
        self.root.focus()
        if self.area.area_ratio_m_proj_px_proj:
            # self.render_image()
            # self.canvas.delete(self.tag_freeDraw)
            self.clear_drawings()
            self.action_box.config(text='-Clique para selecionar os pontos que delimitam a lesão.\n\n- Aperte espaço para finalizar o polígono.',justify=LEFT)
            self.polygon.reset_points()
            self.canvas.bind('<Button-1>',self.create_polygon)
            self.root.bind('<space>',lambda event: self.close_polygon())
        else:
            self.canvas.unbind('<Button-1>')
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def create_polygon(self,event):
        ponto = Point(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.polygon.get_point(ponto)
        self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=2,tags=self.tag_polygon)
        if len(self.polygon.points)>1:
            self.canvas.create_line(self.polygon.points[-2].x, self.polygon.points[-2].y, self.polygon.points[-1].x, self.polygon.points[-1].y,tags=self.tag_polygon)

    def close_polygon(self):
        if len(self.polygon.points)>=3:
            self.unbind_all()
            self.canvas.create_line(self.polygon.points[-1].x, self.polygon.points[-1].y, self.polygon.points[0].x, self.polygon.points[0].y,tags=self.tag_polygon) 
            self.calcula_area_polygon()
        else:
            self.unbind_all()
            self.polygon.reset_points()
            # self.render_image()

    def check_spline(self):
        self.root.focus()
        if self.area.area_ratio_m_proj_px_proj:
            # self.render_image()
            # self.canvas.delete(self.tag_freeDraw)
            self.clear_drawings()
            self.action_box.config(text='-Clique para selecionar os pontos que delimitam a lesão.\n\n- Aperte espaço para finalizar a spline.',justify=LEFT)
            self.spline.reset_points()
            self.canvas.bind('<Button-1>',self.create_spline)
            self.root.bind('<space>',lambda event: self.close_spline())
        else:
            self.canvas.unbind('<Button-1>')
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def create_spline(self,event):
        ponto = Point(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.spline.get_point(ponto)
        self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=3, tags=self.tag_point_spline) 

        if len(self.spline.points) > 4:
            self.canvas.delete(self.tag_spline)
            # self.canvas.create_line([(point.x,point.y) for point in self.spline.points],smooth=True,tags=self.tag_spline)
            
            x_t = [ponto.x for ponto in self.spline.points]
            y_t = [ponto.y for ponto in self.spline.points]

            x_t_spline = CubicSpline(list(np.arange(0,len(x_t))),x_t)
            y_t_spline = CubicSpline(list(np.arange(0,len(y_t))),y_t)

            # delta_t = np.linspace(0,len(x_t)-1,1000)
            delta_t = list(np.arange(0,len(self.spline.points)-1+0.1,0.1))

            points_list_spline = [(x_t_spline(t), y_t_spline(t)) for t in delta_t]

            self.canvas.create_line(points_list_spline,fill='blue',tags=self.tag_spline)
       
       
    def close_spline(self):
        self.unbind_all()

        if len(self.spline.points)>3:
            self.canvas.create_line(self.spline.points[-1].x, self.spline.points[-1].y, self.spline.points[0].x, self.spline.points[0].y,tags=self.tag_spline) 
            self.calcula_area_spline()   # Definir a função que calcula a area da spline
        else:
            self.spline.reset_points()

    def check_free_draw(self):
        self.root.focus()
        if self.area.area_ratio_m_proj_px_proj:
            self.clear_drawings()
            self.action_box.config(text='Clique duas vezes para começar o desenho e, chegando perto do final do desenho, clique novamente duas vezes')
            self.freeDraw.reset_points()
            # self.canvas.bind('<Double-Button>', lambda event: [self.canvas.bind('<Motion>',self.free_draw), self.canvas.bind('<Double-Button>', lambda event: [self.canvas.unbind('<Motion>'),self.freeDraw.closing_points_free_draw(),self.close_free_draw(),self.calcula_area_freeDraw()]) ])
            self.canvas.bind('<Double-Button>', lambda event: [self.canvas.bind('<Motion>',self.free_draw), self.canvas.bind('<Double-Button>', lambda event: [self.canvas.unbind('<Motion>'),self.close_free_draw(),self.calcula_area_freeDraw()]) ])
        else:
            self.canvas.unbind('<Motion>')
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def free_draw(self,event):
        if self.area.area_ratio_m_proj_px_proj:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            ponto = Point(x,y)
            print(x,y)
            self.freeDraw.get_point(ponto)
            if len(self.freeDraw.points)>1:
                self.canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y,tags=self.tag_freeDraw)
        else:
            self.canvas.unbind('<Motion>')
            messagebox.showerror('','Você precisa definir os comprimentos conhecidos')

    def close_free_draw(self):
        self.unbind_all()
        self.canvas.create_line(self.freeDraw.points[-1].x,self.freeDraw.points[-1].y,self.freeDraw.points[0].x,self.freeDraw.points[0].y,tags=self.tag_freeDraw)

    def set_proj_plan_ratio(self):
        P1 = self.dimensionRatio_1.points[0]
        P2 = self.dimensionRatio_1.points[1]
        P3 = self.dimensionRatio_2.points[0]
        P4 = self.dimensionRatio_2.points[1]
                 
        vetor_1 = Point(P2.x - P1.x, P2.y - P1.y)

        vetor_2 = Point(P4.x - P3.x, P4.y - P3.y)

        self.area.area_px_plan = ((vetor_1.x*vetor_2.y) ** 2 + (vetor_2.x*vetor_1.y) ** 2) ** 0.5

        self.area.area_px_proj = (vetor_1.x**2 + vetor_1.y**2)**0.5 * (vetor_2.x**2 + vetor_2.y**2)**0.5

        self.area.area_ratio_px_proj_px_plan = self.area.area_px_proj / self.area.area_px_plan

        length_1 = self.dimensionRatio_1.length 

        length_2 = self.dimensionRatio_2.length 

        self.area.area_m_proj = length_1 * length_2 

        self.area.area_ratio_m_proj_px_proj = length_1 * length_2 / self.area.area_px_proj

    def C1_button_pressed(self):
        if self.input_value_1.get():
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.dimensionRatio_1.reset_points()
            self.dimensionRatio_1.set_length(float(self.input_value_1.get()))
            self.canvas.bind('<Button-1>', self.get_C1_points)
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C1_points(self, event):   
        ponto=Point(self.canvas.canvasx(event.x),self.canvas.canvasy(event.y))
        
        if len(self.dimensionRatio_1.points)<=1:
            self.dimensionRatio_1.points.append(ponto)
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=5,tags=self.tag_dimension)
        
        if len(self.dimensionRatio_1.points) == 2:
            self.led_1.config(image=self.green_led_figure_1)
            self.canvas.unbind('<Button-1>')
            self.root.focus()

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()
            self.unbind_all()
            self.canvas.delete(self.tag_dimension)

    def C2_button_pressed(self):
        if self.input_value_2.get():
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.dimensionRatio_2.reset_points()
            self.dimensionRatio_2.set_length(float(self.input_value_2.get()))
            self.canvas.bind('<Button-1>',self.get_C2_points)
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C2_points(self, event):   
        ponto=Point(self.canvas.canvasx(event.x),self.canvas.canvasy(event.y))
        
        if len(self.dimensionRatio_2.points)<=1:
            self.dimensionRatio_2.points.append(ponto)
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=5, tags=self.tag_dimension)
        
        if len(self.dimensionRatio_2.points) == 2:
            self.led_2.config(image=self.green_led_figure_2)
            self.canvas.unbind('<Button-1>')
            self.root.focus()

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()
            self.canvas.delete(self.tag_dimension)


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
          
            self.canvas.destroy()
                   
            self.canvas = Canvas(self.frame, width=picture_w_resized, height=picture_h_resized,scrollregion=(0,0,picture_w_resized,picture_h_resized))

            self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)

            self.hbar.config(command=self.canvas.xview)

            self.vbar.config(command=self.canvas.yview)

            self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

            self.canvas.pack(side=TOP, anchor='n')

    def calcula_area_freeDraw(self):
        if len(self.freeDraw.points)>2 and self.area.area_ratio_m_proj_px_proj:

            areas_px=[]

            for i,_ in enumerate(self.freeDraw.points):
                delta_x_px = self.freeDraw.points[i].x - self.freeDraw.points[i-1].x
                delta_y_px = self.freeDraw.points[i].y - self.freeDraw.points[i-1].y
                y_1_px = min(self.freeDraw.points[i].y ,self.freeDraw.points[i-1].y)
                area = delta_x_px * (y_1_px + abs(delta_y_px)/2)

                areas_px.append(area)
            
            self.freeDraw.area_px = abs(sum(areas_px))
            
            area_meters = self.freeDraw.area_px * self.area.area_ratio_px_proj_px_plan * self.area.area_ratio_m_proj_px_proj
            self.freeDraw.area_m = area_meters
            
            self.action_box.config(text=f'A área da figura é {area_meters:.2f} mm²')
            # print(f'Calcula area geom foi chamado, o ponto inicial é {self.freeDraw.points[0].x},{self.freeDraw.points[0].y} e o ponto Final é {self.freeDraw.points[-1].x},{self.freeDraw.points[-1].y} ')
    
    def calcula_area_polygon(self):
        if len(self.polygon.points)>2 and self.area.area_ratio_m_proj_px_proj:

            areas_px=[]

            for i,_ in enumerate(self.polygon.points):
                delta_x_px = self.polygon.points[i].x - self.polygon.points[i-1].x
                delta_y_px = self.polygon.points[i].y - self.polygon.points[i-1].y
                y_1_px = min(self.polygon.points[i].y ,self.polygon.points[i-1].y)
                area = delta_x_px * (y_1_px + abs(delta_y_px)/2)
                areas_px.append(area)
            
            self.polygon.area_px = abs(sum(areas_px))
            
            area_meters = self.polygon.area_px * self.area.area_ratio_px_proj_px_plan * self.area.area_ratio_m_proj_px_proj
            self.polygon.area_m = area_meters
            
            self.action_box.config(text=f'A área da figura é {area_meters:.2f} mm²')
            # print(f'Calcula area geom foi chamado, o ponto inicial é {self.freeDraw.points[0].x},{self.freeDraw.points[0].y} e o ponto Final é {self.freeDraw.points[-1].x},{self.freeDraw.points[-1].y} ')
  
    def calcula_area_spline(self):
        if len(self.spline.points)>3 and self.area.area_ratio_m_proj_px_proj:

            x_t = [ponto.x for ponto in myApp.spline.points]
            y_t = [ponto.y for ponto in myApp.spline.points]

            x_t_spline = CubicSpline(list(range(0,len(x_t))),x_t)
            y_t_spline = CubicSpline(list(range(0,len(y_t))),y_t)

            delta_t = np.linspace(0,len(x_t)-1,2000)
            # delta_t = list(np.arange(0,len(self.spline.points)-1+0.1,0.1))

            points_list = [Point(x_t_spline(t),y_t_spline(t)) for t in delta_t]

            areas_px=[]

            for i,_ in enumerate(points_list):
                delta_x_px = points_list[i].x - points_list[i-1].x
                delta_y_px = points_list[i].y - points_list[i-1].y
                y_1_px = min(points_list[i].y ,points_list[i-1].y)
                area = delta_x_px * (y_1_px + abs(delta_y_px)/2)
                areas_px.append(area)

            area_px = abs(sum(areas_px))

            self.spline.area_px = area_px

            self.spline.area_m = self.spline.area_px * self.area.area_ratio_px_proj_px_plan * self.area.area_ratio_m_proj_px_proj

            self.action_box.config(text=f'A área da figura é {self.spline.area_m:.2f} mm²')

    def unbind_all(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Double-Button>')
        self.canvas.unbind('<Motion>')
        self.root.unbind('<space>')
        # self.root.unbind('<KeyPress>')

    def clear_drawings(self):
        self.canvas.delete(self.tag_dimension)
        self.canvas.delete(self.tag_freeDraw)
        self.canvas.delete(self.tag_polygon)
        self.canvas.delete(self.tag_spline)
        self.canvas.delete(self.tag_point_spline)

myApp = App()

myApp.root.mainloop()

# print('Raza pixel proj pixel plan',myApp.area.area_ratio_px_proj_px_plan)

# print('\n Razao m proj pixel proj', myApp.area.area_ratio_m_proj_px_proj)