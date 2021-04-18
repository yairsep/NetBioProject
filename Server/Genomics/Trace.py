import requests
import json
import csv

def process_request(request, date_time):
    print('Trace is processing request')
    genes = request.get_json()['genes']
    genomeVersion = request.get_json()['genomeVersion']
    inputFormat = request.get_json()['inputFormat']
    tissue = request.get_json()['tissue']
    generate_table_from_vcf(genes, tissue, date_time)


def generate_table_from_vcf(vcf, tissue, date_time):
    print('generating TRACE data from GeneIDs')
    genes = set([])

    with open("./Data/Cadd_Output/{}_output.tsv".format(date_time)) as in_file:
      line_count = 0
      for line in in_file:
          if line_count > 1:
            columns = line.split("\t")
            gene_name = columns[18]
            if gene_name != 'NA':
              genes.add(gene_name)
          line_count += 1
    print(genes)
    send_query_to_Trace(list(genes), date_time)

def send_query_to_Trace(genes, date_time):
    print("Sending Query to Trace")
    #TODO: Send query to Trace
    from models import Df_Complete_Dataset
    q = Df_Complete_Dataset.query.filter(Df_Complete_Dataset.ID.in_(genes)).all()
    from sqlalchemy import inspect
    inst = inspect(Df_Complete_Dataset)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    values_for_csv = list()
    values_for_csv.append(attr_names)
    for row in q:
        values_for_csv.append(multi_getattr(row, attr_names))
      
    generate_csv_file(values_for_csv, date_time)

    # engine = create_engine('mysql+pymysql://root:BiVc18@genomics.bgu.ac.il:3306/netbio1', echo=True)
    # metadata = MetaData(engine)
    # Relevant_Benign = Table('Relevant_Benign_GRCh37-v1.6_CADD', metadata, autoload=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # result = session.query(Relevant_Benign).first()
    # print(result)

def generate_csv_file(values_for_csv, date_time):
  print('generating csv file from TRACE data')
  with open('./data/TRACE_Output/{}.csv'.format(date_time), 'w', newline='') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',')
      for value in values_for_csv:
        spamwriter.writerow(value)

def multi_getattr(row, attr, default = None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.

    """
    sol = list()
    for i in attr:
        try:
            obj = getattr(row, i)
            sol.append(obj)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return sol