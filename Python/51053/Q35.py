import re
def f1(data):
    p = re.compile('(?P[A-Z]{2,3}) (?P[0-9]{3})')
    return p.search(data)





# obj = f1('CS 101')
# dept, num = obj.group('dept'), obj.group('num')