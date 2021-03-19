from sqlalchemy import or_
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from NetBioProject.Server.Utils.utils import merge_by_key
from NetBioProject.Server.Database.models import NamesA, GeneToDisease

class GeneSchema(ModelSchema):
    @classmethod
    def process_to_object(cls, genes):
        ids = [item['Gene'] for item in genes]
        print(genes)
        diseaseGenes = DiseaseSchema(many=True).dump(GeneToDisease.query.filter(GeneToDisease.GeneID.in_(ids)))
        from api.v1.app import getWorkingVersion
        from importlib import import_module
        version = getWorkingVersion()
        models = 'api.v1.models'
        names = getattr(import_module(models), 'Names{}'.format(version))

        aliases = AliasesSchema(many=True).dump(names.query.filter(names.Ensembl.in_(ids)).all())
        ret = merge_by_key(aliases, diseaseGenes, 'Ensembl', 'GeneID')
        ret = merge_by_key(ret, genes, 'Ensembl', 'Gene')
        for n in range(len(ret)):
            ret[n]['id'] = ret[n]['Ensembl']
        # return {'{}'.format(datum['Ensembl']): datum for datum in ret}
        return ret

    # class Meta:
    #     model = GTEx

class DiseaseSchema(ModelSchema):
    class Meta:
        fields = ('GeneID', 'MIM_morbid_accession', 'MIM_morbid_description')
        model = GeneToDisease

class AliasesSchema(ModelSchema):
    class Meta:
        fields = ('Ensembl', 'Symbol', 'Entrez', 'GeneType')
# was B rotem change to A
        model = NamesA

class NamesASchema(ModelSchema):
    title = fields.Str(attribute='Symbol')
    description = fields.Method('build_description')

    def build_description(self, obj):
        stmt = or_(self.context.SourceName == obj.Ensembl, self.context.TargetName == obj.Ensembl)
        if self.context.query.filter(stmt).first() is not None:
            interactions = True
        else:
            interactions = False
        return {
            'ensembl': obj.Ensembl,
            'entrez': obj.Entrez,
            'interactions': interactions
        }

    class Meta:
        model = NamesA
