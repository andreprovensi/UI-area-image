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


if(cashInDrawer<change){return {status:"INSUFFICIENT_FUNDS",change:[]}}
else if(cashInDrawer>change){status="OPEN";}
else if(cashInDrawer === change){status="CLOSED";}


const arr100=[];
const arr20=[];
const arr10=[];
const arr5=[];
const arr1=[];
const arr025=[];
const arr010=[];
const arr005=[];
const arr001=[];

let n001=Math.round(cid[0][1]/0.01);
let n005=Math.round(cid[1][1]/0.05);
let n010=Math.round(cid[2][1]/0.1);
let n025=Math.round(cid[3][1]/0.25);
let n1=Math.round(cid[4][1]);
let n5=Math.round(cid[5][1]/5);
let n10=Math.round(cid[6][1]/10);
let n20=Math.round(cid[7][1]/20);
let n100=Math.round(cid[8][1]/100);

let valor = Math.abs(change);
let cont=0;

while(valor>=0 && cont<25000){
  cont++
  valor = Math.round(valor*1000)/1000;
  if(valor>=100 && n100>0){
    arr100.push(1)
    valor-=100
    n100--
  }
  else if(valor>=20 && n20>0){
    arr20.push(1);
    valor-=20
    n20--
  }
  else if(valor>=10 && n10>0){
    arr10.push(1);
    valor-=10
    n10--
  }
  else if( valor>=5 && n5>0){
    arr5.push(1);
    valor-=5
    n5--
  }
  else if(valor>=1 && n1>0){
    arr1.push(1);
    valor-=1
    n1--
  }
  else if(valor>=0.25 && n025>0){
    arr025.push(1);
    valor-=0.25
    n025--
  }
  else if(valor>=0.1 && n010>0){
    arr010.push(1);
    valor-=0.1
    n010--
  }
  else if(valor>=0.05 && n005>0){
    arr005.push(1);
    valor-=0.05
    n005--
  }
  else if(valor>=0.01 && n001>0){
    arr001.push(1);
    valor-=0.01
    n001--
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

const possibleChange = arrStatusChange.reduce((acc,arr)=>acc+arr[1],0);

if(possibleChange < change){return {status:"INSUFFICIENT_FUNDS",change:[]}}

const obj = {status:status,change:cid}

if(status==="CLOSED"){return obj}


const filterdArrStatusChange = arrStatusChange.filter(arr=>arr[1]!==0);

return {status:status,change:filterdArrStatusChange}


}

checkCashRegister(19.5, 20, [["PENNY", 0.01], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 1], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]])
