class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    

try:
    print('Hello World!')
    raise MyError('Oops something went wrong')
except MyError as e:
    print('Error Message: ', e)


#Output:
    # Hello World!
    # Error Message:  'Oops something went wrong'