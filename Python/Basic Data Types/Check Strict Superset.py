A = set(map(int, input().split()))
n = int(input())
is_strict_superset = False

for i in range(n):
    B = set(map(int, input().split()))
    if B.issubset(A):
        is_strict_superset = True
    else:
        is_strict_superset = False
        break

print(is_strict_superset)