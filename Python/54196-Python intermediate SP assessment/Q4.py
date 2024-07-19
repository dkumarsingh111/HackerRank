import sys

try:
    f = open('textFile.txt')
    s = f.readline()
    l = int(s.strip())

except IOError as e:
    print("I/O error({0}):{1}".format(e.errno, e.strerror))

except ValueError:
    print("Could not convert data to an integer.")
    raise

except:
    print("Unexpected error:", sys.exc_info()[0])

finally:
    print("finally executed..")


#Output:
    # I/O error(2):No such file or directory
    # finally executed..