f = open("data.txt", "r")
data = f.read().split("#")
data.remove("")
t = data[0]
v = data[1]
c = data[2]
s = data[3]

e = t.split("\n")
for en in e:
	if "//" in en or en == "":
		continue
	p = en.split()
	print p
print 'Done'

e = v.split("\n")
for en in e:
	if "//" in en or en == "":
		continue
	p = en.split()
	print p
print 'Done'

e = c.split("\n")
for en in e:
	if "//" in en or en == "":
		continue
	p = en.split()
	print p
print 'Done'

e = s.split("\n")
for en in e:
	if "//" in en or en == "":
		continue
	p = en.split()
	print p
print 'Done'