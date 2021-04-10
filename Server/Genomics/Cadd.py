from scp import SCPClient
import os, paramiko, vobject

#TODO: Configurations

# LOCAL_SESSIONS_DIR = '/media/disk2/users/interactomenetprod/Websites/ClusterSessions/MyProteinNet2Sessions/'
# CLUSTER_SESSIONS_DIR = '/storage16/users/interactomenetprod/InteractomeNet/Sessions/MyProteinNet2Sessions/'
# CLUSTER_RUNNER = '/storage16/users/interactomenetprod/MyProteinNet2/RunMyProteinNet.py'

def getConnectiionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD

def execute_ssh_and_create_vsf(request):
    print("****************")
    print(type(request))
    vcard = vobject.readOne('\n'.join([f'{k}:{v}' for k, v in request.items()]))
    vcard.name = 'VCARD'
    #vcard.useBegin = True
    vcard.prettyPrint()
    with open('./test.vcf', 'w', newline='') as f:
        f.write(vcard.serialize())
    print("****************")
    # Processing the request (all data from submitted file)
    processed_request = process_request(request)

    # Initiating a ssh client protocol
    CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD = getConnectiionConfig()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    print('Connected to Remote host by SSH')
    # clusterSessionDir = os.path.join(CLUSTER_SESSIONS_DIR, userName, jobName + '_' + time_str)
    cmd = 'cd /mnt/disk1/CADD/test '
    stdin, stdout, stderr = client.exec_command(cmd)
    print('SSH Command Was executed')
    sftp  = client.open_sftp()
    
    print(sftp)
    a = sftp.put(r'C:\\Users\\Emi\\VSCode Projects\\Netbio\\NetBioProject\\Server\\hello.txt',r'\\mnt\\disk1\\CADD\\test')
    print(a)
    client.open_sftp().put(r'C:\\Users\\Emi\\VSCode Projects\\Netbio\\NetBioProject\\Server\\hello.txt',r'\\mnt\\disk1\\CADD\\test')
    # args = os.path.join(clusterSessionDir, 'conf.json')
    # cmd = cmd

    # Executing the command
    
    msg = stderr.readlines()
    print(msg)
    client.close()

def execute_ssh(request):
    # Processing the request (all data from submitted file)
    processed_request = process_request(request)

    # Initiating a ssh client protocol
    CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD = getConnectiionConfig()

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


def generate_vcf_file(vcf_string):
    f = open("./Utils/vcf_output.vcf", "a")
    #TODO: Parse string
    f.write(vcf_string)
    f.close()


def send_vcf_to_genomics(vcf_string):
    generate_vcf_file(vcf_string)
    print("Sending VCF file to CADD...")
    CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    scp = SCPClient(client.get_transport())
    # scp.put("./Utils/vcf_test.vcf" , "./PathoSearch")
    scp.put("./Utils/vcf_output.vcf" , "./PathoSearch")

    print("VCF file has been sent to Cadd successfully")
    client.close()

def process_request(request):
    print('Processed request')
    return 'data'
