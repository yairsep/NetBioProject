from scp import SCPClient
import os, paramiko, vobject

def getConnectiionConfig():
    CLUSTER_HOST = 'genomics.bgu.ac.il'
    CLUSTER_USER = 'estiyl'
    CLUSTER_PASSWORD = 'H!ytfP7eq'

    return CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD

def generate_vcf_file(vcf_string):
    f = open("./Data/vcf_output.vcf", "a")
    #TODO: Parse string
    f.write(vcf_string)
    f.close()


def send_vcf_to_genomics(vcf_string):
    generate_vcf_file(vcf_string)
    #Todo: Check what arik tried to do
    # print("****************")
    # vcard = vobject.readOne('\n'.join([f'{k}:{v}' for k, v in vcf_string.items()]))
    # vcard.name = 'VCARD'
    # #vcard.useBegin = True
    # vcard.prettyPrint()
    # with open('./test.vcf', 'w', newline='') as f:
    #     f.write(vcard.serialize())
    # print("****************")

    print("Sending VCF file to CADD...")
    CLUSTER_HOST , CLUSTER_USER , CLUSTER_PASSWORD = getConnectiionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)
    scp = SCPClient(client.get_transport())
    # scp.put("./Data/vcf_test.vcf" , "./PathoSearch")
    scp.put("./Data/vcf_output.vcf" , "./PathoSearch")

    print("VCF file has been sent to Cadd successfully")
    client.close()

def process_request(request):
    print('Cadd is processing  request')
    vcf_string = request.data.decode("utf-8")
    send_vcf_to_genomics(vcf_string)
    return "Cadd process has finished"
