from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


class Point:
    def __init__(self, x=0.0, y=0.0):
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
    
    def closing_points_free_draw(self):
        
        if len(self.points)>1:
            final_point = self.points[-1]
            initial_point = self.points[0]

            delta_x = initial_point.x - final_point.x
            delta_y = initial_point.y - final_point.y

            x_dir = 1 if delta_x > 0 else -1 if delta_x < 0 else 0
            
            y_dir = 1 if delta_y > 0 else -1 if delta_y < 0 else 0
            
            points_list = []

            for i in range(1,abs(delta_x)+1):
                ponto = Point(final_point.x+i*x_dir,final_point.y)
                points_list.append(ponto)
            for j in range(1,abs(delta_y)):
                ponto = Point(initial_point.x,final_point.y+j*y_dir)
                points_list.append(ponto)
            
            for k in points_list:
                self.get_point(k)

        else:
            pass

   
class App:
    def __init__(self):

        self.root = Tk()
        self.root.geometry("1000x500")

        self.imagem = Imagem()

        self.freeDraw = FreeDraw()

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

        # self.frame.pack(side=RIGHT,fill=BOTH)

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

        # SLIDERS
        self.slider_lable = ttk.Label(self.frame_zoom,text='Zoom',wraplength=90)
        self.slider = ttk.Scale(self.frame_zoom,from_=1, to=100, orient='horizontal', command = lambda event: self.render_image(),length=125)
        self.slider.set(30)

        ### INPUTS, LABEL and LEDS
        self.dimension_input_lable = ttk.Label(self.frame_input_lable,text='Comprimentos conhecidos em mm',wraplength=150)

        # LENGTH 1
        self.green_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_1 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_1 = ttk.Label(self.frame_input_led_1, image=self.red_led_figure_1 )
        self.C1_button = ttk.Button(self.frame_input_led_1, text='C1', width=4, command= lambda: self.C1_button_pressed())
        
        # LENGTH 2
        self.green_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_green_led.jpg'))
        self.red_led_figure_2 = ImageTk.PhotoImage(Image.open('images/small_red_led.jpg'))
        self.led_2 = ttk.Label(self.frame_input_led_2, image=self.red_led_figure_2)
        self.C2_button = ttk.Button(self.frame_input_led_2, text='C2', width=4, command= lambda: self.C2_button_pressed())
        
        
        self.input_value_1 = StringVar(self.root)
        self.dimension_input_1 = Entry(self.frame_input_led_1,textvariable=self.input_value_1, bd=3,width=15)
        
        self.input_value_2 = StringVar(self.root)
        self.dimension_input_2 = Entry(self.frame_input_led_2,textvariable=self.input_value_2, bd=3,width=15)
        

        self.button_set_dimension = ttk.Button(
            self.frame_input_button,text='Selecionar pontos do\ncomprimento',
            command= lambda: self.C1_button_pressed()
        )
        
        # Action box
        self.action_box = Message(self.frame_img_prop,text='- Carregue uma imagem\n\n- Ajuste o zoom\n\n- Digite os valores dos comprimentos conhecidos\n\n- Aperte C1 para definir os pontos do comprimento 1\n\n- Aperte C2 para definir os pontos do comprimento 2\n\n- Quando os dois leds ficarem verdes, aperte em desenho livre',bg='light yellow', anchor='nw',justify=LEFT, width=150)
        
    
        #Positioning
        self.frame_zoom.pack(side=TOP,fill=BOTH)
        self.frame_input.pack(side=TOP,fill=BOTH)
        self.action_box.pack(side=TOP, fill=BOTH,expand=True)
        self.frame_input_lable.pack(side=TOP)
        self.frame_input_led_1.pack(side = TOP)
        self.frame_input_led_2.pack(side=TOP,pady=5)
        self.frame_input_button.pack(side=TOP)

        self.slider_lable.pack(side=LEFT,anchor='w',pady=15)
        self.slider.pack(side=LEFT,anchor='n')

        self.C1_button.pack(side=LEFT,padx=2)
        self.C2_button.pack(side=LEFT,padx=2)

        self.dimension_input_lable.pack(side=TOP,pady=10)
        self.dimension_input_1.pack(side=LEFT)
        self.dimension_input_2.pack(side=LEFT)

        self.led_1.pack(side=RIGHT,anchor='ne')
        self.led_2.pack(side=RIGHT,anchor='ne')
    
        # Canvas
        self.canvas = Canvas(self.frame)

        
        self.button_free_draw = ttk.Button(
            self.frame_buttons, text ='Desenho Livre', 
            command = self.check_free_draw
        )

        self.button_free_draw.pack(side=TOP,pady=25)
        self.slider.pack(side=TOP,padx=1,pady=15)

    def check_free_draw(self):
        if self.area.area_ratio_m_proj_px_proj:
            self.render_image()
            self.action_box.config(text='Clique duas vezes para começar o desenho e, chegando perto do final do desenho, clique novamente duas vezes')
            self.freeDraw.reset_points()
            self.root.bind('<Double-Button>', lambda event: self.root.bind('<Motion>',self.free_draw))
        else:
            self.root.unbind('<Motion>')
            messagebox.showerror('','Você precisa definir o comprimento conhecido')
    
    def free_draw(self,event):
        if self.area.area_ratio_m_proj_px_proj:
            self.root.bind('<Double-Button>', lambda event: [self.root.unbind('<Motion>'),self.freeDraw.closing_points_free_draw(),self.close_free_draw(),self.calcula_area_geom()]) 
            x, y = event.x, event.y
            ponto = Point(x,y)
            print(x,y)
            self.freeDraw.get_point(ponto)
            if len(self.freeDraw.points)>1:
                self.canvas.create_line(self.freeDraw.points[-2].x, self.freeDraw.points[-2].y, self.freeDraw.points[-1].x, self.freeDraw.points[-1].y)
        else:
            self.root.unbind('<Motion>')
            messagebox.showerror('','Você precisa definir os comprimentos conhecidos')

    
    def set_proj_plan_ratio(self):
        P1 = self.dimensionRatio_1.points[0]
        P2 = self.dimensionRatio_1.points[1]
        P3 = self.dimensionRatio_2.points[0]
        P4 = self.dimensionRatio_2.points[1]
    
        delta_x_1 = P2.x - P1.x
        delta_y_1 = P2.y - P1.y
        #Colocar casos dos deltas serem 0
        angular_coeff_1 = delta_y_1 / delta_x_1 if delta_x_1 != 0 else None
        linear_coeff_1 = P1.y - angular_coeff_1 * P1.x if delta_x_1 !=0 else None
        # angular_coeff_1 = delta_y_1 / delta_x_1
        # linear_coeff_1 = P1.y - angular_coeff_1 * P1.x
        P0_x = P1.x if delta_x_1 == 0 else None

        delta_x_2 = P4.x - P3.x
        delta_y_2 = P4.y - P3.y
        angular_coeff_2 = delta_y_2 / delta_x_2 if delta_x_2 != 0 else None
        linear_coeff_2 = P3.y - angular_coeff_2 * P3.x if delta_x_2 !=0 else None

        P0_x = P3.x if delta_x_2 == 0 else None

        P0_x = (linear_coeff_2 - linear_coeff_1) / (angular_coeff_1 - angular_coeff_2) if not P0_x else P0_x
        P0_y = angular_coeff_1 * P0_x + linear_coeff_1 if angular_coeff_1 else angular_coeff_2 * P0_x + linear_coeff_2

        P0 = Point(P0_x, P0_y)

        print('Ponto zero',P0.x,P0.y)

        # Definir os pontos com máximo delta_x e delta_y entre P0 e os outros pontos 
                
        vetor_1 = Point(max(abs(P1.x - P0.x), abs(P2.x - P0.x)), max(abs(P1.y - P0.y), abs(P2.y - P0.y)))

        vetor_2 = Point(max(abs(P3.x - P0.x), abs(P4.x - P0.x)), max(abs(P3.y - P0.y), abs(P4.y - P0.y)))

        self.area.area_px_plan = ((vetor_1.x*vetor_2.y) ** 2 + (vetor_2.x*vetor_1.y) ** 2) ** 0.5

        self.area.area_px_proj = (vetor_1.x**2 + vetor_1.y**2)**0.5 * (vetor_2.x**2 + vetor_2.y**2)**0.5

        self.area.area_ratio_px_proj_px_plan = self.area.area_px_proj / self.area.area_px_plan

        length_1 = self.dimensionRatio_1.length * (vetor_1.x**2 + vetor_1.y**2)**0.5 / (delta_x_1**2 + delta_y_1**2)**0.5

        length_2 = self.dimensionRatio_2.length * (vetor_2.x**2 + vetor_2.y**2)**0.5 / (delta_x_2**2 + delta_y_2**2)**0.5

        print(f'O comprimento 1 é de {length_1} e o comprimento 2 de {length_2}')

        self.area.area_m_proj = length_1 * length_2 

        self.area.area_ratio_m_proj_px_proj = length_1 * length_2 / self.area.area_px_proj


    def C1_button_pressed(self):
        if self.input_value_1.get():
            self.render_image() #Caso já tenha algo desenhado, uma nova imagem é renderizada ao apertar o botão
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.dimensionRatio_1.reset_points()
            self.dimensionRatio_1.set_length(float(self.input_value_1.get()))
            self.root.bind('<Button-1>', lambda event: self.get_C1_points(event))
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C1_points(self, event):   
        ponto=Point(event.x,event.y)
        
        if len(self.dimensionRatio_1.points)<=1:
            self.dimensionRatio_1.points.append(ponto)
            self.canvas.create_oval((event.x,event.y,event.x,event.y),fill='black',width=5)
        
        if len(self.dimensionRatio_1.points) == 2:
            self.led_1.config(image=self.green_led_figure_1)
            self.root.unbind('<Button-1>')

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()

    def C2_button_pressed(self):
        if self.input_value_2.get():
            self.render_image() #Caso já tenha algo desenhado, uma nova imagem é renderizada ao apertar o botão
            self.action_box.config(text='- Selecione os pontos do comprimento conhecido')
            self.dimensionRatio_2.reset_points()
            self.dimensionRatio_2.set_length(float(self.input_value_2.get()))
            self.root.bind('<Button-1>', lambda event: self.get_C2_points(event))
            
        else:
            messagebox.showerror('','Você precisa digitar o comprimento conhecido')
            
        
    def get_C2_points(self, event):   
        ponto=Point(event.x,event.y)
        
        if len(self.dimensionRatio_2.points)<=1:
            self.dimensionRatio_2.points.append(ponto)
            self.canvas.create_oval((event.x,event.y,event.x,event.y),fill='black',width=5)
        
        if len(self.dimensionRatio_2.points) == 2:
            self.led_2.config(image=self.green_led_figure_2)
            self.root.unbind('<Button-1>')

        if len(self.dimensionRatio_1.points) == 2 and len(self.dimensionRatio_2.points) == 2:
            self.set_proj_plan_ratio()


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

            self.frame.pack(side=TOP,anchor='n', padx = 50,fill=BOTH, expand=True)
            
            self.canvas.destroy()
                   
            self.canvas = Canvas(self.frame, width=picture_w_resized, height=picture_h_resized)

            self.canvas.create_image(0, 0, anchor=NW, image=self.imagem.img)
            
            self.canvas.pack(side=TOP, anchor='n')

        else:
            pass
        
    def close_free_draw(self):
        points_list = [(point.x,point.y) for point in self.freeDraw.points]
        self.canvas.create_line(points_list)

    def calcula_area_geom(self):
        if len(self.freeDraw.points)>2 and self.area.area_ratio_m_proj_px_proj:
            
            unique_list = [self.freeDraw.points[0]]
            areas_px=[]

            for i, ponto in enumerate(self.freeDraw.points[1:]):
                if self.freeDraw.points[i].x != self.freeDraw.points[i-1].x or self.freeDraw.points[i].y != self.freeDraw.points[i-1].y:
                    unique_list.append(ponto)
                else:
                    pass

            for i, ponto in enumerate(unique_list[0:-1]):
                delta_x_px = unique_list[i+1].x - unique_list[i].x
                delta_y_px = unique_list[i+1].y - unique_list[i].y
                y_1_px = min(unique_list[i].y,unique_list[i+1].y)
                area = delta_x_px * (y_1_px + delta_y_px/2)

                areas_px.append(area)
            
            self.freeDraw.area_px = abs(sum(tuple(areas_px)))
            
            area_meters = self.freeDraw.area_px * self.area.area_ratio_px_proj_px_plan * self.area.area_ratio_m_proj_px_proj
            self.freeDraw.area_m = area_meters
            
            self.action_box.config(text=f'A área da figura é {area_meters:.2f} mm²')
            
                 

myApp = App()

myApp.root.mainloop()

# print('Raza pixel proj pixel plan',myApp.area.area_ratio_px_proj_px_plan)

# print('\n Razao m proj pixel proj', myApp.area.area_ratio_m_proj_px_proj)