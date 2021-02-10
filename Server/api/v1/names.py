"""
    names
    ~~~~~

    A utility module for all manners of gene names matching, regex-ing
    and database querying.
"""
import re

from api.v1.models import Updates

from api.v1.database import db

# Regex for ENSEMBL & ENTREZ validation.
ENSEMBL_RE = re.compile("ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?|CG[0-9]+|[A-Z0-9]+[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]")
ENTREZ_RE = re.compile("[0-9]+|[A-Z]{1,2}_[0-9]+|[A-Z]{1,2}_[A-Z]{1,4}[0-9]+")

def _latest_table_version():
    ver = Updates.query.order_by(Updates.Date.desc()).limit(1).first().DBv
    return 'A' if ver == 'A' else 'B'


# Bind to most up-to-date Interactions and Names tables.
class Interactions(db.Model):
    __bind_key__ = 'Interactions'
    __table__ = db.Model.metadata.tables['Interactions' + _latest_table_version()]


class Names(db.Model):
    __bind_key__ = 'Interactions'
    __table__ = db.Model.metadata.tables['Names' + _latest_table_version()]


def is_valid_gene_name(candidate):
    id_type = get_id_type(candidate)

    if id_type is 'ENSEMBL':
        return Names.query.filter_by(ENSEMBL=candidate).limit(1).all(), id_type
    elif id_type is 'ENTREZ':
        return Names.query.filter_by(ENTEZ=candidate).with_entities('ENSEMBL').all(), id_type
    else:
        return Names.query.filter_by(Symbol=candidate).with_entities('ENSEMBL').all(), id_type


def get_id_type(gene):
    if ENSEMBL_RE.match(gene):
        return 'ENSEMBL'
    elif ENTREZ_RE.match(gene):
        return 'ENTREZ'
    else:
        return 'Symbol'


def is_ambiguous_gene_name(candidate):
    ids, id_type = is_valid_gene_name(candidate)
    if not ids:
        return None
    elif len(ids) > 1:
        return True, candidate, ids, id_type
    elif len(ids) == 1:
        return False, candidate, ids, id_type


def get_gene_identifiers(gene):
    pass

