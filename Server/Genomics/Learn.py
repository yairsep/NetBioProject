import os, paramiko

def getConnectiionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD

def execute_ML_module(date_time):
    #Send cadd & trace output to ML Module
    print("Execute ML Module")
    # Initiating a ssh client protocol
    # CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD = getConnectiionConfig()
    #
    # client = paramiko.SSHClient()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.load_system_host_keys()
    # client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    # print('Connected to Remote host by SSH')
    # # clusterSessionDir = os.path.join(CLUSTER_SESSIONS_DIR, userName, jobName + '_' + time_str)
    # cmd = 'cd PathoSearch && python script.py'
    # # args = os.path.join(clusterSessionDir, 'conf.json')
    # # cmd = cmd
    #
    # # Executing the command
    # stdin, stdout, stderr = client.exec_command(cmd)
    # print('SSH Command Was executed')
    # msg = stderr.readlines()
    # print(msg)
    # client.close()