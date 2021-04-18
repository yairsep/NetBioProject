import paramiko , os , time
from scp import SCPClient

def getConnectionConfig():
    CLUSTER_HOST = 'sge180.bgu.ac.il'
    CLUSTER_USER = 'interactomenetprod'
    CLUSTER_PASSWORD = 'bgu2010'
    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD


def execute_ML_module(date_time):
    # Send cadd & trace output to ML Module
    print("Initiating Connection with Cluster")

    # Initiating a ssh client protocol
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)

    # Moving Outputs from CADD & Trace to Cluster
    # TODO: Check about tsv output file
    cadd_output_csv = "./Data/Cadd_Output/{}.tsv".format(date_time)
    trace_output_csv = "./Data/Trace_Output/{}.csv".format(date_time)
    # TODO: Complete path here
    cluster_output_path = "./PathoSearch/ML-Scripts/DataInput"
    scp = SCPClient(client.get_transport())
    print("Coping CADD output to Cluster...")
    scp.put(cadd_output_csv, cluster_output_path)
    print("Coping Trace output to Cluster...")
    scp.put(trace_output_csv, cluster_output_path)

    # Executing Hanan Algorithem
    print("Executing Hanan algorithem...")
    cadd_cluster_path = "./PathoSearch/ML-Scripts/DataInput/{}.tsv".format(date_time)
    trace_cluster_path = "./PathoSearch/ML-Scripts/DataInput/{}.csv".format(date_time)
    hanan_cluster_path = "cd PathoSearch/ML-Scripts && "

    # TODO: Check Hanan execute configuration
    
    exec_command = "python script.py" + cadd_cluster_path + trace_cluster_path
    cmd = hanan_cluster_path + exec_command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('SSH Command in Cluster Was executed')
    msg = stderr.readlines()
    print(msg)

    # Coping Hanan algo output to server

    server_hanan_output_path = './Data/Hanan_Output/{}_output.tsv'.format(date_time)
    sftp = client.open_sftp()
    hanan_output_csv = "./Data/Hanan_Output"
    while not os.path.exists(server_hanan_output_path):
        try:
            print('Trying to copy file from Genomics to Server...')
            sftp.get(cluster_output_path, hanan_output_csv)
        except IOError or paramiko.SSHException:
            time.sleep(5)
            print('Waiting 5 secs for re-copying')
            break
    client.close()

# TODO: Complete parsing CSV to Json
def getOutput(date_time):
    json_output = {}
    with open("./Data/Hanan_Output/{}_hanan_output.tsv".format(date_time)) as input_file:
        print(input_file)
    return json_output
