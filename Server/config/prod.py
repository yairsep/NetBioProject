
# Set this to True only in dev environment. Highly verbose.
DEBUG = False

# Suppress idiot warning.
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Main database bind URI.
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:33306/netbio2'

# Auxiliary bindings.
SQLALCHEMY_BINDS = {
    # 'InteractionsData': 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/InteractionsData',
    # 'TissueExpressionData': 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/TissueExpressionData',
    # 'Interactions': 'mysql+pymysql://ms_trace_dbu:bgu2010@netbio.bgu.ac.il:33306/Interactions',
    'netbio2': 'mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio2'
}
