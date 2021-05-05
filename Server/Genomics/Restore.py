import paramiko

def getConnectionConfig():
    CLUSTER_HOST = 'sge180.bgu.ac.il'
    CLUSTER_USER = 'chanana'
    CLUSTER_PASSWORD = 'pilpI108'
    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD

def exist_in_cluster(date_time):

    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)

    file_to_search = '{}_hanan_output.csv'.format(date_time)
    hanan_cluster_path = "cd PathoSearch/ML-Scripts && "
    exec_command = "search_csv_output.sh " + file_to_search
    cmd = hanan_cluster_path + exec_command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('Searching for file in Cluster')
    msg = stderr.readlines()
    print(msg)

    if (msg == "Exist"):
        server_hanan_output_path = './Data/Hanan_Output/{}_hanan_output.csv'.format(date_time)
        sftp = client.open_sftp()
        cluster_output_path = "./PathoSearch/ML-Scripts/DataOutput/{}.csv".format(date_time)
        while not os.path.exists(server_hanan_output_path):
            try:
                print('Trying to copy file from Genomics to Server...')
                sftp.get(cluster_output_path, server_hanan_output_path)
            except IOError or paramiko.SSHException:
                time.sleep(5)
                print('Waiting 5 secs for re-copying')
                break
        client.close()

def process_request(request):
    timestamp = request.query_string
    output = exist_in_cluster(timestamp)
    return output