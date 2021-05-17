import sys
import os
import time
import shutil

import win32console, win32gui, win32con
import json
from db_query import DB_Query

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


##########################################################
# create the tmp_dst_file  in src directory if not exist #
##########################################################
if(not os.path.isfile(tmp_dest)):
  
  tmp_file = open(tmp_dest,"a+")
  
  print("tmp file has been created !")
  
  tmp_file.write("tmp_" + dest_name.replace(' ','_') + ".txt")
  
  tmp_file.close()

print("Listening and copying ... ")

query.updateScriptProcessStatus(os.getpid(),script_id)

try:
  while True:
    time.sleep(5)

    #####################################
    # get file list in source directory #
    #####################################
    src_all_files = os.listdir(src)

    ####################################################  
    # read the tmp file of destination dest            #
    # get all file name lists which are already copied #
    ####################################################
    tmp_file = open(tmp_dest,"r")  
    registered_files = tmp_file.readlines()
    tmp_file.close()
    stripped_registered_files = list(map(str.strip, registered_files))

    for src_file in src_all_files:
      
      if src_file not in stripped_registered_files:
        
        if src_file.find('tmp') != -1 :
          break
        #############
        # copy file #
        #############
        shutil.copyfile(src + "\\" + src_file , dest + "\\" + src_file)

        #########################################################
        # register or append the file name to the tmp_dest file #
        #########################################################
        tmp_file_a = open(tmp_dest,"a")  
        tmp_file_a.write("\n"+src_file)
        print("file: " + src_file + " has been copied")
        tmp_file_a.close()


except KeyboardInterrupt:
  print('Service has been ended')

query.updateScriptProcessStatus(0,script_id)
  

    
  