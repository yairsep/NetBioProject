import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from Genomics import Cadd, Trace, Learn
from Email import emailHandler
import datetime

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


@app.route('/sample', methods=['GET'])
# @cross_origin()
def sample():
    from Utils.utils import sample
    return jsonify(sample)
    # from Database.service import generate_sample_table
    # sample_ans = generate_sample_table()


@app.route('/vcf', methods=['POST'])
@cross_origin(supports_credentials=True)
def process_vcf():
    print("VCF file received in Server")
    date_time = datetime.datetime.now()
    date_time = str(date_time.replace(microsecond=0)).replace(" ", "__").replace(':', '_')
    Cadd.process_request(request, date_time)
    Trace.process_request(request, date_time)
    # Then Execute ML module
    # Learn.execute_ML_module(date_time)
    # hanan_output = Learn.getOutput(date_time)
    # return hanan_output
    return "VCF file has been sent successfully"


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
