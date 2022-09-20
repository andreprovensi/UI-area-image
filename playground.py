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

---------------------------

function telephoneCheck(str) {

// ver se passa no formato sem o código internacional

// se passar, ver se o código internacional é igual a 1

const regex1=/^\d{3}-\d{3}-\d{4}$/;
const regex1Int=/^(1\s{0,1})(\d{3}-\d{3}-\d{4})$/;

const regex2=/^[(]\d{3}[)]\d{3}-\d{4}$/;
const regex2Int=/^(1\s{0,1})([(]\d{3}[)]\d{3}-\d{4})$/;

const regex3=/^[(]\d{3}[)]\s{1}\d{3}-\d{4}$/;
const regex3Int=/^(1\s{0,1})([(]\d{3}[)]\s{1}\d{3}-\d{4})$/;

const regex4=/^\d{3}\s{1}\d{3}\s{1}\d{4}$/;
const regex4Int=/^(1\s{0,1})(\d{3}\s{1}\d{3}\s{1}\d{4})$/;

const regex5=/^\d{10}$/;
const regex5Int=/^(1\s{0,1})(\d{10})$/;


const numberRegexArr = [regex1,regex2,regex3,regex4,regex5,regex1Int,regex2Int,regex3Int,regex4Int,regex5Int];

const testNumber = numberRegexArr.some(regex=>regex.test(str))

if(!testNumber){return false}

else{return true}


}

console.log(telephoneCheck('5555555555'))

// telephoneCheck('12 5555555555');
                              
                              
-------------------------------------------
 function checkCashRegister(price, cash, cid) {

const change = cash-price;
const cashInDrawer = cid.reduce((acc,arr)=>acc+arr[1],0);
let status;
let changeStatus;

if(cashInDrawer>change){status="OPEN";}
else if(cashInDrawer<change){status="INSUFFICIENT_FUNDS";changeStatus=[]}
else if(cashInDrawer === change){status="CLOSED";}

let centenas;
let dezenas;
let unidades;
let frCentena;
let frUnidade;

centenas = Math.floor(change/100);
dezenas = Math.floor((change-centenas*100)/10)
unidades = Math.floor((change-centenas*100-dezenas*10))
frCentena = Math.floor((change-centenas*100-dezenas*10-unidades)*10)
frUnidade = Math.floor((change-centenas*100-dezenas*10-unidades)*10)


console.log(change,frCentena)

console.log(change,cashInDrawer)

}

checkCashRegister(19.51, 20, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]]);

