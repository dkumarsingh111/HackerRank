class grandpa(object):
    pass

class father(grandpa):
    pass

class mother(object):
    pass


class child(mother, father):
    pass


print(child.__mro__)



#Output is
#(<class '__main__.child'>, <class '__main__.mother'>, <class '__main__.father'>, <class '__main__.grandpa'>, <class 'object'>)