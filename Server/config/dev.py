# Set this to True only in dev environment. Highly verbose.
DEBUG = True

# Suppress idiot warning.
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Main database bind URI.
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/TRACE'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio2'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/DifferentialInteractomes'

# Auxiliary bindings.
SQLALCHEMY_BINDS = {
    'TRACE': 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/TRACE',
    'Interactions': 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/Interactions',
    'netbio2': 'mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio2'
}
