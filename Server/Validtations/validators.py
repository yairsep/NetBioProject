from webargs import ValidationError
from api.v1.utils import GTExTissues

NODE_LIMIT = 1

def database_must_exist(args):
    database = args['database']
    if database not in ['HPA', 'GTEx']:
        raise ValidationError(
            '{} is not a supported database. Please choose either GTEx or HPA.'.format(database)
        )


def tissue_must_exist_in_db(args):
    # database = 'HPA_RNA_Seq' if args['database'] == 'HPA' else args['database']
    database = 'GTEx'
    if database == 'GTEx':
        tissues = GTExTissues
    else:
        tissues = HPATissues

    # tissues = db.metadata.tables[database].columns
    if args['tissue'] not in tissues:
        # Optionally pass a status_code
        raise ValidationError('{} does not exist in database.'.format(args['tissue']))


def gene_list_right_size(args):
    if len(args['gene_id']) > NODE_LIMIT:
        raise ValidationError(
            'Query contains too many genes. Please select as many as {}.'.format(NODE_LIMIT)
        )