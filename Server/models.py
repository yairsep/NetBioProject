from app import db


class Df_Complete_Dataset(db.Model):
    __bind_key__ = 'netbio2'
    __table_args__ = {'schema': 'netbio2'}
    __table__ = db.Model.metadata.tables['df_complete_dataset']
