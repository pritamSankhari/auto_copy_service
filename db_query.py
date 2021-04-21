import mysql.connector
import json

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

    def updateScriptProcessStatus(self,pid,script_id):

        sql2 = "UPDATE scripts SET process_id = " + str(pid) + " WHERE id = " + str(script_id)

        self.cursor.execute(sql2)

        self.db.commit()