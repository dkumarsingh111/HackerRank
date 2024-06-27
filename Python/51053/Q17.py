class Person(object):
    def __init__(self, name):
        print("My name is ", name)


class Bob(Person):
    def __init__(self, name='Bob'):
        print(f'My name is Bob')

    def ClassID(self):
        print("I'm the father")


class Sue(Person):
    def __init__(self, name='Sue'):
        print('My name is Sue')

    def ClassID(self):
        print("I'm the mother")   


class Child(Bob, Sue):
    def __init__(self, name='X'):
        super(Child, self).__init__(name)

    def ClassID(self):
        print("I'm the child")


Ann = Child('Ann')
Ann.ClassID()


# Output: 
#         My name is Bob
#         I'm the child