from scp import SCPClient
import os, paramiko, vobject
import getpass

def getConnectiionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD


def generate_vcf_file(vcf_string):
    f = open("./Data/vcf_output.vcf", "a")
    # TODO: Parse string
    f.write(vcf_string)
    f.close()


def send_vcf_to_genomics(vcf_string):
    generate_vcf_file(vcf_string)
    # Todo: Check what arik tried to do
    # print("****************")
    # vcard = vobject.readOne('\n'.join([f'{k}:{v}' for k, v in vcf_string.items()]))
    # vcard.name = 'VCARD'
    # #vcard.useBegin = True
    # vcard.prettyPrint()
    # with open('./test.vcf', 'w', newline='') as f:
    #     f.write(vcard.serialize())
    # print("****************")

    print("Sending VCF file to CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    scp = SCPClient(client.get_transport())
    # scp.put("./Data/vcf_test.vcf" , "./PathoSearch")
    scp.put("./Data/vcf_output.vcf", "./PathoSearch")
    print("VCF file has been sent to Cadd successfully")
    client.close()


def execute_cadd_script():
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    print('Connected to Genomics by SSH')
    #TODO: Find cadd script
    cmd = 'cd PathoSearch && python script.py'

    # Executing the command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('SSH Command Was executed')
    msg = stderr.readlines()
    print(msg)
    client.close()

def fetch_vcf_output_from_genomics():
    print("Fetching VCF file to CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    # scp = SCPClient(client.get_transport())
    cadd_output_exist = False
    while not cadd_output_exist:
        try:
            client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
            sftp = client.open_sftp()
            sftp.chdir("/tmp/")
            try:
                print(sftp.stat('/tmp/cadd_output.csv'))
                print('File exists')
                cadd_output_exist = True
            except IOError:
                print('copying file')
                sftp.get('/tmp/cadd_output.txt','./Data/cadd_output.csv')
            client.close()
        except paramiko.SSHException:
            print("Server Couldn't Fetch Cadd CSV Output  Error")
    print("VCF file has been been sent to Server successfully")
    client.close()


def process_request(request):
    print('Cadd is processing  request')
    vcf_string = request.data.decode("utf-8")
    send_vcf_to_genomics(vcf_string)
    execute_cadd_script()
    fetch_vcf_output_from_genomics()
    return "Cadd process has finished"
