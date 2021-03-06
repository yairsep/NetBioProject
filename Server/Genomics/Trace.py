import csv


def process_request(request, date_time, tissue):
    print('Trace is processing request')
    genes = request.get_json()['genes']
    genomeVersion = request.get_json()['genomeVersion']
    inputFormat = request.get_json()['inputFormat']
    generate_table_from_vcf(genes, tissue, date_time)


def generate_table_from_vcf(vcf, tissue, date_time):
    print('Generating TRACE data from GeneIDs')
    genes = set([])

    with open("./Data/Cadd_Output/{}_cadd.tsv".format(date_time)) as in_file:
        line_count = 0
        for line in in_file:
            if line_count > 1:
                columns = line.split("\t")
                gene_name = columns[18]
                if gene_name != 'NA':
                    genes.add(gene_name)
            line_count += 1
    # print(genes)
    send_query_to_Trace(list(genes), date_time)
    in_file.close()


def send_query_to_Trace(genes, date_time):
    print("Sending Query to Trace")
    from models import Df_Complete_Dataset
    q = Df_Complete_Dataset.query.filter(Df_Complete_Dataset.ID.in_(genes)).all()
    from sqlalchemy import inspect
    inst = inspect(Df_Complete_Dataset)
    from Utils.attr_names import attr_names_csv
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    values_for_csv = list()
    values_for_csv.append(attr_names_csv)
    for row in q:
        values_for_csv.append(multi_getattr(row, attr_names))

    generate_csv_file(values_for_csv, date_time)


def generate_csv_file(values_for_csv, date_time):
    print('Generating csv file from TRACE data')
    with open('./Data/TRACE_Output/{}_trace.csv'.format(date_time), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for value in values_for_csv:
            spamwriter.writerow(value)
    csvfile.close()


def multi_getattr(row, attr, default=None):
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
