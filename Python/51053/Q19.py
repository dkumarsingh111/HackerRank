class A: pass
class B(A): pass
class C(object): pass
class D(C): pass


a = A()
b = B()
c = C()
d = D()

print(isinstance(a, type(b)))   #Output: False
print(issubclass(C,C))          #Output: True
print(isinstance(d,D))          #Output: True
print(issubclass(C, (D,A,B,C))) #Output: True