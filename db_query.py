import mysql.connector
import json
from uuid import uuid1
from datetime import datetime

class DB_Query:

    def __init__(self,db_config_file_name):

        with open(db_config_file_name) as f:
            db = json.load(f)
        
        self.db = mysql.connector.connect(
            host= db['host'],
            user= db['user'],
            password= db['pwd'],
            database= db['name']
            )
        
        self.cursor = self.db.cursor()    

    def getScriptInDetails(self,script_id):

        

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

        self.cursor.execute(sql)

        result = self.cursor.fetchall()     

        return result  
    
    def getScriptBackupDetails(self,script_id):
        
        sql = "SELECT backup_dirs.backup_dir_path as backup_path, backup_dirs.backup_dir_name as backup_name, backup_dirs.backup_process_id, backup_dirs.id as id, scripts1.id as script_id, scripts1.name as script_name, scripts1.process_id as process_id, scripts1.source_server as source_server, scripts1.source_path as source_path FROM backup_dirs JOIN (SELECT scripts.id, scripts.name, scripts.process_id, servers.name as source_server, servers.path as source_path FROM scripts JOIN servers ON scripts.source_id=servers.id) as scripts1 ON backup_dirs.script_id = scripts1.id"

        self.cursor.execute(sql)

        result = self.cursor.fetchall()     
        if len(result) > 0:
            return result[0] 
        
        return False    
    
    def updateScriptProcessStatus(self,pid,script_id):

        sql2 = "UPDATE scripts SET process_id = " + str(pid) + " WHERE id = " + str(script_id)

        self.cursor.execute(sql2)

        self.db.commit()

    def updateBackupProcessStatus(self,pid,script_id):

        sql2 = "UPDATE backup_dirs SET backup_process_id = " + str(pid) + " WHERE script_id = " + str(script_id)

        self.cursor.execute(sql2)

        self.db.commit()       

    def fileInScriptLog(self,script_id,filename):

        sql = "SELECT * FROM script_log_" + str(script_id) + " WHERE copied_file = '"+filename+"'"    

        self.cursor.execute(sql)

        result = self.cursor.fetchall() 

        if(len(result) > 0):
            return True    

        return False

    def uniqueID(self,script_id):
        
        

        while(True):
            id = uuid1().hex

            sql = "SELECT * FROM script_log_" + str(script_id) + " WHERE id = '"+id+"'"

            self.cursor.execute(sql)

            result = self.cursor.fetchall() 

            if(len(result) < 1):
                return id    


    def addToLog(self,script_id,filename):

        current_time = datetime.now().strftime('%H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')

        sql = "INSERT INTO script_log_" + str(script_id) + "(id,copied_file,on_date,at_time) VALUES('" + self.uniqueID(script_id) + "','"+filename+"','" + current_date + "','" + current_time + "')"    

        self.cursor.execute(sql)

        self.db.commit()

    def getBackupPath(self,script_id):

        sql = "SELECT * FROM backup_dirs WHERE script_id = '"+str(script_id)+"'"

        self.cursor.execute(sql)

        result = self.cursor.fetchall() 
        
        if(len(result) > 0):
            return result[0]

        return False

    def removeFromLog(self,script_id,filename):

        sql = "DELETE FROM script_log_" + str(script_id) + " WHERE copied_file = '"+filename+"'"    

        self.cursor.execute(sql)

        self.db.commit()        
