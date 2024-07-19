def abc(val, y=[]):
    y.append(val)
    return y


print(abc(3))

print(abc(4, [1,2]))

print(abc(10))


#output: 
        # [3]
        # [1, 2, 4]
        # [3, 10]  