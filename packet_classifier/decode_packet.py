import subprocess

packet_file = ""
open_key = ""

cmd = "openssl -e DHE-RSA-AES256-GCM-SHA384 -in test.pk -out abc.txt"
proc = subprocess.check_output()
print(proc)
