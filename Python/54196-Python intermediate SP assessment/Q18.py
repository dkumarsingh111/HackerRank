class A:
    def __init__(self, param):
        self.a1=param


class B(A):
    def __init__(self, param):
        self.b1=param



obj=B(100)
print("%d %d" % (obj.a1, obj.b1))

#Output: Error is generated