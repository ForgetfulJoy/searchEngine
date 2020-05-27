
with open('1.json','r') as d:
    str=d.read()
print(str)
str.replace("[","")
str.replace("]","")
print(str)
with open('1.json','w') as w:
    w.write(str)