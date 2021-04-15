def main():
    inputString = {
        "genes": "#CHROM\tPOS\tID\tREF\tALT\n1\t983404\t137965991\tC\tT\n1\t6529186\t\tTCC\t\n1\t11159851\t146839323\t\tG\tA",
        "genomeVersion": 37,
        "tissue": "heart",
        "inputFormat": "VCF"
    }
    # print(inputString["genes"])
    genes_string_to_vf_file(inputString["genes"])

def genes_string_to_vf_file(genes):
    startIdx = genes.find("ALT")
    #Remove first row
    genes = genes[startIdx+4:]
    # print(genes)
    genesList = genes.split("\n")
    print(genesList)
    # for char in genes:
    #     if
if __name__ == '__main__':
    main()
