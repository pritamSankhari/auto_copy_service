import sys
import os
import time
import shutil
from datetime import datetime

import win32console, win32gui, win32con
import json
from db_query import DB_Query

import msvcrt

def throwError(msg,exitFlag = True):
  print(msg)
  print("Press any key to terminate ...")
  msvcrt.getch()
  
  if(exitFlag):
    quit()

###########################################################################
# DISABLE WINDOW CLOSE OPTION                                             #
###########################################################################
try:
  hwnd = win32console.GetConsoleWindow()
  if hwnd:
    hMenu = win32gui.GetSystemMenu(hwnd, 0)
    if hMenu:
        win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
except Exception:
  pass
###########################################################################       

if(len(sys.argv) < 2):
    throwError(msg="Script ID is not passed",exitFlag=True)
    

script_id = sys.argv[1]

query = DB_Query('config\db_py_config.json')

myresult = query.getScriptInDetails(script_id)

if(len(myresult) == 0):
    throwError(msg="Script not found",exitFlag=True)
    

for x in myresult:
  script_id = x[0]
  script_name = x[1]
  src_name = x[2]
  src = x[3]
  dest_name = x[4]
  dest = x[5]



#############################################
# Check source directory exists or not #
#############################################
if(not os.path.isdir(src)):
#   query.updateScriptProcessStatus(-1,script_id)
  throwError(msg= src +" directory(source)  does not exist !",exitFlag=True)

backup_dir ="D:\\San1_Data\\backup_for_test"

# current_date = temp_date = datetime.now().strftime('%Y-%m-%d')


last_time = current_time = datetime.now().strftime('%H_%M')
# last_time = current_time = datetime.now().strftime('%Y_%m_%d')


try:
    while True:
        
        # Interval for checking backup
        # time.sleep(300)
        time.sleep(10)

        print("Checking for backup ...")

        current_time = datetime.now().strftime('%H_%M')
        # current_time = datetime.now().strftime('%Y_%m_%d')

        src_all_files = os.listdir(src)
        
        # if current time or date is greater than last backup time or date
        if(current_time > last_time):
            
            backup_dir_last = os.path.join(backup_dir, "backup_"+ last_time + "_" + src_name)
            os.mkdir(backup_dir_last)
            
            for src_file in src_all_files :
                
                file_full_name = os.path.join(src,src_file)

                # get created time or date
                created_time = os.path.getctime(file_full_name) 
                created_time = datetime.fromtimestamp(created_time).strftime('%H_%M')
                # created_time = datetime.fromtimestamp(created_time).strftime('%Y_%m_%d')

                #  if file created time or date less than current time or date
                if(created_time < current_time):

                    if src_file.find('tmp') != -1 :
                        continue
                    
                    # do backup
                    # copy file then remove file from the src directory    
                    shutil.copyfile(file_full_name , backup_dir_last + "\\" + src_file)
                    os.remove(file_full_name)

            
            print("Last Backup Done at " + current_time + " !")
            last_time = current_time

except KeyboardInterrupt:
    print('Auto Backup is Terminated')

throwError("Warning ! Auto Backup Service has been closed !")    