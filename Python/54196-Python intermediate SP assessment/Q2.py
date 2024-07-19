def country(*abc):
    if len(abc) == 1:
        item = abc[0]
        
        def f(obj):
            return obj[item]
        

    else:
        def f(obj):
            return tuple(obj[item] for item in abc)
    return f


selection = []

selection = country(slice(2, None))('AUSTRALIA')
print(selection)


#Output: STRALIA