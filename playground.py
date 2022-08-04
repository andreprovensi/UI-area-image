class class_test:
    class_atr = 1

    def muda_atr(self):
        self.class_atr+=1


myobj = class_test()
myobj.muda_atr()
myobj2 = class_test()
print(f'antes:{myobj2.class_atr}')