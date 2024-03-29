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
        self.pre_points=[]
        self.points = points
        self.area_px = None
        self.area_m = None
        
    def get_point(self,ponto=Point()):
        self.points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def get_pre_point(self,ponto=Point()):
        self.pre_points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def reset_points(self):
        self.points = []

    def reset_pre_points(self):
        self.pre_points=[]

    def remove_pre_point(self):
        self.pre_points.pop()

class Spline:
    def __init__(self, points=[]):
        self.pre_points = []
        self.points = points
        self.area_px = None
        self.area_m = None
        
    def get_point(self,ponto=Point()):
        self.points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def get_pre_point(self,ponto=Point()):
        self.pre_points.append(ponto)
        print(f'{ponto.x}, {ponto.y}')

    def reset_points(self):
        self.points = []

    def reset_pre_points(self):
        self.pre_points=[]

    def remove_pre_point(self):
        self.pre_points.pop()

class FreeDraw:
    def __init__(self, points=[]):
        self.pre_points=[]
        self.points = points
        self.area_px = None
        self.area_m = None

    def get_point(self,ponto=Point()):   
        self.points.append(ponto)

    def get_pre_point(self,ponto=Point()):   
        self.pre_points.append(ponto)

    def reset_points(self):
        self.points = []

    def reset_pre_points(self):
        self.pre_points=[]

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

