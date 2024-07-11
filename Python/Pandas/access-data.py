import pandas as pd
import numpy as np
z = np.arange(10, 16)
s = pd.Series(z, index=list('abcdef'))
#Accessing 3rd element of s.
print(s[2]) # ---> Returns '12' 
#Accessing 4th element of s.
print(s['d']) # ---> Returns '13'


'''It is also possible to access a single element by passing index number or index value, 
as an argument to get method.'''

print(s.get(2)) # ---> Returns '12'
print(s.get('d')) # ---> Returns '13'


'''A Series can be sliced in a way, very similar to slicing a python list.'''


print(s[1:4])
print(s['b':'e'])
