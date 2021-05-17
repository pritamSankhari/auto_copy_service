# import datetime

# now = datetime.datetime.now()

# print(now.strftime("%X"))

# import os
# import zipfile
    
# zip_file = zipfile.ZipFile('temp.zip', 'w')
# zip_file.write('.', compress_type=zipfile.ZIP_DEFLATED)
# zip_file.close()

# zipf.close()

# from db_query import DB_Query

# db = DB_Query()

# print(db)

import os
import time
from datetime import datetime

ctime = os.path.getctime("e.txt")
mtime = os.path.getmtime("e.txt")
# c

# time.ctime(os.path.getmtime("d.txt"))
#strftime('%Y-%m-%d')
#strftime('%X')

# d = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
# ct = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
# mt = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
ct = datetime.fromtimestamp(ctime).strftime('%X')
mt = datetime.fromtimestamp(mtime).strftime('%X')

current_date = last_date = datetime.now().strftime('%Y-%m-%d')
last_time = current_time = datetime.now().strftime('%H:%M')


while True:
    time.sleep(2)
    
    # print(last_time)
    # print(current_time)

    print("Checking for backup ...")

    current_time = datetime.now().strftime('%H:%M')

    if(current_time > last_time):
        print("Last Backup Done at " + current_time + " !")
        last_time = current_time