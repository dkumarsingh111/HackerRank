def factorial1(N):
    return N if N == 1 else N * fact1(N-1)


def factorial2(N):
    res = 1
    for i in range(1, N+1):
        res *= i
    return res


def factorial3(N):
    if N == 1:
        return N
    else:
        return N * fact0(N-1)

        

def fact0(X):
    res = 1
    for i in range(1, X+1):
        res *= i
    return res


def fact1(X):
    res = 1
    for i in range(1, X+1):
        res *= i
    return res


print(factorial1(10))
print(factorial2(10))
print(factorial3(10))