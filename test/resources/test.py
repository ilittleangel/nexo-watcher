import setproctitle
import sys
import time

times = sys.argv[1]
setproctitle.setproctitle('test.py')

i = 1
while i <= int(times):
    print(i)
    i += 1
    time.sleep(1)

print("bye\n")
