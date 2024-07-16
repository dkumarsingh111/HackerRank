#while True:
try:
    fh=open("openfile", "w")
    fh.write("Write contet to file")

else:
    print("Else condition occured for")  

except:
    print("This is Exception")     

finally:
    print("Closing the file")
    fh.close()