class class_test:
    class_atr = 1

    def muda_atr(self):
        self.class_atr+=1


myobj = class_test()
myobj.muda_atr()
myobj2 = class_test()
print(f'antes:{myobj2.class_atr}')


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

p1 = Point(2,2)
p2 = Point(2,2)

myset = set()
myset = myset | {p1}
myset = myset | {p2}

print(myset)

# aa = []

# print(aa[-1])

a = 1.2855866655
print(f'O valor e de {a:.2f}')