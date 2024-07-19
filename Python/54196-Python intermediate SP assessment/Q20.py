class A:
    def __init__(self,x):
        self.x = x


a=A(100)
a.__dict__['y']=50
print(a.x+len(a.__dict__))