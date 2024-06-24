def minion_game(string):
    # your code goes here
    n = len(string)
    combinations = ((n)*(n+1))/2
    player1 = 0
    player2 = 0    
    player2 = sum([len(string[i:]) for i in range(len(string)) if string[i] in "AEIOU"])
    player1 = combinations - player2
    
    if player1 == player2:
        print("Draw")
    elif player1 > player2:
        print("Stuart", int(player1))
    else:
        print("Kevin", int(player2))


if __name__ == '__main__':
    s = input()
    minion_game(s)