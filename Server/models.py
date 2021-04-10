from app import db

#
# class Relevant_Benign_GRCh37(db.Model):
#     __bind_key__ = 'netbio1'
#     __table_args__ = {'schema': 'netbio1'}
#     __table__ = db.Model.metadata.tables['Relevant_Benign_GRCh37-v1.6_CADD']
#
#
# class Relevant_Benign_GRCh38(db.Model):
#     __bind_key__ = 'netbio1'
#     __table_args__ = {'schema': 'netbio1'}
#     __table__ = db.Model.metadata.tables['Relevant_Benign_GRCh38-v1.6_CADD']
#
#
# class Relevant_Pathogenic_GRCh37(db.Model):
#     __bind_key__ = 'netbio1'
#     __table_args__ = {'schema': 'netbio1'}
#     __table__ = db.Model.metadata.tables['Relevant_Pathogenic_GRCh37-v1.6_CADD']
#
#
# class Relevant_Pathogenic_GRCh38(db.Model):
#     __bind_key__ = 'netbio1'
#     __table_args__ = {'schema': 'netbio1'}
#     __table__ = db.Model.metadata.tables['Relevant_Pathogenic_GRCh38-v1.6_CADD']

class Df_Complete_Dataset(db.Model):
    __bind_key__ = 'netbio2'
    __table_args__ = {'schema': 'netbio2'}
    __table__ = db.Model.metadata.tables['df_complete_dataset']