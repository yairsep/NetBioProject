from scp import SCPClient
import os, paramiko, vobject
import getpass

def getConnectiionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD


# def generate_vcf_file(vcf_string):
#     f = open("./Data/vcf_output.vcf", "a")
#     # TODO: Parse string
#     f.write(vcf_string)
#     f.close()

def generate_vcf_file(vcf_string):
    f = open("./Data/vcf_output.vcf", "a") 
    genes = vcf_string.decode("utf-8").split('\n')[1]
    genes=genes[12:-2]
    genes=genes.replace('\\t','    ')
    genes=genes.replace('\\n','\n')

    f.write(genes)
    f.close()

def send_vcf_to_genomics(vcf_string):
    # generate_vcf_file(vcf_string)
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
    # scp.put("./Data/input_test.vcf" , "./PathoSearch")
    scp.put("./Data/test.vcf", "./PathoSearch/Cadd_Input")
    print("VCF file has been sent to Genomics successfully")
    client.close()


def execute_cadd_script():
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    print('Executing CADD script by SSH')
    #TODO: Find cadd script
    cadd_dir = 'cd /mnt/disk1/CADD/CADD-scripts/ &&'
    conda_env = 'source activate snakemake && '
    cadd_sh = './CADD.sh '
    genome_build = '-a -g GRCh37 '
    output_loc = '-o /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/cadd_output.tsv.gz '
    input_loc = '/mnt/disk2/home/estiyl/PathoSearch/Cadd_Input/github_input.vcf'
    unzip_Output = '&& gunzip /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/cadd_output.tsv.gz'
    cmd = cadd_dir + conda_env+ cadd_sh + genome_build + output_loc + input_loc + unzip_Output

    # Executing the command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('CADD script was executed')
    msg = stderr.readlines()
    print(msg)
    client.close()

def fetch_vcf_output_from_genomics():
    print("Fetching VCF Output file from CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    cadd_output_exist = False
    #TODO: Fix waiting
    while not cadd_output_exist:
        try:
            client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
            sftp = client.open_sftp()
            try:
                sftp.get('./PathoSearch/Cadd_Output/cadd_output.tsv', './Data/Cadd_Output/cadd_output.tsv')
                print('File exists!')
                print('Copying file from Genomics to Server...')
                cadd_output_exist = True
            except IOError:
                sftp.get('./PathoSearch/Cadd_Output/cadd_output.tsv', './Data/Cadd_Output/cadd_output.tsv')
            client.close()
        except paramiko.SSHException:
            print("Server Couldn't Fetch Cadd CSV Output  Error")
    print("VCF file has been been sent to Server successfully")
    client.close()


def process_request(request):
    print('Server is processing request for CADD')
    # vcf_string = request.data.decode("utf-8")
    # send_vcf_to_genomics(vcf_string)
    execute_cadd_script()
    fetch_vcf_output_from_genomics()
    return "Cadd process has finished"
