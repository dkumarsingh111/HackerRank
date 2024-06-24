if __name__ == '__main__':
    N = int(input())
    newList = []
    
    for i in range(N):
        arr = list(input().split(" "))
        
        if arr[0] == "insert":
            newList.insert(int(arr[1]), int(arr[2]))

        elif arr[0] == "print":
            print(newList)
            
        elif arr[0] == "remove":
            newList.remove(int(arr[1]))

        elif arr[0] == "append":
            newList.append(int(arr[1]))

        elif arr[0] == "sort":
            newList.sort()

        elif arr[0] == "pop":
            newList.pop()

        elif arr[0] == "reverse":
            newList.reverse()