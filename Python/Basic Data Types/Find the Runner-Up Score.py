if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    
    newList = list(set(arr))  

    for i in range(len(newList)):
        for j in range(i, len(newList)):
            if newList[i] > newList[j]:
                temp = newList[i]
                newList[i] = newList[j]
                newList[j] = temp

    print(newList[len(newList)-2])       