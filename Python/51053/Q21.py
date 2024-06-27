class class1:
    a = 1

    def f1():
        a = 2
        class1.a += 1
        print(class1.a)
        print(a)



class1.f1()
class1.f1()


#Output:
        # 2
        # 2
        # 3
        # 2