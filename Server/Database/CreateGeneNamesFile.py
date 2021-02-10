__author__ = 'bashao'

import os

class CreateGeneNamesFiles:
    def __init__(self, workDir):
        self.workDir = workDir

    def run(self, namesfile, infile, ensg, entrez, symbol):
        self.ensgs = self.readFilteredExpressionFile(infile)
        print 'There are %d genes expressed in any tissue'%len(self.ensgs)
        self.ensg2entrez, self.ensg2symbol = self.readNamesFile(namesfile)
        self.writeOutfiles(ensg, entrez, symbol)

    def readFilteredExpressionFile(self, infile):
        genes = set([])
        f = open(os.path.join(self.workDir, infile), 'r')
        for line in f:
            tokens = line.split('\t')
            gene1 = tokens[0].strip()
            gene2 = tokens[1].strip()

            genes.add(gene1)
            genes.add(gene2)
        f.close()
        return genes

    def readNamesFile(self, namesfile):
        f = open(os.path.join(self.workDir, namesfile), 'r')
        ensg2entrez = {}
        ensg2symbol = {}
        for line in f:
            tokens = line.split('\t')
            ensg = tokens[0].strip()
            try:
                entrez = int(tokens[1].strip())
                #print entrez
            except Exception:
                entrez = ''
            symbol = tokens[3].strip()
            if ensg in ensg2entrez:
                ensg2entrez[ensg].add(entrez)
            else:
                ensg2entrez[ensg] = set([entrez])
            if ensg in ensg2symbol:
                ensg2symbol[ensg].add(symbol)
            else:
                ensg2symbol[ensg] = set([symbol])
        f.close()
        return (ensg2entrez, ensg2symbol)

    def writeOutfiles(self, ensg, entrez, symbol):
        f = open(os.path.join(self.workDir, ensg), 'w')
        for gene in self.ensgs:
            f.write('%s\n'%gene)
        f.close()

        f = open(os.path.join(self.workDir, entrez), 'w')
        entrezs = set([])
        for gene in self.ensgs:
            if gene in self.ensg2entrez:
                for entrez_ident in self.ensg2entrez[gene]:
                    if not entrez_ident == '':
                        entrezs.add(int(entrez_ident))
                    else:
                        print 'not an int %s'%entrez_ident
        print 'There are %d entrez identifiers'%(len(entrezs))
        for entrez_ident in entrezs:
            if not entrez_ident == '':
                f.write('%d\n'%entrez_ident)
        f.close()

        f = open(os.path.join(self.workDir, symbol), 'w')
        symbols = set([])
        for gene in self.ensgs:
            if gene in self.ensg2symbol:
                for symbol_ident in self.ensg2symbol[gene]:
                    symbols.add(symbol_ident)
        print 'There are %d symbol identifiers'%(len(symbols))
        for symbol_ident in symbols:
            f.write('%s\n'%symbol_ident)
        f.close()

if __name__ == '__main__':
    cgnf = CreateGeneNamesFiles('../../data')
    cgnf.run('human_names.tsv', 'HPA interactomes/adrenal.tsv', 'HPA ensg identifiers.tsv', 'HPA entrez identifiers.tsv', 'HPA symbol identifiers.tsv')
    cgnf.run('human_names.tsv', 'GTEx interactomes/Adipose - Subcutaneous.tsv', 'GTEx ensg identifiers.tsv', 'GTEx entrez identifiers.tsv', 'GTEx symbol identifiers.tsv')