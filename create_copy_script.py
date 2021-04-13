import mysql.connector
import sys
import os
import time
import shutil

import win32console, win32gui, win32con

###########################################################################
# DISABLE WINDOW CLOSE OPTION                                             #
###########################################################################
hwnd = win32console.GetConsoleWindow()
if hwnd:
   hMenu = win32gui.GetSystemMenu(hwnd, 0)
   if hMenu:
       win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
###########################################################################       

if(len(sys.argv) < 2):
    
    print("Script ID is not passed")
    quit()

script_id = sys.argv[1]

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MyPasswordNew",
  database="create_copy"
)

mycursor = mydb.cursor()

sql_1_script_id = "scripts.id"
sql_1_script_name = "scripts.name"
sql_1_process_id = "scripts.process_id"
sql_1_src_name = "servers.name as source_server"
sql_1_src_path = "servers.path as source_path"
sql_1_dest_id = "scripts.destination_id"

sql_1 = "SELECT "+ sql_1_script_id + "," + sql_1_script_name + "," +sql_1_process_id + "," +sql_1_src_name + "," + sql_1_src_path + "," +sql_1_dest_id + " FROM scripts JOIN servers ON scripts.source_id=servers.id WHERE scripts.id = " + script_id


sql_script_id = "scripts1.id as script_id"
sql_script_name = "scripts1.name as script_name"
sql_src_name = "scripts1.source_server"
sql_src_path = "scripts1.source_path"
sql_dest_name = "servers.name as destination_server"
sql_dest_path = "servers.path as destination_path"

sql = "SELECT " + sql_script_id + "," + sql_script_name + "," + sql_src_name + "," + sql_src_path + "," + sql_dest_name + "," + sql_dest_path + " FROM servers JOIN ( "+sql_1+") as scripts1 ON servers.id = scripts1.destination_id"

mycursor.execute(sql)

myresult = mycursor.fetchall()

if(len(myresult) == 0):
    print("Script not found")

for x in myresult:
  script_id = x[0]
  script_name = x[1]
  src_name = x[2]
  src = x[3]
  dest_name = x[4]
  dest = x[5]
  
#############################################
# Check destination directory exists or not #
#############################################
if(not os.path.isdir(dest)):
  print("Directory path is invalid !!!")
  quit()


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

print("Script Name : " + script_name)
print("Source: " + src_name + " |path:[ "+ src +" ]")
print("Destination: " + dest_name + " |path:[ "+ dest +" ]")
print("Listening and copying ... ")

sql2 = "UPDATE scripts SET process_id = " + str(os.getpid()) + " WHERE id = " + str(script_id)

mycursor.execute(sql2)

mydb.commit()

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

sql2 = "UPDATE scripts SET process_id = 0 WHERE id = " + str(script_id)

mycursor.execute(sql2)

mydb.commit()
  

    
  