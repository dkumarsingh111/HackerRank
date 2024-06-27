class Base1(object):
    def __init__(self):
        print('Base1 Created')

class Child1(Base1):
    def __init__(self):
        super(Child1).__init__()
        print('Child1 Created')

b1 = Base1()
c1 = Child1()

#Output:
        # Base1 Created
        # Child1 Created

#-----------------------------------------------------------------------#


class Base2(object):
    def __init__(self):
        print('Base2 Created')

class Child2(Base2):
    def __init__(self):
        Child2.__bases__[0].__init__(self)
        print('Child2 Created')

b2 = Base2()
c2 = Child2()


#Output:
        # Base2 Created
        # Base2 Created
        # Child2 Created

#-----------------------------------------------------------------------#


class Base3(object):
    def __init__(self):
        print('Base3 Created')

class Child3(Base3):
    def __init__(self):
        super(Child3, self).__init__()
        print('Child3 Created')

b3 = Base3()
c3 = Child3()

#Output:
        # Base3 Created
        # Base3 Created
        # Child3 Created

#-----------------------------------------------------------------------#


class Base4(object):
    def __init__(self):
        print('Base4 Created')

class Child4(Base4):
    def __init__(self):
        super().__init__()
        print('Child4 Created')

b4 = Base4()
c4 = Child4()

#Output:
        # Base4 Created
        # Base4 Created
        # Child4 Created