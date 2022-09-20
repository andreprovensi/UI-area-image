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

let change = cash-price;
change*=1000;
change = Math.round(change)/1000
let cashInDrawer = cid.reduce((acc,arr)=>acc+arr[1],0);
cashInDrawer*=1000
cashInDrawer = Math.round(cashInDrawer)/1000
let status;
let changeStatus;

if(cashInDrawer<change){return {status:"INSUFFICIENT_FUNDS",change:[]}}
else if(cashInDrawer>change){status="OPEN";}
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
frUnidade = Math.round((change-centenas*100-dezenas*10-unidades-frCentena/10)*100)

const arr100=[];
const arr20=[];
const arr10=[];
const arr5=[];
const arr1=[];
const arr025=[];
const arr010=[];
const arr005=[];
const arr001=[];

// console.log(change,frUnidade)

let valor = Math.abs(change);
let cont=0;
while(valor>=0 && cont<2500){
  cont++
  if(valor>=100){
    arr100.push(1)
    valor-=100
  }
  else if(valor<100 && valor>=20){
    arr20.push(1);
    valor-=20
  }
  else if(valor<20 && valor>=10){
    arr10.push(1);
    valor-=10
  }
  else if(valor<10 && valor>=5){
    arr5.push(1);
    valor-=5
  }
  else if(valor<5 && valor>=1){
    arr1.push(1);
    valor-=1
  }
  else if(valor<1 && valor>=0.25){
    arr025.push(1);
    valor-=0.25
  }
  else if(valor<0.25 && valor>=0.1){
    arr010.push(1);
    valor-=0.1
  }
  else if(valor<0.1 && valor>=0.05){
    arr005.push(1);
    valor-=0.05
  }
  else if(valor<0.05 && valor>=0.01){
    arr001.push(1);
    valor-=0.01
  }
}

const arrStatusChange = [
  ['ONE HUNDRED',arr100.length*100],
  ['TWENTY',arr20.length*20],
  ['TEN',arr10.length*10],
  ['FIVE',arr5.length*5],
  ['ONE',arr1.length],
  ['QUARTER',arr025.length*0.25],
  ['DIME',arr010.length*0.1],
  ['NICKEL',arr005.length*0.05],
  ['PENNY',arr001.length*0.01],

];

arrStatusChange.sort((a,b)=>b[1]-a[1])
// console.log(arrStatusChange)

const obj = {status:status,change:arrStatusChange}
console.log(change)
console.log(obj)

}

checkCashRegister(19.5, 20, [["PENNY", 0.5], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 0], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]])

