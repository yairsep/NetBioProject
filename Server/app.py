import os, sys, datetime, time
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from Genomics import Cadd, Trace, Learn, Check_History
from Email import emailHandler

sys.path.insert(0, '')

# initialize flask app
app = Flask(__name__)
cors = CORS(app, expose_headers='Authorization', support_credentials=True, resources={r"/*": {"origins": "*"}},
            headers="Content-Type")

# apply configuration
cfg = os.path.join(os.path.dirname(__file__), 'config/dev.py')
app.config.from_pyfile(cfg)
# initialize error logging.
if not app.debug:
    emailHandler.sendEmail()

# initialize db engine
db = SQLAlchemy()

db.init_app(app)
# bind Model to existing tables
db.reflect(app=app)


@app.route('/sample/<tissue>', methods=['GET'])
# @cross_origin()
def sample(tissue):
    from Utils.sample import brain_sample_jason, Testis_sample_jason
    if(tissue == 'brain'):
        return jsonify(brain_sample_jason)
    return jsonify(Testis_sample_jason)
    # from Database.service import generate_sample_table
    # sample_ans = generate_sample_table()


@app.route('/vcf', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_vcf():
    print("VCF file received in Server")
    tissue = request.get_json()['tissue']
    genome_version = request.get_json()['genomeVersion']
    print('The genome_version is: ', genome_version)
    print('The tissue is: ', tissue)
    date_time = datetime.datetime.now()
    date_time = str(date_time.replace(microsecond=0)).replace(" ", "__").replace(':', '_')
    Cadd.process_request(request, date_time)
    Trace.process_request(request, date_time, tissue)
    # Then Execute ML module
    Learn.execute_ML_module(date_time, tissue, genome_version)
    hanan_output = Learn.getOutput(date_time, tissue)
    return jsonify([hanan_output, {'time': date_time}])

@app.route('/shap', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_shap_results():
    print("Shap get request received in Server")
    # tissue = request.get_json()['tissue']
    date_time = request.get_json()['timestamp']
    tissue = request.get_json()['tissue']
    genome_version = request.get_json()['genomeVersion']
    print('The tissue is: ', tissue)
    print("genome_version", genome_version)
    # Then Execute ML module
    image_name = Learn.fetch_shap_results(date_time, tissue, genome_version, 0)

    return send_file(image_name, mimetype='image/gif')

@app.route('/shap', methods=['GET'])
# @cross_origin()
def get_image():
    timestamp = request.args.get('timestamp')
    tissue = request.args.get('tissue')
    rowNum = request.args.get('rowNum')
    img_path = './Data/Shap_Output/{}_{}_{}_shap_output.jpg'.format(timestamp, tissue, rowNum)
    return send_file(img_path, mimetype='image/gif')

@app.route('/updateShap', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_shap_results():
    print("Shap get request received in Server")
    # tissue = request.get_json()['tissue']
    # date_time = request.get_json()['timestamp']
    date_time = request.get_json()['timeStamp']
    genome_version = request.get_json()['genomeVersion']
    tissue = request.get_json()['tissue']
    row_num = request.get_json()['rowNum']
    print('The tissue is: ', request.get_json()['tissue'])
    print("genome_version", genome_version)
    # Then Execute ML module
    image_name = Learn.fetch_shap_results(date_time, tissue, genome_version, row_num)
    print(image_name)
    return send_file(image_name, mimetype='image/gif')

@app.route('/history', methods=['GET'])
# @cross_origin()
def restore():
    response = Check_History.process_request(request)
    return response

@app.errorhandler(422)
def handle_validation_error(err):
    # exc = err.data['exc']
    return err


@app.errorhandler(500)
def handle_internal_server_error(err):
    # exc = err.data['exc']
    # return jsonify({'errors': str(err), 'trace': traceback.format_exc()}), 500
    print('err:', err)
    return jsonify({'errors': 'The server has encountered an internal error, please check your query.'}), 500


@app.errorhandler(404)
def handle_page_not_found_error(err):
    # exc = err.data['exc']
    # return jsonify({'errors': repr(err)}), 404
    return jsonify({'errors': '404 - The path you are looking for is no on this server'}), 404


if __name__ == '__main__':
    basestring = (str, bytes)
    app.run(debug=True)
