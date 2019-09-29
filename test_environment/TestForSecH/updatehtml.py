import subprocess
import time

wordcount = 10
tp = 0.1

def make_html(string):
	sepstr = string.split(" ")
	i = 0
	flag = True
	while(flag):
	
		usewords = sepstr[i * wordcount: (i+1)*wordcount]

		if (i+1) * wordcount >= len(sepstr):
			usewords = sepstr[i * wordcount: len(sepstr)]
			flag = False
		retstr = " ".join(usewords)
		
		with open("index.html", "w") as f:
			f.write(retstr)
		i += 1
		print(flag, retstr)
		time.sleep(tp)
	

make_html("a b c d e f g h i j k l m n o p q r s t u v w x y z")