class App:
    def __init__(self):

        self.root = Tk()
        self.root.title('SMART - Surface Measurement Tool')
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

        # Frame para Botões dos tipos de desenho
        self.frame_buttons = Frame(self.root,relief=GROOVE,borderwidth=2)
        self.frame_buttons.pack(side=RIGHT,fill=Y,expand=False)

        # Frame e componentes para a definição do tamanho da imagem e da razão mm/pixel

        self.frame_img_prop = Frame(self.root,relief=GROOVE,borderwidth=2,width=135)
        self.frame_img_prop.pack(side=LEFT,fill=Y,expand=False)

        self.frame_zoom = Frame(self.frame_img_prop,relief=RIDGE,borderwidth=1)
        self.frame_checkbox = Frame(self.frame_zoom,height=1)

        self.frame = Frame(self.root,relief=RIDGE,border=1)
        self.frame.pack(side=TOP,anchor='n',fill=BOTH, expand=True)

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

        # BUTTON C1 e LED 1
        self.green_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_1 = ttk.Label(self.frame_input_led_1, image=self.red_led_figure_1 )
        self.C1_button = ttk.Button(self.frame_input_led_1, text='C1', width=4, command=self.C1_button_pressed)
        self.C1_input_value_was_changed = False
        
        # BUTTON C2 e LED 2
        self.green_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_2 = ttk.Label(self.frame_input_led_2, image=self.red_led_figure_2)
        self.C2_button = ttk.Button(self.frame_input_led_2, text='C2', width=4, command=self.C2_button_pressed)
        self.C2_input_value_was_changed = False
        
        # SLIDERS e CHECK BOX
        self.slider_lable = ttk.Label(self.frame_zoom,text='Zoom',wraplength=90)
        self.slider = ttk.Scale(self.frame_zoom,from_=1, to=200, orient='horizontal', command =lambda event: self.set_zoom() ,length=125)
        self.slider.set(30)

        self.on_off = StringVar(self.root)
        self.check_box = ttk.Checkbutton(self.frame_checkbox, text='Fixar zoom', variable=self.on_off, onvalue='disabled', offvalue='enabled', command=lambda: [self.slider.config(state=self.on_off.get()),self.root.focus()])
        
        
        #INPUTS DO C1 E C2
        self.input_value_1 = StringVar(self.root)
        self.dimension_input_1 = Entry(self.frame_input_led_1,textvariable=self.input_value_1, bd=3,width=15)
        self.input_value_1.trace_add("write", lambda name, index,mode, var=self.input_value_1: self.check_dimension1_value_change())
        
        self.input_value_2 = StringVar(self.root)
        self.dimension_input_2 = Entry(self.frame_input_led_2,textvariable=self.input_value_2, bd=3,width=15)
        self.input_value_2.trace_add("write", lambda name, index,mode, var=self.input_value_2: self.check_dimension2_value_change())
        
        # Action box
        # self.action_box = Text(self.frame_img_prop,bg='light yellow', width=20,wrap=WORD,font='verdana 8',padx=5,pady=8)   
        # self.action_box.insert(INSERT,'1 - Carregue uma imagem\n\n2 - Ajuste o zoom\n\n3 - Digite os valores dos comprimentos conhecidos\n\n4 - Aperte C1 para definir os pontos do comprimento 1\n\n5 - Aperte C2 para definir os pontos do comprimento 2\n\n6 - Quando os dois leds ficarem verdes, escolha uma forma de selecionar a área da lesão') 
        
        self.action_box = Message(self.frame_img_prop,text='1 - Carregue uma imagem\n\n2 - Ajuste o zoom\n\n3 - Digite os valores dos comprimentos conhecidos\n\n4 - Aperte C1 para definir os pontos do comprimento 1\n\n5 - Aperte C2 para definir os pontos do comprimento 2\n\n6 - Quando os dois leds ficarem verdes, escolha uma forma de selecionar a área da lesão',bg='light yellow', anchor='nw',justify=LEFT, width=150, font='arial 8')      
            
        #Positioning
        self.frame_zoom.pack(side=TOP,fill=BOTH)
        self.frame_checkbox.pack(side=BOTTOM, fill=BOTH)
        self.frame_input.pack(side=TOP,fill=BOTH)
        self.action_box.pack(side=TOP, fill=BOTH,expand=True)
        self.frame_input_lable.pack(side=TOP)
        self.frame_input_led_1.pack(side=TOP)
        self.frame_input_led_2.pack(side=TOP,pady=5)
        self.frame_input_button.pack(side=TOP)

        self.slider_lable.pack(side=LEFT,anchor='w')
        self.slider.pack(side=LEFT,anchor='ne',pady=15)
        self.check_box.pack(side=LEFT,pady=5)

        self.C1_button.pack(side=LEFT,padx=2)
        self.C2_button.pack(side=LEFT,padx=2)

        self.dimension_input_lable.pack(side=TOP,pady=10)
        self.dimension_input_1.pack(side=LEFT)
        self.dimension_input_2.pack(side=LEFT)

        self.led_1.pack(side=RIGHT,anchor='ne')
        self.led_2.pack(side=RIGHT,anchor='ne')
    
        #LADO DIREITO 

        #FRAMES
        self.frame_free_draw = Frame(self.frame_buttons, relief=RIDGE,border=1)
        self.frame_polygon = Frame(self.frame_buttons,relief=RIDGE,border=1)
        self.frame_spline = Frame(self.frame_buttons,relief=RIDGE,border=1)
        self.frame_erase = Frame(self.frame_buttons, relief=RIDGE,border=1)

        self.frame_free_draw.pack(side=TOP,fill=BOTH)
        self.frame_polygon.pack(side=TOP,fill=BOTH)
        self.frame_spline.pack(side=TOP,fill=BOTH)
        self.frame_erase.pack(side=TOP,fill=BOTH)
        
        #BOTÕES
        self.button_new_free_draw = ttk.Button(self.frame_free_draw, text ='Novo Desenho Livre', command = self.check_free_draw, width=20)
        self.button_show_free_draw = ttk.Button(self.frame_free_draw, text ='Mostrar Desenho Livre', command = self.show_free_draw, width=20)
        self.label_area_free_draw = Label(self.frame_free_draw,text='Área do Desenho Livre')
        self.text_area_freeDraw = Text(self.frame_free_draw,width=18,height=1,font='arial 10',padx=2)

        self.button_new_polygon = ttk.Button(self.frame_polygon, text ='Novo Polígono', command = self.check_polygon,width=20)
        self.button_show_polygon = ttk.Button(self.frame_polygon, text ='Mostrar Polígono', command = self.show_polygon, width=20)
        self.label_area_polygon = Label(self.frame_polygon,text='Área do Polígono')
        self.text_area_polygon = Text(self.frame_polygon,width=18,height=1,font='arial 10',padx=2)

        self.button_new_spline = ttk.Button(self.frame_spline, text ='Nova Spline', command = self.check_spline, width=20)
        self.button_show_spline = ttk.Button(self.frame_spline, text ='Mostrar Spline', command = self.show_spline, width=20)
        self.label_area_spline = Label(self.frame_spline,text='Área da Spline')
        self.text_area_spline = Text(self.frame_spline,width=18,height=1,font='arial 10',padx=2)

        self.button_erase = ttk.Button(self.frame_erase, text ='Limpar Imagem', command = lambda: [self.clear_drawings(), self.cler_dimensions_drawings(), self.root.focus()] , width=20)
        self.button_erase.pack(side=BOTTOM,pady=25)

        self.button_new_free_draw.pack(side=TOP,pady=15,padx=5)
        self.button_show_free_draw.pack(side=TOP,pady=10,padx=5)
        self.label_area_free_draw.pack(side=TOP)
        self.text_area_freeDraw.pack(side=TOP,pady=10, padx=5)

        self.button_new_polygon.pack(side=TOP,pady=15,padx=5)
        self.button_show_polygon.pack(side=TOP,pady=10,padx=5)
        self.label_area_polygon.pack(side=TOP)
        self.text_area_polygon.pack(side=TOP,pady=10, padx=5)

        self.button_new_spline.pack(side=TOP,pady=15)
        self.button_show_spline.pack(side=TOP,pady=10, padx=5)
        self.label_area_spline.pack(side=TOP)
        self.text_area_spline.pack(side=TOP,pady=10, padx=5)

        self.vbar = Scrollbar(self.frame, orient='vertical')
        self.hbar = Scrollbar(self.frame, orient='horizontal')

        # CANVAS
        self.canvas = Canvas(self.frame)

        #TAGS
 
        self.tag_pre_freeDraw = 'tagPreFreeDraw'
        self.tag_pre_polygon = 'tagPrePolygon'
        self.tag_pre_spline = 'tagPreSpline'
        self.tag_pre_point_spline = 'tagPrePointSpline'

        self.tag_dimension_1 = 'tagDimension_1'
        self.tag_dimension_2 = 'tagDimension_2'
        self.tag_freeDraw = 'tagFreeDraw'
        self.tag_polygon = 'tagPolygon'
        self.tag_spline = 'tagSpline'
        self.tag_point_spline = 'tagPointSpline'

        #SCROLLBARS
        self.vbar.pack(side=LEFT,fill=Y)
        self.hbar.pack(side=BOTTOM,fill=X)
            
    def check_polygon(self):
        self.root.focus()
        self.unbind_all()
        if self.area.area_ratio_m_proj_px_proj:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            self.action_box.config(text='-Clique para selecionar os pontos que delimitam a lesão.\n\n- Aperte Enter para finalizar o polígono.',justify=LEFT)
            self.polygon.reset_pre_points()
            self.canvas.bind('<Button-1>',self.create_polygon)
            self.canvas.bind('<Button-3>',lambda event: self.correct_polygon())
            self.root.bind('<Return>',lambda event: self.close_polygon())
            self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.clear_drawings()])
        else:
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def create_polygon(self,event):
        ponto = Point(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.polygon.get_pre_point(ponto)
        if len(self.polygon.pre_points) == 1:
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=2,tags=self.tag_pre_polygon)
        if len(self.polygon.pre_points)>1:
            self.canvas.create_line(self.polygon.pre_points[-2].x, self.polygon.pre_points[-2].y, self.polygon.pre_points[-1].x, self.polygon.pre_points[-1].y,tags=self.tag_pre_polygon)

    def correct_polygon(self):
        if len(self.polygon.pre_points)>2:
            self.polygon.remove_pre_point()
            self.draw_pre_polygon()
        else:
            self.clear_drawings()
            self.unbind_all()
            self.polygon.reset_pre_points()

    def draw_pre_polygon(self):
        self.canvas.delete(self.tag_pre_polygon)
        if len(self.polygon.pre_points)>=2:
            pointsList = [(p.x,p.y) for p in self.polygon.pre_points]
            self.canvas.create_line(pointsList,tags=self.tag_pre_polygon)

    def close_polygon(self):
        self.unbind_all()
        if len(self.polygon.pre_points)>=2:
            self.polygon.points = self.polygon.pre_points
            self.calcula_area_polygon()
            self.text_area_polygon.delete('1.0',END)
            self.text_area_polygon.insert(INSERT,f'        {self.polygon.area_m:.3f} mm²')
            points_list = [(p.x,p.y) for p in self.polygon.points]
            self.canvas.create_line(points_list,tags=self.tag_polygon)
            self.canvas.create_line(self.polygon.points[-1].x,self.polygon.points[-1].y,self.polygon.points[0].x,self.polygon.points[0].y,tags=self.tag_polygon)
            self.action_box.config(text='')
        else:
            self.polygon.reset_pre_points()

    def check_spline(self):
        self.root.focus()
        self.unbind_all()
        if self.area.area_ratio_m_proj_px_proj:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            self.action_box.config(text='-Clique para selecionar os pontos que delimitam a lesão.\n\n- Aperte Enter para finalizar a spline.',justify=LEFT)
            self.spline.reset_pre_points()
            self.canvas.bind('<Button-1>',self.create_spline)
            self.canvas.bind('<Button-3>',lambda event: self.correct_spline())
            self.root.bind('<Return>',lambda event: self.close_spline())
            self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.clear_drawings()])
        else:
            self.canvas.unbind('<Button-1>')
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def create_spline(self,event):
        ponto = Point(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.spline.get_pre_point(ponto)
        if len(self.spline.pre_points)==1:
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=3, tags=self.tag_pre_point_spline) 
        self.draw_pre_spline()

    def correct_spline(self):
        if len(self.spline.pre_points)>2:
            self.spline.remove_pre_point()
            self.draw_pre_spline()
        else:
            self.clear_drawings()
            self.unbind_all()
            self.spline.reset_pre_points()

    def draw_pre_spline(self):
        self.canvas.delete(self.tag_pre_spline)
        if len(self.spline.pre_points) > 1:
                    self.canvas.delete(self.tag_pre_spline)

                    x_t = [ponto.x for ponto in self.spline.pre_points]
                    y_t = [ponto.y for ponto in self.spline.pre_points]

                    x_t_spline = CubicSpline(list(np.arange(0,len(x_t))),x_t)
                    y_t_spline = CubicSpline(list(np.arange(0,len(y_t))),y_t)

                    # delta_t = np.linspace(0,len(x_t)-1,1000)
                    delta_t = list(np.arange(0,len(self.spline.pre_points)-1+0.1,0.1))

                    points_list_spline = [(x_t_spline(t), y_t_spline(t)) for t in delta_t]

                    self.canvas.create_line(points_list_spline,fill='black',tags=self.tag_pre_spline,width=1.2)
       
       
    def close_spline(self):
        self.unbind_all()
        self.spline.points = self.spline.pre_points
        self.calcula_area_spline()
        self.text_area_spline.delete('1.0',END)
        self.text_area_spline.insert(INSERT,f'        {self.spline.area_m:.3f} mm²')
        self.action_box.config(text='')

        if len(self.spline.points)>=3:
            self.show_spline()
            
        else:
            self.spline.reset_points()

    def check_free_draw(self):
        self.root.focus()
        self.unbind_all()
        if self.area.area_ratio_m_proj_px_proj:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            self.action_box.config(text='Clique,segure e arraste para selecionar a lesão, aperte Enter para finaliza o desenho livre')
            self.freeDraw.reset_pre_points()
            self.canvas.bind('<B1-Motion>',self.create_free_draw)
            self.root.bind('<Return>',lambda event: self.close_free_draw())
            self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.clear_drawings()])
        else:
            self.unbind_all()
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def create_free_draw(self,event):
        if self.area.area_ratio_m_proj_px_proj:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
            ponto = Point(x,y)
            print(x,y)
            self.freeDraw.get_pre_point(ponto)
            if len(self.freeDraw.pre_points)>1:
                self.canvas.create_line(self.freeDraw.pre_points[-2].x, self.freeDraw.pre_points[-2].y, self.freeDraw.pre_points[-1].x, self.freeDraw.pre_points[-1].y,tags=self.tag_pre_freeDraw)
        else:
            self.canvas.unbind('<Motion>')
            messagebox.showerror('','Você precisa definir os comprimentos conhecidos')

    def close_free_draw(self):
        self.unbind_all()
        self.freeDraw.points=self.freeDraw.pre_points
        self.calcula_area_freeDraw()
        self.text_area_freeDraw.delete('1.0',END)
        self.text_area_freeDraw.insert(INSERT,f'        {self.freeDraw.area_m:.3f} mm²')
        self.show_free_draw()
        self.action_box.config(text='')

    def set_proj_plan_ratio(self):
        P1 = self.dimensionRatio_1.points[0]
        P2 = self.dimensionRatio_1.points[1]
        P3 = self.dimensionRatio_2.points[0]
        P4 = self.dimensionRatio_2.points[1]
                 
        vetor_1 = Point(P2.x - P1.x, P2.y - P1.y)

        vetor_2 = Point(P4.x - P3.x, P4.y - P3.y)

        self.area.area_px_plan = abs(vetor_1.x*vetor_2.y - vetor_2.x*vetor_1.y)

        self.area.area_px_proj = (vetor_1.x**2 + vetor_1.y**2)**0.5 * (vetor_2.x**2 + vetor_2.y**2)**0.5

        self.area.area_ratio_px_proj_px_plan = self.area.area_px_proj / self.area.area_px_plan

        length_1 = self.dimensionRatio_1.length 

        length_2 = self.dimensionRatio_2.length 

        self.area.area_m_proj = length_1 * length_2 

        self.area.area_ratio_m_proj_px_proj = length_1 * length_2 / self.area.area_px_proj

    
    def check_dimension1_value_change(self):

        self.C1_input_value_was_changed =  True
        self.led_1.config(image=self.red_led_figure_1)
        self.dimensionRatio_1 = Dimension()
        self.area = Area()
        self.canvas.delete(self.tag_dimension_1)
        
        self.dimensions_logic()
    
    def check_dimension2_value_change(self):

        self.C2_input_value_was_changed = True
        self.led_2.config(image=self.red_led_figure_2)
        self.dimensionRatio_2 = Dimension()
        self.area = Area()
        self.canvas.delete(self.tag_dimension_2)
        
        self.dimensions_logic()
        
    def dimensions_logic(self):

        if self.C1_input_value_was_changed:
            self.clear_drawings()
            self.clear_points_entities()
        if self.C2_input_value_was_changed:    
            self.clear_drawings()
            self.clear_points_entities()
    
    def C1_button_pressed(self):
        self.root.focus()
        if self.input_value_1.get():
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.clear_drawings()
            self.dimensionRatio_1.reset_points()
            self.dimensionRatio_1.set_length(float(self.input_value_1.get()))
            self.unbind_all()
            self.clear_points_entities()
            self.text_area_freeDraw.delete('1.0',END)
            self.text_area_polygon.delete('1.0',END)
            self.text_area_spline.delete('1.0',END)
            self.canvas.bind('<Button-1>', self.get_C1_points)
            self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.canvas.delete(self.tag_dimension_1), self.dimensionRatio_1.reset_points(), self.root.focus()])
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C1_points(self, event):   
        ponto=Point(self.canvas.canvasx(event.x),self.canvas.canvasy(event.y))
        
        if len(self.dimensionRatio_1.points)<=1:
            self.dimensionRatio_1.points.append(ponto)
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=3,tags=self.tag_dimension_1)
        
        if len(self.dimensionRatio_1.points) == 2:
            self.led_1.config(image=self.green_led_figure_1)
            self.unbind_all()
            self.root.focus()
            self.C1_input_value_was_changed = False

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()
            self.unbind_all()
            self.action_box.config(text='- Selecione um método para selecionar a área da lesão')
            self.C1_input_value_was_changed = False
            # self.canvas.delete(self.tag_dimension)

    def C2_button_pressed(self):
        self.root.focus()
        if self.input_value_2.get():
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.clear_drawings()
            self.dimensionRatio_2.reset_points()
            self.dimensionRatio_2.set_length(float(self.input_value_2.get()))
            self.unbind_all()
            self.clear_points_entities()
            self.text_area_freeDraw.delete('1.0',END)
            self.text_area_polygon.delete('1.0',END)
            self.text_area_spline.delete('1.0',END)
            self.canvas.bind('<Button-1>',self.get_C2_points)
            self.root.bind('<Escape>',lambda event: [self.unbind_all(), self.canvas.delete(self.tag_dimension_2), self.dimensionRatio_2.reset_points(),self.root.focus()])
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C2_points(self, event):   
        ponto=Point(self.canvas.canvasx(event.x),self.canvas.canvasy(event.y))
        
        if len(self.dimensionRatio_2.points)<=1:
            self.dimensionRatio_2.points.append(ponto)
            self.canvas.create_oval((ponto.x,ponto.y,ponto.x,ponto.y),fill='black',width=3, tags=self.tag_dimension_2)
        
        if len(self.dimensionRatio_2.points) == 2:
            self.led_2.config(image=self.green_led_figure_2)
            self.unbind_all()
            self.root.focus()
            self.C2_input_value_was_changed = False

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()
            self.action_box.config(text='- Selecione um método para selecionar a área da lesão')
            # self.canvas.delete(self.tag_dimension)


    def open_image(self):
        self.imagem.file = askopenfilename(filetypes=[("all files","*"),("Bitmap Files","*.bmp; *.dib"), ("JPEG", "*.jpg; *.jpe; *.jpeg; *.jfif"),("PNG", "*.png"), ("TIFF", "*.tiff; *.tif")])
        
        self.imagem.src_img = Image.open(self.imagem.file)

        self.render_image()
        
        self.clear_points_entities()

        self.led_1.config(image=self.red_led_figure_1)
        self.led_2.config(image=self.red_led_figure_2)

        self.input_value_1.set('')
        self.input_value_2.set('')

        self.text_area_freeDraw.delete('1.0',END)
        self.text_area_polygon.delete('1.0',END)
        self.text_area_spline.delete('1.0',END)

        self.area = Area()

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

        
        if self.freeDraw.area_m or self.polygon.area_m or self.spline.area_m:
            self.clear_points_entities()

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
            
            # self.action_box.config(text=f'A área da figura é {area_meters:.2f} mm²')
            # self.text_area_freeDraw.insert(INSERT,f'{self.freeDraw.area_m:.2f} mm²')

    
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
              
    def calcula_area_spline(self):
        if len(self.spline.points)>3 and self.area.area_ratio_m_proj_px_proj:

            x_t = [ponto.x for ponto in self.spline.points]
            y_t = [ponto.y for ponto in self.spline.points]

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

    def show_free_draw(self):
        self.root.focus()
        if self.freeDraw.area_m:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            points_list = [(p.x,p.y) for p in self.freeDraw.points]
            points_list.append((self.freeDraw.points[0].x,self.freeDraw.points[0].y))
            self.canvas.create_line(points_list,tags=self.tag_freeDraw)
        else:
            messagebox.showerror('','O desenho livre precisa ser definido.')

    def show_polygon(self):
        self.root.focus()
        if self.polygon.area_px:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            points_list = [(p.x,p.y) for p in self.polygon.points]
            points_list.append((self.polygon.points[0].x,self.polygon.points[0].y))
            self.canvas.create_line(points_list,tags=self.tag_polygon)
        else:
            messagebox.showerror('','O polígono precisa ser definido.')

    def show_spline(self):
        self.root.focus()
        if self.spline.area_m:
            self.clear_drawings()
            self.cler_dimensions_drawings()
            x_t = [ponto.x for ponto in self.spline.points]
            y_t = [ponto.y for ponto in self.spline.points]

            x_t_spline = CubicSpline(list(np.arange(0,len(x_t))),x_t)
            y_t_spline = CubicSpline(list(np.arange(0,len(y_t))),y_t)

            # delta_t = np.linspace(0,len(x_t)-1,1000)
            delta_t = list(np.arange(0,len(self.spline.points)-1+0.1,0.1))

            points_list_spline = [(x_t_spline(t), y_t_spline(t)) for t in delta_t]
            points_list_spline.append((self.spline.points[0].x,self.spline.points[0].y))

            self.canvas.create_line(points_list_spline,fill='black',tags=self.tag_spline)
        
        else:
            messagebox.showerror('','A spline precisa ser definida.')   

    def unbind_all(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<Double-Button>')
        self.canvas.unbind('<Motion>')
        self.canvas.unbind('<B1-Motion>')
        self.root.unbind('<space>')
        self.root.unbind('<Escape>')
        self.root.unbind('<Return>')

    def clear_drawings(self):
        self.canvas.delete(self.tag_freeDraw)
        self.canvas.delete(self.tag_pre_freeDraw)
        self.canvas.delete(self.tag_polygon)
        self.canvas.delete(self.tag_pre_polygon)
        self.canvas.delete(self.tag_spline)
        self.canvas.delete(self.tag_pre_spline)
        self.canvas.delete(self.tag_point_spline)
        self.canvas.delete(self.tag_pre_point_spline)

    def cler_dimensions_drawings(self):
        self.canvas.delete(self.tag_dimension_1)
        self.canvas.delete(self.tag_dimension_2)

    def clear_points_entities(self):
        self.freeDraw = FreeDraw()
        self.polygon = Polygon()
        self.spline = Spline()
        self.canvas.delete(self.tag_freeDraw)
        self.canvas.delete(self.tag_polygon)
        self.canvas.delete(self.tag_spline)
        self.canvas.delete(self.tag_point_spline)
        self.text_area_freeDraw.delete('1.0',END)
        self.text_area_polygon.delete('1.0',END)
        self.text_area_spline.delete('1.0',END)

    def set_zoom(self):

        if self.imagem.src_img:
            self.render_image()
            self.led_1.config(image=self.red_led_figure_1)
            self.led_2.config(image=self.red_led_figure_2)
            self.clear_points_entities()
            self.input_value_1.set('') 
            self.input_value_2.set('')
            self.text_area_freeDraw.delete('1.0',END)
            self.text_area_polygon.delete('1.0',END)
            self.text_area_spline.delete('1.0',END)

myApp = App()

myApp.root.mainloop()