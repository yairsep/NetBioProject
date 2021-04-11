import requests
import json

def process_request(request):
    print('Trace is processing request')
    genes = request.get_json()['genes']
    genomeVersion = request.get_json()['genomeVersion']
    inputFormat = request.get_json()['inputFormat']
    tissue = request.get_json()['tissue']
    genes_names = generate_table_from_vcf(genes, tissue)


# TODO: Make a csv file from the variations, inside Genomics
#  Filter from the db the variations from trace(df_fulldataset), put inside csv.
def generate_table_from_vcf(vcf, tissue):
    # print('tissue: %s, genes: %s' % (tissue, str(vcf)))
    genes = set([])

    s_vcf = vcf.split('\n')
    vars = []
    for line in s_vcf:
        if len(line) > 0 and not line[0] == '#' and not ('CHR' in line):
            vars.append(line)
    variants = {'variants': vars}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    res = requests.post("https://rest.ensembl.org/vep/homo_sapiens/region", headers=headers, data=json.dumps(variants))

    if not res.ok:
        print('Error getting genes names for TRACE')
    else:
        print('res', res.json())
        res_data = res.json()
        for item in res_data:
            if "transcript_consequences" in item:
                for var in item["transcript_consequences"]:
                    if "gene_id" in var:
                        genes.add(var["gene_id"])
                        
    print(genes)
    send_query_to_Trace(list(genes))

def send_query_to_Trace(genes):
    print("Sending Query to Trace")
    #TODO: Send query to Trace
    from models import Df_Complete_Dataset
    
    #TODO: May need to use handle_genes_names function from TRACE
    q = Df_Complete_Dataset.query.filter(Df_Complete_Dataset.ID.in_(genes)).all()
    from sqlalchemy import inspect
    inst = inspect(Df_Complete_Dataset)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    print(attr_names)
    for row in q:
        for attr in attr_names:
            print(row.ID + " " + attr + " " + str(getattr(row, attr)))

    # engine = create_engine('mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio1', echo=True)
    # metadata = MetaData(engine)
    # Relevant_Benign = Table('Relevant_Benign_GRCh37-v1.6_CADD', metadata, autoload=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # result = session.query(Relevant_Benign).first()
    # print(result)