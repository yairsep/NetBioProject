__author__ = 'bashao'

import os
from SQLConnection import SQLConnection

class UploadGTEx:
    def __init__(self, workDir):
        self.workDir = workDir
        self.sqlConnection = SQLConnection()

    def run(self):
        #Create table
        #self.sqlConnection.createGTExDiffTable()
        self.sqlConnection.deleteGTExTable()

        #Read files
        ret = {}
        dirs = os.listdir(self.workDir)
        for dir in dirs:
            f = open(os.path.join(self.workDir, dir, dir+'_median.tsv'), 'r')
            dir = dir.replace(' - ', '_')
            dir = dir.replace(' ', '_')
            dir = dir.replace('(', '')
            dir = dir.replace(')', '')
            for line in f:
                tokens = line.strip().split()
                sourceName = tokens[0].strip()
                targetName = tokens[1].strip()
                sourceType = tokens[2].strip()
                targetType = tokens[3].strip()
                interactionType = tokens[4].strip()
                weight = tokens[5].strip()
                if ((sourceName, sourceType), (targetName, targetType), interactionType) in ret:
                    ret[((sourceName, sourceType), (targetName, targetType), interactionType)].append(weight)
                else:
                    ret[((sourceName, sourceType), (targetName, targetType), interactionType)] = [weight]
            f.close()

        #Upload
        for ((sourceName, sourceType), (targetName, targetType), interactionType) in ret:
            self.sqlConnection.updateGTExTable(sourceName, targetName, sourceType, targetType, interactionType,
                                              ret[((sourceName, sourceType), (targetName, targetType), interactionType)])

if __name__ == '__main__':
    ug = UploadGTEx('../../data/GTEx')
    ug.run()