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

def generate_vcf_file(vcf_string, date_time):
    f = open("./Data/{}.vcf".format(date_time), "a") 
    # f = open("./Data/vcf_output.vcf", "a") 
    # genes = vcf_string.split('\n')[1]
    # genes=genes[12:-2]
    genes = '\n'.join(vcf_string)
    genes=genes.replace('\\t','    ')
    genes=genes.replace('\\n','\n')
    print(genes)

    f.write(genes)
    f.close()

def send_vcf_to_genomics(vcf_string, date_time):
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

    generate_vcf_file(vcf_string, date_time)
    print("Sending VCF file to CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    scp = SCPClient(client.get_transport())
    # scp.put("./Data/input_test.vcf" , "./PathoSearch")
    scp.put("./Data/{}.vcf".format(date_time), "./PathoSearch/Cadd_Input")
    # scp.put("./Data/vcf_output.vcf", "./PathoSearch/Cadd_Input")
    print("VCF file has been sent to Genomics successfully")
    client.close()


def execute_cadd_script(date_time, genomeVersion):
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
    genome_build = '-a -g {} '.format(genomeVersion)
    output_loc = '-o /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/{}_output.tsv.gz '.format(date_time)
    input_loc = '/mnt/disk2/home/estiyl/PathoSearch/Cadd_Input/{}.vcf'.format(date_time)
    unzip_Output = '&& gunzip /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/{}_output.tsv.gz'.format(date_time)
    cmd = cadd_dir + conda_env+ cadd_sh + genome_build + output_loc + input_loc + unzip_Output

    # Executing the command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('CADD script was executed')
    msg = stderr.readlines()
    print(msg)
    client.close()

def fetch_vcf_output_from_genomics(date_time):
    #TODO: Fetch the right output based on date_time as part the name of the output
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
                sftp.get('./PathoSearch/Cadd_Output/{}_output.tsv'.format(date_time), './Data/Cadd_Output/{}_output.tsv'.format(date_time))
                print('File exists!')
                print('Copying file from Genomics to Server...')
                cadd_output_exist = True
            except IOError:
                sftp.get('./PathoSearch/Cadd_Output/{}_output.tsv'.format(date_time), './Data/Cadd_Output/{}_output.tsv'.format(date_time))
            client.close()
        except paramiko.SSHException:
            print("Server Couldn't Fetch Cadd CSV Output  Error")
    print("VCF file has been been sent to Server successfully")
    client.close()


def process_request(request, date_time):
    print('Server is processing request for CADD')
    # vcf_string = request.data.decode("utf-8")
    vcf_string = request.get_json()["genes"]
    genomeVersion = request.get_json()["genomeVersion"]
    send_vcf_to_genomics(vcf_string, date_time)
    execute_cadd_script(date_time, genomeVersion)
    fetch_vcf_output_from_genomics(date_time)
    return "Cadd process has finished"
