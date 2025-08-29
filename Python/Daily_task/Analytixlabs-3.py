def weird_functionn(x=[]):
    x.append(1)
    return x


print(weird_functionn())
print(weird_functionn())
print(weird_functionn())

# Ans:
# [1]
# [1, 1]
# [1, 1, 1]