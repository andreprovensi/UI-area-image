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

aa = []

print(aa[-1])

function rot13(str) {
  function parser(char){

  const alphabet = 'abcdefghijklmnopqrstuvwxyz'.toUpperCase().split('');
  
    const regex = /[a-zA-Z]/;
    if(regex.test(char)){
    const charPositionInAlphabet = alphabet.indexOf(char)

    const cipherPosition = (charPositionInAlphabet+13)>(alphabet.length-1)?(charPositionInAlphabet+13-alphabet.length):(charPositionInAlphabet+13)

    const cipher = alphabet[cipherPosition]
    return cipher
    }

    else{
      return char
    }

  }

  const resp = str.split('').map(char=>parser(char)).join('')

  return resp

}

rot13("GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT.");
