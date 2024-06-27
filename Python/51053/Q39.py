def foo(n):
    if (n < 3): yield 1
    else: return
    yield 2


n = 2
f = foo(n)
for i in range(n): print(f.__next__())


n = 5
f = foo(n)
for i in range(n): print(f.__next__())


#Output:
        # 1
        # 2
        # Traceback (most recent call last):
        # File "c:\Users\10278018\OneDrive - BD\100-Days-of-Code-The-Complete-Python-Pro-Bootcamp\51053\Q39.py", line 13, in <module>
        #     for i in range(n): print(f.__next__())
        #                             ^^^^^^^^^^^^
        # StopIteration