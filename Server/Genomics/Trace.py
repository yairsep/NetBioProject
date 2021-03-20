from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


def generate_csv(request):
    print('Genarting Csv')
    getFirstRow()
    # print(result)


def getFirstRow():
    engine = create_engine('mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio1', echo=True)
    metadata = MetaData(engine)
    Relevant_Benign = Table('Relevant_Benign_GRCh37-v1.6_CADD', metadata, autoload=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Relevant_Benign).first()
    print(result)


def process_request(request):
    print('Processed request')
    genes = request.get_json()['genes']
    genomeVersion = request.get_json()['genomeVersion']
    inputFormat = request.get_json()['inputFormat']
    tissue = request.get_json()['tissue']
    genes_names = generate_table_from_vcf(genes, tissue)


# TODO: Make a csv file from the variations, inside Genomics
#  Filter from the db the variations from trace(df_fulldataset), put inside csv.
def generate_table_from_vcf(vcf, tissue):
    print('tissue: %s, genes: %s' % (tissue, str(vcf)))
    genes = set([])

    s_vcf = vcf.split('\n')
    vars = []
    for line in s_vcf:
        if len(line) > 0 and not line[0] == '#' and not ('CHR' in line):
            vars.append(line)
    variants = {'variants': vars}
