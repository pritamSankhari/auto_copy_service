import sys
import os
import time
import shutil

import win32console, win32gui, win32con
import json
from db_query import DB_Query
from datetime import datetime

import msvcrt

def throwError(msg,exitFlag,forceExit = False):
  print(msg)
  print("Press any key to terminate ...")

  if not forceExit:
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
    throwError(msg="Script ID is not passed",exitFlag=True,forceExit=True)
    

script_id = sys.argv[1]

query = DB_Query('config\db_py_config.json')

myresult = query.getScriptInDetails(script_id)

if(len(myresult) == 0):
    throwError(msg="Script not found",exitFlag=True,forceExit=True)
    

for x in myresult:
  script_id = x[0]
  script_name = x[1]
  src_name = x[2]
  src = x[3]
  dest_name = x[4]
  dest = x[5]

print("Script Name : " + script_name)
print("Source: " + src_name + " |path:[ "+ src +" ]")
print("Destination: " + dest_name + " |path:[ "+ dest +" ]")



#############################################
# Check source directory exists or not #
#############################################
if(not os.path.isdir(src)):
  query.updateScriptProcessStatus(-1,script_id)
  throwError(msg= src +" directory(source)  does not exist !",exitFlag=True,forceExit=True)
  
#############################################
# Check destination directory exists or not #
#############################################
if(not os.path.isdir(dest)):
  query.updateScriptProcessStatus(-1,script_id)
  throwError(msg= dest +" directory(destination) does not exist !",exitFlag=True,forceExit=True)
  


##############################################
# Set the tmp_dst_file name in src directory #
##############################################
tmp_dest = src +"\\tmp_" + dest_name.replace(' ','_') + ".txt"




print("Listening and copying ... ")

query.updateScriptProcessStatus(os.getpid(),script_id)

try:
  while True:
    time.sleep(5)

    #####################################
    # get file list in source directory #
    #####################################
    src_all_files = os.listdir(src)

    copied = 0
    current_time = datetime.now().strftime('%H:%M:%S')

    for src_file in src_all_files:
      
      if not query.fileInScriptLog(script_id,src_file):
        
        os.system("cls")
        print("Script Name : " + script_name)
        print("Source: " + src_name + " |path:[ "+ src +" ]")
        print("Destination: " + dest_name + " |path:[ "+ dest +" ]")
        print("Listening and copying ... ")

        #############
        # copy file #
        #############
        shutil.copyfile(src + "\\" + src_file , dest + "\\" + src_file)
        copied = copied + 1
        
        query.addToLog(script_id,src_file)

        print("Copied " + str(copied) + " file(s) at " + current_time)

    

except KeyboardInterrupt:
  print('Service has been ended')

query.updateScriptProcessStatus(0,script_id)
  

    
  