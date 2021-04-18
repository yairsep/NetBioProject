from scp import SCPClient
import os, paramiko, time


def getConnectionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD

#TODO: Fix this function
def generate_vcf_file(vcf_string, date_time):
    f = open("./Data/Cadd_Input/{}.vcf".format(date_time), "a")
    if ("#CHROM" in vcf_string[0]):
        vcf_string = vcf_string[1:]
    genes = '\n'.join(vcf_string)
    genes = genes.replace('\t\t', '\t.\t')
    genes = genes.replace('\t\n', '\t.\n')
    genes = genes.replace('\\t', '    ')
    genes = genes.replace('\\n', '\n')
    f.write(genes)
    f.close()


def send_vcf_to_genomics(date_time):
    print("Sending VCF file to CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    scp = SCPClient(client.get_transport())
    scp.put("./Data/Cadd_Input/{}.vcf".format(date_time), "./PathoSearch/Cadd_Input")
    print("VCF file has been sent to Genomics successfully")
    client.close()


def execute_cadd_script(date_time, genomeVersion):
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    print('Executing CADD script by SSH')
    cadd_dir = 'cd /mnt/disk1/CADD/CADD-scripts/ &&'
    conda_env = 'source activate snakemake && '
    cadd_sh = './CADD.sh '
    genome_build = '-a -g {} '.format(genomeVersion)
    output_loc = '-o /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/{}.tsv.gz '.format(date_time)
    input_loc = '/mnt/disk2/home/estiyl/PathoSearch/Cadd_Input/{}.vcf'.format(date_time)
    unzip_Output = '&& gunzip /mnt/disk2/home/estiyl/PathoSearch/Cadd_Output/{}.tsv.gz'.format(date_time)
    cmd = cadd_dir + conda_env + cadd_sh + genome_build + output_loc + input_loc + unzip_Output

    # Executing the command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('CADD script was executed')
    msg = stderr.readlines()
    print(msg)
    client.close()


def fetch_vcf_output_from_genomics(date_time):
    # TODO: Fetch the right output based on date_time as part the name of the output
    print("Fetching VCF Output file from CADD...")
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    sftp = client.open_sftp()
    genomics_cadd_output_path = './PathoSearch/Cadd_Output/{}.tsv'.format(date_time)
    server_cadd_output_path = './Data/Cadd_Output/{}.tsv'.format(date_time)

    while not os.path.exists(server_cadd_output_path):
        try:
            print('Trying to copy file from Genomics to Server...')
            sftp.get(genomics_cadd_output_path, server_cadd_output_path)
        except IOError or paramiko.SSHException:
            time.sleep(5)
            print('Waiting 5 secs for re-copying')
            break
    print("VCF file has been been sent to Server successfully")
    sftp.close()
    client.close()


def process_request(request, date_time):
    print('Server is processing request for CADD')
    vcf_string = request.get_json()["genes"]
    genomeVersion = request.get_json()["genomeVersion"]
    generate_vcf_file(vcf_string, date_time)
    send_vcf_to_genomics(date_time)
    execute_cadd_script(date_time, genomeVersion)
    fetch_vcf_output_from_genomics(date_time)
    return "Cadd process has finished"
