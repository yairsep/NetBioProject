from webargs import ValidationError

from api.v1.database import db
# from api.v1.models import NamesB
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


# def gene_must_be_unambiguous(args):
#     gene, database = args['gene'], args['database']
#     database = 'HPA_RNA_Seq' if args['database'] == 'HPA' else args['database']
#     potential_genes = NamesB.check_name(gene)
#     if len(potential_genes) > 1:
#         raise ValidationError(
#             'Ambiguous gene identifier {} matches the following: {}'.format(gene, potential_genes)
#         )
#     elif len(potential_genes) < 1:
#         raise ValidationError(
#             'No entry matches {} in our database.'.format(gene, potential_genes)
#         )
#     else:
#         q = db.session.query(db.metadata.tables[database]).filter_by(Gene_identifier=gene).first()
#         if q is None:
#             raise ValidationError(
#                 'No entry matches {} in our database.'.format(gene, potential_genes))

#         # Inject ENSG name to be passed instead of whatever the user filled in.
#         args['gene'] = potential_genes


def gene_list_right_size(args):
    if len(args['gene_id']) > NODE_LIMIT:
        raise ValidationError(
            'Query contains too many genes. Please select as many as {}.'.format(NODE_LIMIT)
        )