class A:

    def __init__(self, i=1):
        self.i = i


class B(A):
    
    def __init__(self, j=2):
        super().__init__()
        self.j = j

    def main():
        b = B()
        print(b.i, b.j)


main()