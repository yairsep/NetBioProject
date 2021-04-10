from importlib import import_module
# from api.v1.schemas import InteractionsContext
from NetBioProject.Server.Utils.utils import sample
# from api.v1.models import Updates


# TODO: Make a csv file from the variations, inside Genomics.
# Filter from the db the variations from trace(df_fulldataset), put inside csv.
# 
def generate_table_from_vcf(vcf, tissue):
    print('tissue: %s, genes: %s' % (tissue, str(vcf)))
    genes = set([])

    s_vcf = vcf.split('\n')
    vars = []
    for line in s_vcf:
        if len(line) > 0 and not line[0] == '#' and not ('CHR' in line):
            vars.append(line)
    variants = {'variants': vars}



def generate_sample_table():

    return sample


def handle_genes_names(genes):
    import re
    ENSEMBL_RE = re.compile(
        "ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?|CG[0-9]+|[A-Z0-9]+\.[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]")

    models = 'api.v1.models'
    version = Updates.getWorkingVersion()
    symbols = []
    final_ensembles = []
    for gene in genes:
        if not ENSEMBL_RE.match(gene):
            symbols.append(gene)
        else:
            final_ensembles.append(gene)

    if len(symbols) > 0:
        converted_names = getattr(import_module(models), 'Names' + version).genes_list_to_ensembl(symbols)
        # print('converted', converted_names)
        final_ensembles += converted_names

    return final_ensembles


