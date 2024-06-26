primes = [2,3,5,7,11,13,17,19,23,29]
squared_primes = [x*x for x in primes if x%10 == 3]
print(squared_primes)


# output: [9, 169, 529]