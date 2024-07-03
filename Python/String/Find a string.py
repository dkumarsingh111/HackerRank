def count_substring(string, sub_string):
    if string.find(sub_string) > 0:
        return string.find(sub_string)
    else:
        return 0 

if __name__ == '__main__':
    string = input().strip()
    sub_string = input().strip()

    count = count_substring(string, sub_string)
    print(count)