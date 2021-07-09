import time
t1 = time.time()
ks = 0
while True:
    n = input()
    if n=="0":
        break
    ks = ks + len(n)

t2 = time.time()
if t2-t1 < 10:
    print("Please type atleast 10 sec")
else:
    ans = (ks*60)/(t2-t1)
    print(ans, "keystroke per minute")
