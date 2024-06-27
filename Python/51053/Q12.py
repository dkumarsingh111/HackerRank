import warnings

def deprecated(func):
    def newFunc(*args, **kwargs):
        warnings.warn('Call to deprecated function {}'.format(func.__name__), category=DeprecationWarning)
        return func(*args, **kwargs)
    return newFunc


@deprecated
def prod(x,y):
    'Returns product of two numbers'
    return x * y


print(prod(12, 12))
print(prod.__name__)
print(prod.__doc__)


# Output is:
#             144
#             newFunc
#             None