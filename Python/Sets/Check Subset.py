# Enter your code here. Read input from STDIN. Print output to STDOUT

T = int(input())

for i in range(T):
    nA = int(input())
    A = set(map(int, input().split()))
    nB = int(input())
    B = set(map(int, input().split()))

    if A.issubset(B):
        print(True)
    else:
        print(False)    
