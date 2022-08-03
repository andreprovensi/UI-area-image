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

def get_coordinates_on_click(event):
    x, y = event.x, event.y
    return x,y

def getsquare(root):

    newrec = Rectangle()
    root.bind('<Button-1>', get_coordinates_on_click)
    
    while len(newrec.points) <4:
        x,y = get_coordinates_on_click(event)
        point = Point(x,y)
        newrec.get_point(point)

    root.unbind('<Button-1>', get_coordinates_on_click)
    return newrec
p1 = Point(1,2)
p2= Point(5,6)
p3 = Point(-1,-2)



# myrec = Rectangle()
# ponto = Point(1,2)

# myrec.get_point(ponto)

# print(myrec.points[0].y)



# def get_points(event):

#     myRec = Rectangle()
#     cont=0
#     while cont<3:
#         cont+=1
#         x, y = get_coordinates_on_click(event)
#         ponto = Point(x,y)
#         myRec.points.append(ponto)
        
#     return myRec