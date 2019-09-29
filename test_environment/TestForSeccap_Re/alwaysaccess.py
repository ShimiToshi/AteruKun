import subprocess
import time

cmd = "curl"
opt = "-L"
address = "192.168.1.12:8000"
tp = 0.1

flag = True

while flag:
	subprocess.call([cmd, opt, address])
	print()
	time.sleep(tp)
