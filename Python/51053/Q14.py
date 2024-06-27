def check_twice1(lst, elm):
    return lst.count(elm) > 1

def check_twice2(lst, elm):
    return (elm in lst and elm in lst[lst.index(elm)+1:])

def check_twice3(lst, elm):
    c = 0
    for x in lst:
        if x == elm: c += 1
    return c

def check_twice4(lst, elm):
    try:
        lst.remove(elm)
        lst.remove(elm)
    except:
        return False
    return True   


lst = [1, 2, 2, 3, 4]
elm = 2

print(check_twice1(lst, elm)) #output: True
print(check_twice2(lst, elm)) #output: True
print(check_twice3(lst, elm)) #output: 2
print(check_twice4(lst, elm)) #output: True