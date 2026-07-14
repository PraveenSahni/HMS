import urllib.request
h = urllib.request.urlopen("http://127.0.0.1/").read().decode()
print(h)
for line in h.splitlines():
    if "script" in line and "assets" in line:
        print("SCRIPT_LINE", line.strip())
