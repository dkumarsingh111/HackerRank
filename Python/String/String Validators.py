if __name__ == '__main__':
    s = input()

    is_alphanumeric = False
    is_alphabetical = False
    is_digits = False
    is_lowerChar = False
    is_upperChar = False

    for i in range(len(s)):
        substr1 = s[i:len(s)]
        substr2 = s[0:i]

        if substr1.isalnum() or substr2.isalnum():
            print(f"{substr1} ---- {substr2}")
            is_alphanumeric = True

        if s[i].isalpha():
            is_alphabetical = True

        if s[i].isdigit():
            is_digits = True

        if s[i].islower():
            is_lowerChar = True

        if s[i].isupper():
            is_upperChar = True


    print(is_alphanumeric)
    print(is_alphabetical)
    print(is_digits)
    print(is_lowerChar)
    print(is_upperChar)