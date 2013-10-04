import string

fp = open("inp", "r")
strset = []
while True:
	str = string.rstrip(fp.readline(), "\n")
	if str == "":
		break
	strset = strset + [int(str)]
	print strset
	print strset[0:2]
