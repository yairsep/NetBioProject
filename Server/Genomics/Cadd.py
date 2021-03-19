import os, paramiko

#TODO: Configurations

# LOCAL_SESSIONS_DIR = '/media/disk2/users/interactomenetprod/Websites/ClusterSessions/MyProteinNet2Sessions/'
# CLUSTER_SESSIONS_DIR = '/storage16/users/interactomenetprod/InteractomeNet/Sessions/MyProteinNet2Sessions/'
# CLUSTER_RUNNER = '/storage16/users/interactomenetprod/MyProteinNet2/RunMyProteinNet.py'
CLUSTER_HOST = 'genomics.bgu.ac.il'
CLUSTER_USER = 'estiyl'
CLUSTER_PASSWORD = 'H!ytfP7eq'


def execute_ssh(request):
    # Processing the request (all data from submitted file)
    processed_request = process_request(request)

    # Initiating a ssh client protocol

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    print('Connected to Remote host by SSH')
    # clusterSessionDir = os.path.join(CLUSTER_SESSIONS_DIR, userName, jobName + '_' + time_str)
    cmd = 'cd PathoSearch && python script.py'
    # args = os.path.join(clusterSessionDir, 'conf.json')
    # cmd = cmd

    # Executing the command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('SSH Command Was executed')
    msg = stderr.readlines()
    print(msg)
    client.close()


def process_request(request):
    print('Processed request')
    return 'data'
