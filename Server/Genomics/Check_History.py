import os, csv
from flask import jsonify

def exist_in_cluster(date_time):
    server_hanan_output_path = './Data/Hanan_Output/{}_hanan_output.csv'.format(date_time)
    if os.path.exists(server_hanan_output_path):
        json_output = []
        with open("./Data/Hanan_Output/{}_hanan_output.csv".format(date_time)) as input_file:
            # print(input_file)
            csvReader = csv.DictReader(input_file)
            for rows in csvReader:
                json_output.append(rows)
                # print(input_file)
        return jsonify([json_output, {'time': date_time}])
    else:
        return "This file doesn't exist in our Data Base"

# TODO: Implement this function
def get_shap_history(date_time):

    server_shap_output_path = './Data/Shap_Output/{}_shap_output.jpg'.format(date_time)
    if os.path.exists(server_shap_output_path):
        return "The jpg img"
    else:
        return "This jpg shap result file doesn't exist in our Data Base"


def process_request(request):
    timestamp = request.args.get('timestamp')
    # print(timestamp)
    output = exist_in_cluster(timestamp)

    # Todo: add shap history to output
    get_shap_history(timestamp)
    return output
