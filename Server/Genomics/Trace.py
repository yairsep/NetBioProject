def generate_csv(request):
    print('Genarting Csv')
    processed_request = process_request(request)


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
