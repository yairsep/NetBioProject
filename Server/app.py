import os
import sys

import flask_cors
from flask import Flask, jsonify, send_file, request , session
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from Genomics import Cadd , Trace , Learn

sys.path.insert(0, '')

# initialize flask app
app = Flask(__name__)
cors = CORS(app, expose_headers='Authorization', support_credentials=True , resources={r"/*": {"origins": "*"}}, headers="Content-Type")


# apply configuration
cfg = os.path.join(os.path.dirname(__file__), 'config/dev.py')
app.config.from_pyfile(cfg)
UPLOAD_FOLDER = './Data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# initialize error logging.
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter

    mail_handler = SMTPHandler('smtp.bgu.ac.il',
                               'netbio@post.bgu.ac.il',
                               ['netbio@post.bgu.ac.il'], 'TRACE has failed')
    mail_handler.setLevel(logging.ERROR)

    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))

# initialize db engine
db = SQLAlchemy()

db.init_app(app)
# bind Model to existing tables
db.reflect(app=app)

# Argument schemas
from webargs import fields, validate, ValidationError

get_vcf_args = {
    'vcf': fields.Str(required=True),
    'tissue': fields.Str(required=True, location='view_args')
}

get_genes_args = {
    'genes': fields.List(fields.Str(required=True)),
    'tissue': fields.Str(required=True, location='view_args')
}


# @app.route('/api/genes', methods=['POST'])
# # @use_kwargs(get_vcf_args)
# # @cross_origin()
# def vcf_and_tissues():
#     # save_location(request.remote_addr)
#     genes = request.get_json()['genes']
#     genomeVersion = request.get_json()['genomeVersion']
#     inputFormat = request.get_json()['inputFormat']
#     tissue = request.get_json()['tissue']
#     from api.v1.service import generate_table_from_vcf
#     genes_names = generate_table_from_vcf(genes, tissue)
#     print(genes_names)
#     # return jsonify({'genes': nodes, 'summary': params}), 200
#     return jsonify({'genes': genes})

@app.route('/sample', methods=['GET'])
# @cross_origin()
def sample():
    print("HELLO")

    from api.v1.service import generate_sample_table
    sample_ans = generate_sample_table()

    return jsonify(sample_ans)



@app.route('/vcf', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_vcf():
    print("VCF file recived in Server")
    Trace.process_request(request)
    vcf_string = request.data.decode("utf-8")
    Cadd.send_vcf_to_genomics(vcf_string)
    #Then Execute ML module
    # Learn.execute_ML_module()
    return "VCF file has been sent successfully"


def save_location(ip):
    import ipinfo
    access_token = '38497bee5db942'
    handler = ipinfo.getHandler(access_token)
    res = handler.getDetails(ip)

    import datetime
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = ['TRACE', date_time, res.latitude, res.longitude, res.country_name, res.city]

    import csv
    try:
        with open(r'/media/disk2/users/trace/Websites/Server/users_locations.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    except:
        print('save_location has failed')



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
