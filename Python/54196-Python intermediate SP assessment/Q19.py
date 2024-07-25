class A:
    def __init__(self, i=0):
        self.i = i


class B(A):
    def __init__(self, j=0):
        super().__init__()
        self.j = j

    def main():
        b = B(50)
        print(b.i, b.j)


B.main()

#Output: 0 50