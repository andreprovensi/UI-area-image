

def countup(n):

    if n<1:
        return []
    else:
        
        countArray = countup(n-1)
        print('depois',countArray)
        countArray.append(n)
        return countArray



#countup(3)

a =1


# import numpy as np

# print(np.linspace(0,50,50))

class Testt:


    atr_class = 'atributo de classe'

    def __init__(self):
        self.a=2

    @staticmethod
    def metodo_estatico(arg1):
        print(arg1)


myobj = Testt()

myobj.metodo_estatico('chamei o metodo estatic')