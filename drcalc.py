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
			cpi=x[0].split()[-8]
			
			roll=x[0].split()[19][1:]
			if len(cpi)!=4:
				print i	
			final.append([cpi,roll])
		except:
			print i	
final.sort(reverse=True)
f = open("sorted.csv","w")
for i in final:
	f.write(i[0]+","+i[1]+"\n")