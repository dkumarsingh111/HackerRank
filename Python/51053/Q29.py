def f1(a, b):
    f1.s = 'some value'
    return a+b

try:
    print(f1.s)
except Exception as e:
    print(str(e))


f1(3,4)

try:
    print(f1.s)
except Exception as e:
    print(str(e))


#Output:
        # 'function' object has no attribute 's'
        # some value