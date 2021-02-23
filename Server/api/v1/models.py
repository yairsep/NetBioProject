from api.v1.database import db
from sqlalchemy import func


class Relevant_Benign_GRCh37(db.Model):
        __bind_key__ = 'netbio1'
        __table_args__ = {'schema': 'netbio1'}
        __table__ = db.Model.metadata.tables['Relevant_Benign_GRCh37-v1.6_CADD']


class Relevant_Benign_GRCh38(db.Model):
        __bind_key__ = 'netbio1'
        __table_args__ = {'schema': 'netbio1'}
        __table__ = db.Model.metadata.tables['Relevant_Benign_GRCh38-v1.6_CADD']

class Relevant_Pathogenic_GRCh37(db.Model):
        __bind_key__ = 'netbio1'
        __table_args__ = {'schema': 'netbio1'}
        __table__ = db.Model.metadata.tables['Relevant_Pathogenic_GRCh37-v1.6_CADD']

class Relevant_Pathogenic_GRCh38(db.Model):
        __bind_key__ = 'netbio1'
        __table_args__ = {'schema': 'netbio1'}
        __table__ = db.Model.metadata.tables['Relevant_Pathogenic_GRCh38-v1.6_CADD']

# class GenesPositions(db.Model):
#     __bind_key__ = 'TRACE'
#     __table_args__ = {'schema': 'TRACE'}
#     __table__ = db.Model.metadata.tables['GenesPositions']
#
# class PredictedScores(db.Model):
#     __bind_key__ = 'TRACE'
#     __table_args__ = {'schema': 'TRACE'}
#     __table__ = db.Model.metadata.tables['PredictedScores']

# class Interactions(db.Model):
#     __bind_key__ = 'TissueExpressionData'
#     __table_args__ = {'schema': 'TissueExpressionData'}
#     __table__ = db.Model.metadata.tables['interactions_with_mi']
#
#
# class GTEx(db.Model):
#     __bind_key__ = 'TissueExpressionData'
#     __table_args__ = {'schema': 'TissueExpressionData'}
#     __table__ = db.Model.metadata.tables['GTEx']
#
# class AgeDifferentialGTEx(db.Model):
#     #__bind_key__ = 'DifferentialInteractomes'
#     __table_args__ = {'schema': 'AgeNet'}
#     __table__ = db.Model.metadata.tables['AgeDifferentialGTEx']

    # @classmethod
    # def random_gene(cls):
    #     return cls.query.order_by(func.random()).first().SourceName


# class MI(db.Model):
#     __bind_key__ = 'TissueExpressionData'
#     __table__ = db.Model.metadata.tables['mi']
#
# class Updates(db.Model):
#     __bind_key__ = 'Interactions'
#     __table_args__ = {'schema': 'Interactions'}
#     __table__ = db.Model.metadata.tables['Updates']
#
#     @classmethod
#     def getWorkingVersion(cls):
#         q = cls.query.all()
#         if q[0].Date > q[1].Date:
#             return q[0].DBv
#         else:
#             return q[1].DBv

# class DifferentialInteractions(db.Model):
#     __bind_key__ = 'TissueExpressionData'
#     __table__ = db.Model.metadata.tables['interactions_with_mi']
#
#
# class GeneToDisease(db.Model): #Interactions
#     __bind_key__ = 'Interactions'
#     __table__ = db.Model.metadata.tables['GeneToDisease']
#
# class NamesA(db.Model):
#     import re
#     __bind_key__ = 'Interactions'
#     __table_args__ = {'schema': 'Interactions'}
#     __table__ = db.Model.metadata.tables['NamesA']
#     ENSEMBL_RE = re.compile(
#         "ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?|CG[0-9]+|[A-Z0-9]+\.[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]")
#     ENTREZ_RE = re.compile("[0-9]+|[A-Z]{1,2}_[0-9]+|[A-Z]{1,2}_[A-Z]{1,4}[0-9]+")
#
#     @classmethod
#     def common_name(cls, ensembl):
#         return cls.query.filter(Ensembl=ensembl).limit(1).first().Symbol
#
#     @classmethod
#     def entrez(cls, ensembl):
#         return cls.query.filter(Ensembl=ensembl).limit(1).first().Entrez
#
#     @classmethod
#     def names(cls, gene):
#         if gene.isdigit():
#             return cls.query.filter(Entrez=gene).all()
#
#     @classmethod
#     def ensembl(cls, symbol):
#         try:
#             q = cls.query.filter_by(Symbol=symbol).first().Ensembl
#             # print(q)
#             return q
#         except AttributeError:
#             return 'null'
#
#             # .limit(1).first().Ensembl
#
#     @classmethod
#     def genes_list_to_ensembl(cls, list):
#         ensembles = []
#         for gene in list:
#             if cls.ENSEMBL_RE.match(gene):
#                 ensembles.append(gene)
#             else:
#                 ensembles.append(cls.ensembl(gene))
#             # print('gene', gene, 'ensembles', ensembles)
#
#
#         return ensembles
#
#     @classmethod
#     def check_name(cls, gene):
#         if cls.ENSEMBL_RE.match(gene):
#             return [cls.query.filter_by(Ensembl=gene).first().Ensembl]
#         elif cls.ENTREZ_RE.match(gene):
#             return set([gene.Ensembl for gene in cls.query.filter_by(Entrez=gene).distinct(cls.Ensembl).all()])
#         else:
#             return set([gene.Ensembl for gene in cls.query.filter_by(Symbol=gene).distinct(cls.Ensembl).all()])
#
#
# class NamesB(db.Model):  # Interactions
#     import re
#     __bind_key__ = 'Interactions'
#     __table__ = db.Model.metadata.tables['NamesB']
#     ENSEMBL_RE = re.compile(
#         "ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?|CG[0-9]+|[A-Z0-9]+\.[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]")
#     ENTREZ_RE = re.compile("[0-9]+|[A-Z]{1,2}_[0-9]+|[A-Z]{1,2}_[A-Z]{1,4}[0-9]+")
#
#     @classmethod
#     def common_name(cls, ensembl):
#         return cls.query.filter(Ensembl=ensembl).limit(1).first().Symbol
#
#     @classmethod
#     def entrez(cls, ensembl):
#         return cls.query.filter(Ensembl=ensembl).limit(1).first().Entrez
#
#     @classmethod
#     def names(cls, gene):
#         if gene.isdigit():
#             return cls.query.filter(Entrez=gene).all()
#
#     @classmethod
#     def ensembl(cls, symbol):
#         try:
#             q = cls.query.filter_by(Symbol=symbol).first().Ensembl
#             # print(q)
#             return q
#         except AttributeError:
#             return 'null'
#
#             # .limit(1).first().Ensembl
#
#     @classmethod
#     def genes_list_to_ensembl(cls, list):
#         ensembles = []
#         for gene in list:
#             if cls.ENSEMBL_RE.match(gene):
#                 ensembles.append(gene)
#             else:
#                 ensembles.append(cls.ensembl(gene))
#             # print('gene', gene, 'ensembles', ensembles)
#
#         return ensembles
#
#     @classmethod
#     def check_name(cls, gene):
#         if cls.ENSEMBL_RE.match(gene):
#             return [cls.query.filter_by(Ensembl=gene).first().Ensembl]
#         elif cls.ENTREZ_RE.match(gene):
#             return set([gene.Ensembl for gene in cls.query.filter_by(Entrez=gene).distinct(cls.Ensembl).all()])
#         else:
#             return set([gene.Ensembl for gene in cls.query.filter_by(Symbol=gene).distinct(cls.Ensembl).all()])

