i = [12, 9, 14]
k = [7, 16, 11]
for j in i[:]: 
    for m in k[:]:
        if(j%m ==0):
            j=j//2
            m=m/j
            print(j,m)

        else:
            j = j+m
            m = m-j
            print(j,m)

#OUTPUT:
            # 19 -12
            # 35 -19
            # 46 -35
            # 16 -9
            # 8 2.0
            # 19 -8
            # 7 1.0
            # 23 -7
            # 34 -23