import time
import os

print(os.getpid())
while True:
    time.sleep(2)
    print('Server is running ...')

