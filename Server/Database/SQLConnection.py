__author__ = 'omer'

import MySQLdb
import datetime
from datetime import date
import traceback

class SQLConnection:


    class __impl:
        def __init__(self):
            try:
                self.db = MySQLdb.connect(host = "132.72.23.114",
                                          user = "datauser",
                                          passwd="bgu2010",
                                          port=33306,
                                          db = "")

                self.db.autocommit = False
                self.dbc = self.db.cursor()
            except Exception, exc:
                print "Can not connect to SQL Server"
                print exc
                

        def execute(self, query):
            try:
                self.dbc.execute(query)
                rows = self.dbc.fetchall()
                return rows
            except Exception, exc:
                self.db.close()
                self.db = MySQLdb.connect(host = "132.72.23.114",
                                          user = "datauser",
                                          passwd="bgu2010",
                                          port=33306,
                                          db = "")

                self.db.autocommit = False
                self.dbc = self.db.cursor()
                try:
                    self.dbc.execute(query)
                    rows = self.dbc.fetchall()
                    return rows
                except Exception, exc:
                    print "Bad query to execute %s"%(query)
                    print traceback.format_exc()
                    return

        def insertQuery(self, query):
            try:
                self.dbc.execute(query)
                self.db.commit()
            except Exception, exc:
                self.db.close()
                self.db = MySQLdb.connect(host = "132.72.23.114",
                                          user = "datauser",
                                          passwd="bgu2010",
                                          port=33306,
                                          db = "")

                self.db.autocommit = False
                self.dbc = self.db.cursor()
                try:
                    self.dbc.execute(query)
                    self.db.commit()
                except Exception, exc:
                    print "Bad insert query %s"%(query)
                    print traceback.format_exc()
                    return


        #Create Tables
        def createGTExDiffTable(self):
            """
            This method will create the databases table

            History
            -------
                13/3/16 - Added by Omer Basha
            """
            try:
                self.dbc.execute("""CREATE TABLE DifferentialInteractomes.GTEx(
                                 SourceName VARCHAR(50),
                                 TargetName VARCHAR(50),
                                 SourceType VARCHAR(50),
                                 TargetType VARCHAR(50),
                                 InteractionType VARCHAR(50),
                                 Adipose_Subcutaneous FLOAT(15,8),
                                 Adipose_Visceral_Omentum FLOAT(15,8),
                                 Artery_Aorta FLOAT(15,8),
                                 Artery_Coronary FLOAT(15,8),
                                 Artery_Tibial FLOAT(15,8),
                                 Brain_Amygdala FLOAT(15,8),
                                 Brain_Anterior_cingulate_cortex_BA24 FLOAT(15,8),
                                 Brain_Caudate_basal_ganglia FLOAT(15,8),
                                 Brain_Cerebellar_Hemisphere FLOAT(15,8),
                                 Brain_Cerebellum FLOAT(15,8),
                                 Brain_Cortex FLOAT(15,8),
                                 Brain_Frontal_Cortex_BA9 FLOAT(15,8),
                                 Brain_Hippocampus FLOAT(15,8),
                                 Brain_Hypothalamus FLOAT(15,8),
                                 Brain_Nucleus_accumbens_basal_ganglia FLOAT(15,8),
                                 Brain_Putamen_basal_ganglia FLOAT(15,8),
                                 Brain_Spinal_cord_cervical_c_1 FLOAT(15,8),
                                 Brain_Substantia_nigra FLOAT(15,8),
                                 Breast_Mammary_Tissue FLOAT(15,8),
                                 Cells_EBV_transformed_lymphocytes FLOAT(15,8),
                                 Cells_Transformed_fibroblasts FLOAT(15,8),
                                 Colon_Sigmoid FLOAT(15,8),
                                 Esophagus_Gastroesophageal_Junction FLOAT(15,8),
                                 Esophagus_Mucosa FLOAT(15,8),
                                 Esophagus_Muscularis FLOAT(15,8),
                                 Heart_Atrial_Appendage FLOAT(15,8),
                                 Heart_Left_Ventricle FLOAT(15,8),
                                 Liver FLOAT(15,8),
                                 Lung FLOAT(15,8),
                                 Minor_Salivary_Gland FLOAT(15,8),
                                 Muscle_Skeletal FLOAT(15,8),
                                 Nerve_Tibial FLOAT(15,8),
                                 Ovary FLOAT(15,8),
                                 Pituitary FLOAT(15,8),
                                 Prostate FLOAT(15,8),
                                 Skin_Not_Sun_Exposed_Suprapubic FLOAT(15,8),
                                 Skin_Sun_Exposed_Lower_leg FLOAT(15,8),
                                 Stomach FLOAT(15,8),
                                 Testis FLOAT(15,8),
                                 Thyroid FLOAT(15,8),
                                 Uterus FLOAT(15,8),
                                 Vagina FLOAT(15,8),
                                 Whole_Blood FLOAT(15,8),
                                 Whole_Brain FLOAT(15,8)
                                 ) ENGINE = INNODB; """)
                self.db.commit()
            except Exception, exc:
                self.db.close()
                self.db = MySQLdb.connect(host = "132.72.23.114",
                                          user = "datauser",
                                          passwd="bgu2010",
                                          port=33306,
                                          db = "")
                self.db.autocommit = False
                self.dbc = self.db.cursor()
                self.dbc.execute("""CREATE TABLE DifferentialInteractomes.GTEx(
                                 SourceName VARCHAR(50),
                                 TargetName VARCHAR(50),
                                 SourceType VARCHAR(50),
                                 TargetType VARCHAR(50),
                                 InteractionType VARCHAR(50),
                                 Adipose_Subcutaneous FLOAT(15,8),
                                 Adipose_Visceral_Omentum FLOAT(15,8),
                                 Artery_Aorta FLOAT(15,8),
                                 Artery_Coronary FLOAT(15,8),
                                 Artery_Tibial FLOAT(15,8),
                                 Brain_Amygdala FLOAT(15,8),
                                 Brain_Anterior_cingulate_cortex_BA24 FLOAT(15,8),
                                 Brain_Caudate_basal_ganglia FLOAT(15,8),
                                 Brain_Cerebellar_Hemisphere FLOAT(15,8),
                                 Brain_Cerebellum FLOAT(15,8),
                                 Brain_Cortex FLOAT(15,8),
                                 Brain_Frontal_Cortex_BA9 FLOAT(15,8),
                                 Brain_Hippocampus FLOAT(15,8),
                                 Brain_Hypothalamus FLOAT(15,8),
                                 Brain_Nucleus_accumbens_basal_ganglia FLOAT(15,8),
                                 Brain_Putamen_basal_ganglia FLOAT(15,8),
                                 Brain_Spinal_cord_cervical_c_1 FLOAT(15,8),
                                 Brain_Substantia_nigra FLOAT(15,8),
                                 Breast_Mammary_Tissue FLOAT(15,8),
                                 Cells_EBV_transformed_lymphocytes FLOAT(15,8),
                                 Cells_Transformed_fibroblasts FLOAT(15,8),
                                 Colon_Sigmoid FLOAT(15,8),
                                 Esophagus_Gastroesophageal_Junction FLOAT(15,8),
                                 Esophagus_Mucosa FLOAT(15,8),
                                 Esophagus_Muscularis FLOAT(15,8),
                                 Heart_Atrial_Appendage FLOAT(15,8),
                                 Heart_Left_Ventricle FLOAT(15,8),
                                 Liver FLOAT(15,8),
                                 Lung FLOAT(15,8),
                                 Minor_Salivary_Gland FLOAT(15,8),
                                 Muscle_Skeletal FLOAT(15,8),
                                 Nerve_Tibial FLOAT(15,8),
                                 Ovary FLOAT(15,8),
                                 Pituitary FLOAT(15,8),
                                 Prostate FLOAT(15,8),
                                 Skin_Not_Sun_Exposed_Suprapubic FLOAT(15,8),
                                 Skin_Sun_Exposed_Lower_leg FLOAT(15,8),
                                 Stomach FLOAT(15,8),
                                 Testis FLOAT(15,8),
                                 Thyroid FLOAT(15,8),
                                 Uterus FLOAT(15,8),
                                 Vagina FLOAT(15,8),
                                 Whole_Blood FLOAT(15,8),
                                 Whole_Brain FLOAT(15,8)
                                 ) ENGINE = INNODB; """)
                self.db.commit()

        def createHPADiffTable(self):
            try:
                self.dbc.execute("""CREATE TABLE DifferentialInteractomes.HPA(
                                 SourceName VARCHAR(50),
                                 TargetName VARCHAR(50),
                                 SourceType VARCHAR(50),
                                 TargetType VARCHAR(50),
                                 InteractionType VARCHAR(50),
                                 adrenal FLOAT(15,8),
                                 appendix FLOAT(15,8),
                                 bonemarrow FLOAT(15,8),
                                 brain FLOAT(15,8),
                                 colon FLOAT(15,8),
                                 endometrium FLOAT(15,8),
                                 esophagus FLOAT(15,8),
                                 fallopiantube FLOAT(15,8),
                                 fat FLOAT(15,8),
                                 gallbladder FLOAT(15,8),
                                 heart FLOAT(15,8),
                                 kidney FLOAT(15,8),
                                 liver FLOAT(15,8),
                                 lung FLOAT(15,8),
                                 lymphnode FLOAT(15,8),
                                 ovary FLOAT(15,8),
                                 placenta FLOAT(15,8),
                                 prostate FLOAT(15,8),
                                 rectum FLOAT(15,8),
                                 salivarygland FLOAT(15,8),
                                 skeletalmuscle FLOAT(15,8),
                                 skin FLOAT(15,8),
                                 smallintestine FLOAT(15,8),
                                 smoothmuscle FLOAT(15,8),
                                 spleen FLOAT(15,8),
                                 stomach FLOAT(15,8),
                                 testis FLOAT(15,8),
                                 thyroid FLOAT(15,8),
                                 tonsil FLOAT(15,8)
                                 ) ENGINE = INNODB; """)
                self.db.commit()
            except Exception, exc:
                self.db.close()
                self.db = MySQLdb.connect(host = "132.72.23.114",
                                          user = "datauser",
                                          passwd="bgu2010",
                                          port=33306,
                                          db = "")
                self.db.autocommit = False
                self.dbc = self.db.cursor()
                self.dbc.execute("""CREATE TABLE DifferentialInteractomes.HPA(
                                 SourceName VARCHAR(50),
                                 TargetName VARCHAR(50),
                                 SourceType VARCHAR(50),
                                 TargetType VARCHAR(50),
                                 InteractionType VARCHAR(50),
                                 adrenal FLOAT(15,8),
                                 appendix FLOAT(15,8),
                                 bonemarrow FLOAT(15,8),
                                 brain FLOAT(15,8),
                                 colon FLOAT(15,8),
                                 endometrium FLOAT(15,8),
                                 esophagus FLOAT(15,8),
                                 fallopiantube FLOAT(15,8),
                                 fat FLOAT(15,8),
                                 gallbladder FLOAT(15,8),
                                 heart FLOAT(15,8),
                                 kidney FLOAT(15,8),
                                 liver FLOAT(15,8),
                                 lung FLOAT(15,8),
                                 lymphnode FLOAT(15,8),
                                 ovary FLOAT(15,8),
                                 placenta FLOAT(15,8),
                                 prostate FLOAT(15,8),
                                 rectum FLOAT(15,8),
                                 salivarygland FLOAT(15,8),
                                 skeletalmuscle FLOAT(15,8),
                                 skin FLOAT(15,8),
                                 smallintestine FLOAT(15,8),
                                 smoothmuscle FLOAT(15,8),
                                 spleen FLOAT(15,8),
                                 stomach FLOAT(15,8),
                                 testis FLOAT(15,8),
                                 thyroid FLOAT(15,8),
                                 tonsil FLOAT(15,8)
                                 ) ENGINE = INNODB; """)
                self.db.commit()

        #Drop Table
        def deleteGTExTable(self):
            """
            This method will emtpy a version of the database

            Return
            ------
                True - if succeeded, exception - if failed for some reason.

            History
            -------
                16/03/2016 - Added by Omer Basha.
            """
            emptyGTExQuery = "DELETE FROM DifferentialInteractomes.GTEx;"
            self.insertQuery(emptyGTExQuery)
            return True

        def deleteHPATable(self):
            """
            This method will emtpy a version of the database

            Return
            ------
                True - if succeeded, exception - if failed for some reason.

            History
            -------
                16/03/2016 - Added by Omer Basha.
            """
            emptyInteractionsQuery = "DELETE FROM DifferentialInteractomes.HPA;"
            self.insertQuery(emptyInteractionsQuery)
            return True

        #Insert to table
        def updateHPATable(self, sourceName, targetName, sourceType, targetType, interactionType, weights):
            """
            This method will update a database in the interactions table.

            Parameters
            ----------
                sourceName : string
                    source gene identifier
                targetName : string
                    target gene identifier
                sourceType : string
                    the type of the source node
                targetType : string
                    the type of the target node
                interactionType : string
                    the type of the interaction

            Return
            ------
                True - if succeded, exception - if failed

            History
            -------
                13/03/16 - Added by Omer Basha.
            """
            query = 'INSERT INTO DifferentialInteractomes.HPA' \
                    '(SourceName, TargetName, SourceType, TargetType, InteractionType, ' \
                    'adrenal, appendix, bonemarrow, brain, colon, endometrium, esophagus, ' \
                    'fallopiantube, fat, gallbladder, heart, kidney, liver, lung, lymphnode, ' \
                    'ovary, placenta, prostate, rectum, salivarygland, skeletalmuscle, skin, ' \
                    'smallintestine, smoothmuscle, spleen, stomach, testis, thyroid, tonsil) VALUES ' \
                    '("%s", "%s", "%s", "%s", "%s"'%(sourceName, targetName, sourceType, targetType, interactionType)
            for weight in weights:
                query += ', ' + str(weight)
            query += ');'
            self.insertQuery(query)

        def updateGTExTable(self, sourceName, targetName, sourceType, targetType, interactionType, weights):
            query = 'INSERT INTO DifferentialInteractomes.GTEx' \
                    '(SourceName, TargetName, SourceType, TargetType, InteractionType, Adipose_Subcutaneous,' \
                    'Adipose_Visceral_Omentum, Artery_Aorta,' \
                    'Artery_Coronary, Artery_Tibial,' \
                    'Brain_Amygdala, Brain_Anterior_cingulate_cortex_BA24,' \
                    'Brain_Caudate_basal_ganglia, Brain_Cerebellar_Hemisphere,' \
                    'Brain_Cerebellum, Brain_Cortex, Brain_Frontal_Cortex_BA9,' \
                    'Brain_Hippocampus, Brain_Hypothalamus, Brain_Nucleus_accumbens_basal_ganglia,' \
                    'Brain_Putamen_basal_ganglia, Brain_Spinal_cord_cervical_c_1,' \
                    'Brain_Substantia_nigra, Breast_Mammary_Tissue, Cells_EBV_transformed_lymphocytes,' \
                    'Cells_Transformed_fibroblasts, Colon_Sigmoid, Esophagus_Gastroesophageal_Junction,' \
                    'Esophagus_Mucosa, Esophagus_Muscularis, Heart_Atrial_Appendage, Heart_Left_Ventricle,' \
                    'Liver, Lung, Minor_Salivary_Gland, Muscle_Skeletal, Nerve_Tibial, Ovary, Pituitary,' \
                    'Prostate, Skin_Not_Sun_Exposed_Suprapubic, Skin_Sun_Exposed_Lower_leg, ' \
                    'Stomach, Testis, Thyroid, Uterus, Vagina, Whole_Blood, Whole_Brain) VALUES ' \
                    '("%s", "%s", "%s", "%s", "%s"'%(sourceName, targetName, sourceType, targetType, interactionType)
            for weight in weights:
                query += ', ' + str(weight)
            query += ');'
            self.insertQuery(query)




        #Selects
        def getInteractions(self, gene, tissue, db):
            """
            This method will get interactions from the server.

            Parameters
            ----------
                gene : String
                    The database form which to get interactions.

            Return
            ------
                A set of tuples of the interactions from this database for this organism.

            History
            -------
                13/3/16 - Added by Omer Basha
            """
            interactions = set([])
            rows = self.execute("""SELECT d.SourceName, d.TargetName, d.SourceType, d.TargetType, d.InteractionType d.%s
                                    FROM DifferentialInteractomes.%s d
                                    WHERE ((d.SourceName = '%s') OR (d.TargetName= '%s'))"""%(tissue, db, gene, gene))
            for row in rows:
                sourceName = row[0]
                targetName = row[1]
                sourceType = row[2]
                targetType = row[3]
                interactionType = row[4]
                weight = row[5]

                interactions.add((sourceName, targetName, sourceType, targetType, interactionType, weight))

            return interactions

    __instance = None

    def __init__(self):

        """ Create singleton instance """
        # Check whether we already have an instance
        if SQLConnection.__instance is None:
            # Create and remember instance
            print "Creating SQL singleton"
            SQLConnection.__instance = SQLConnection.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_SQLConnection__instance'] = SQLConnection.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

if __name__ == "__main__":
    sc = SQLConnection()
    #sc.createMITable()
    #sc.uploadMITable("Data/MI_ontology")
    #sc.createUpdatesTable()
    #sc.createInteractionsTable()
    #sc.uploadDatabasesDate()
    #sc.createEmptyAndNonResponsiveTables()
    #print sc.CheckForUpdateDates(["BioGrid"], 9606)
    sc.createNamesTable()