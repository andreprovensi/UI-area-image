

def countup(n):

    if n<1:
        return []
    else:
        
        countArray = countup(n-1)
        print('depois',countArray)
        countArray.append(n)
        return countArray



countup(3)

a =1


import numpy as np

print(np.linspace(0,50,50))