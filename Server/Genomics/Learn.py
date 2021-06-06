import paramiko, os, time
from scp import SCPClient
import csv
import json


def getConnectionConfig():
    CLUSTER_HOST = 'sge180.bgu.ac.il'
    CLUSTER_USER = 'chanana'
    CLUSTER_PASSWORD = 'pilpI108'
    return CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD


def fetch_shap_results(date_time , tissue):
    # Initiating a ssh client protocol
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)

    hanan_cluster_path = "cd PathoSearch/ML-Scripts && "
    exec_command = "run_shap_python_script_yair.sh "

    cadd_output_path = "./DataInput/{}_cadd.csv ".format(date_time)
    trace_output_path= "./DataInput/{}_trace.csv ".format(date_time)
    prediction_output_path = "./DataOutput/{}.csv".format(date_time)
    relevant_variant_index = "0 "
    tissue = tissue + " "

    cmd = hanan_cluster_path + exec_command + cadd_output_path + trace_output_path + relevant_variant_index + tissue + prediction_output_path
    stdin, stdout, stderr = client.exec_command(cmd)
    print('Shap algo in Cluster Was executed')
    msg = stderr.readlines()
    print(msg)
    # Coping Shap output to server
    server_hanan_output_path = './Data/Shap_Output/{}_shap_output.jpg'.format(date_time)
    sftp = client.open_sftp()

    # TODO: Revert from hardcoded value
    cluster_output_path = "./PathoSearch/ML-Scripts/Shap_Output/{}.jpg".format(date_time)

    while not os.path.exists(server_hanan_output_path):
        try:
            print('Trying to copy jpg shap output file from Genomics to Server...')
            sftp.get(cluster_output_path, server_hanan_output_path)
        except IOError or paramiko.SSHException:
            time.sleep(5)
            print('Waiting 5 secs for re-copying')
            break
    print('Shap results has been copied to server successfully!')
    return server_hanan_output_path

def execute_ML_module(date_time, tissue):
    # Send cadd & trace output to ML Module
    print("Initiating Connection with Cluster")

    # Initiating a ssh client protocol
    CLUSTER_HOST, CLUSTER_USER, CLUSTER_PASSWORD = getConnectionConfig()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(CLUSTER_HOST, username=CLUSTER_USER, password=CLUSTER_PASSWORD)

    # Moving Outputs from CADD & Trace to Cluster
    cadd_input_tsv = "./Data/Cadd_Output/{}_cadd.csv".format(date_time)
    trace_input_csv = "./Data/TRACE_Output/{}_trace.csv".format(date_time)

    cluster_input_path = "./PathoSearch/ML-Scripts/DataInput"
    scp = SCPClient(client.get_transport())
    print("Coping CADD output to Cluster...")
    scp.put(cadd_input_tsv, cluster_input_path)
    print("Coping Trace output to Cluster...")
    scp.put(trace_input_csv, cluster_input_path)
    print("Copy Cadd & Trace output to Cluster Completed!")

    # Executing Hanan Algorithem
    print("Executing Hanan algorithem...")
    cadd_cluster_path = "./DataInput/{}_cadd.csv ".format(date_time)

    # cadd_cluster_path = "CardiomyopathyOtB0551_CADD_GRCh37-v1.6.csv "

    trace_cluster_path = "./DataInput/{}_trace.csv ".format(date_time)

    # trace_cluster_path = "Trace_Sample_CardiomyopathyOtB0551.csv "

    # tissue = tissue + " "
    tissue = tissue + " "

    hanan_cluster_path = "cd PathoSearch/ML-Scripts && "

    exec_command = "run_script_yair.sh " + cadd_cluster_path + trace_cluster_path + tissue + date_time
    print("tissue is:", tissue)
    cmd = hanan_cluster_path + exec_command
    stdin, stdout, stderr = client.exec_command(cmd)
    print('Hanan Algo in Cluster Was executed')
    msg = stderr.readlines()
    print(msg)

    # Coping Hanan algo output to server
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


# TODO: send the jpg shap file as well
def getOutput(date_time):
    json_output = []
    with open("./Data/Hanan_Output/{}_hanan_output.csv".format(date_time)) as input_file:
        # print(input_file)
        csvReader = csv.DictReader(input_file)
        for rows in csvReader:
            json_output.append(rows)
            # print(input_file)

    print("Sending Chanan CSV output file & Shap results back to Client!")
    return json_output
