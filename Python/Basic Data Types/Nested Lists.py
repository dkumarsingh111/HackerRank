if __name__ == '__main__':

    students = []
    for _ in range(int(input())):
        name = input()
        score = float(input()) 
        students.append([name, score])

    for i in range(len(students)):
        for j in range(i, len(students)):
            if students[i][1] > students[j][1]:
                    temp = students[i]
                    students[i] = students[j]
                    students[j] = temp

            if students[i][1] == students[j][1]:
                    if students[i][0] > students[j][0]:
                        temp1 = students[i]
                        students[i] = students[j]
                        students[j] = temp1        

    new_list = []
    for i in range(len(students)):
        if students[i][1] != students[0][1]:
            new_list.append(students[i])
    
    for i in range(len(new_list)):
        if new_list[i][1] == new_list[0][1]:
             print(new_list[i][0])