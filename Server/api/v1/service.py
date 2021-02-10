import random
from importlib import import_module
from itertools import chain
from sqlalchemy import and_, or_
# from api.v1.schemas import InteractionsContext
from api.v1.app import getWorkingVersion
from .utils import sample_genes, sample
from api.v1.models import Updates


def generate_table(genes, tissue):
    print('tissue: %s, genes: %s' % (tissue, str(genes)))
    from api.v1.models import PredictedScores
    schemas = 'api.v1.schemas'
    db_schema = getattr(import_module(schemas), 'GeneSchema')
    genesSet = set(handle_genes_names(genes))
    print(genesSet)
    q = PredictedScores.query.filter(PredictedScores.Ensembl.in_(genesSet)).all()
    # print('HERE', PredictedScores.query.join(PredictedScores.Ensembl).filter(PredictedScores.Ensembl.in_(genesSet)).all())
    data2return = []
    for gene in q:
        # print('gene', gene)
        data2return.append({'Gene': gene.Ensembl,
                                  'XGB': str(getattr(gene, 'XGB_'+tissue)),
                                  'RF': str(getattr(gene, 'RF_'+tissue)),
                                  'LR': str(getattr(gene, 'LR_'+tissue)),
                                  'LR+GB': str(getattr(gene, 'LR.GB_'+tissue)),
                                  'MLP': str(getattr(gene, 'MLP_'+tissue)),
                                  'Meta_MLP': str(getattr(gene, 'meta_MLP_'+tissue)),
                                  })

    retGenesSet = set([item['Gene'] for item in data2return])
    summary = {'gene_not_in_db': len(genesSet - retGenesSet), 'tissue': tissue}
    nodes = db_schema.process_to_object(data2return)
    print('nodes', nodes)
    return nodes, summary


def generate_table_from_vcf(vcf, tissue):
    print('tissue: %s, genes: %s' % (tissue, str(vcf)))
    import requests, json, re
    genes = set([])

    s_vcf = vcf.split('\n')
    vars = []
    for line in s_vcf:
        if not line[0] == '#' and not ('CHR' in line):
            vars.append(line)
    variants = {'variants': vars}
    # print('variants', variants)
    # f = open('nuuuuuu.txt', 'w')
    # f.write(json.dumps(vars))
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.post("https://rest.ensembl.org/vep/homo_sapiens/region", headers=headers, data=json.dumps(variants))

    if not res.ok:
        res.raise_for_status()
        return generate_table([], '')
    else:
        print('res', res.json())
        res_data = res.json()
        for item in res_data:
            if "transcript_consequences" in item:
                for var in item["transcript_consequences"]:
                    if "gene_id" in var:
                        genes.add(var["gene_id"])

    # print(genes)

    return generate_table(list(genes), tissue)


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


