import os
x = "/home/sam/Desktop/nf/"

import slate
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

a = listdir_fullpath(x)
pdfs = []
for i in a:
	pdfs.append(listdir_fullpath(i)[0])

final = []
for i in pdfs:
	with open(i) as f:
		x = slate.PDF(f)
		try:
			txt = x[0].split()
			cpi=x[0].split()[-8]
			
			roll=x[0].split()[19][1:]
			if len(cpi)!=4:
				print i
			# print x[0].split()
			ns= 0
			ne = 0
			for j in range(len(txt)):
				if "NAME" in txt[j]:
					ns=j+1
				if "DISCIPLINE" in txt[j]:
					ne= j
			txt[ns] = txt[ns][1:]
			name = " ".join(txt[ns:ne])
			final.append([cpi,roll,name])		

		except:
			print i	
final.sort(reverse=True)
f = open("sorted1.csv","w")
for i in final:
	f.write(i[0]+","+i[1]+","+i[2]+"\n")