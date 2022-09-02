
string1 = 'ab'

string2 = 'abcccccca'

soma = 0

lista_soma = []

for char1 in string1:

    soma=0
    for char2 in string2:

        if char1 == char2:
            soma+=1
    lista_soma.append(soma)


n = min(lista_soma)

print(n)


forb = ['(]','(}','[)', '[}', '{)', '{]']

sequence = '([([)])[]'
state = None
for index, value in enumerate(sequence):

    if index != len(sequence)-1:

        if sequence[index]+sequence[index+1] in forb:
            state = False
            break

        else:
            state = True

print(state)    

sequence = [1,2,3,4,5]


new_list = sequence.copy()

new_list.pop(2)

print(bool(1))

a = '+'

mylist = [1,2,1,2]

   
        
        
        
        
        

