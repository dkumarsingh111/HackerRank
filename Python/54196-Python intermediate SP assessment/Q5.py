class A:
    def __init__(self):
        self.calculate(30)
        print("i in Class A is", self.i)

    def calculate(self, i):
        self.i = 2 * i


class B(A):
    def __init__(self):
        super().__init__()

    def calculate(self, i):
        self.i = 3 * i


b = B()


# Output: i in Class A is 90