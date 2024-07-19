'''
Select the correct program to transpose value to key
'''


# capitals = {
#     'United States':'Washington, DC', 'France':'Paris', 'Italy':'Rome'
# }

# capitals_bycapital = {}
# for key, value in capitals.items():
#     capitals_bycapital.append({capitals[key], key})



# capitals = {
#     'United States':'Washington DC', 'France':'Paris', 'Italy':'Rome'
# }

# capitals_bycapital = {}
# for k, v in capitals.items():
#     capitals_bycapital[v].append(k)



capitals = {
    'United States':'Washington DC', 'France':'Paris', 'Italy':'Rome'
}

inverted_dict = {}
for key in capitals:
    inverted_dict.setdefault(capitals[key], []).append(key)


print(inverted_dict) 



capitals = {
    'United States':'Washington DC', 'France':'Paris', 'Italy':'Rome'
}

capitals_bycapital = {capitals[key]:key for key in capitals}
print(capitals_bycapital)
