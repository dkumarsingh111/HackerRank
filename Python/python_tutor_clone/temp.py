def fib(limit):
    a, b = 0, 1
    while b < limit:
        yield b
        a, b = b, a + b

# Create a generator object
x = fib(200)

# Iterate over the generator object and print each value
for i in x:
    print(i)
