from collections import namedtuple
from itertools import chain, groupby

from decimal import Decimal
from sqlalchemy import or_
from marshmallow import Schema, fields, post_dump
from marshmallow_sqlalchemy import ModelSchema
from toolz import pluck, dissoc

from .utils import pick, merge_by_key, GTExTissues
from .models import NamesA, NamesB, GeneToDisease
# from .models import Interactions, NamesA, NamesB, GTEx, GeneToDisease, AgeDifferentialGTEx
# from .models import DifferentialGTEx, DifferentialHPA, Interactions, NamesB, NamesA, GTEx, HPA, GeneToDisease, \
#     DifferentialHPAPercentile, DifferentialGTExPercentile



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

# class GTExCytoscapeJsonNodeSchema(ModelSchema):
#
#     @post_dump(pass_many=True)
#     def process_to_object(self, data, many):
#         ids = [datum['Gene_identifier'] for datum in data]
#         diseaseGenes = DiseaseSchema(many=True).dump(GeneToDisease.query.filter(GeneToDisease.GeneID.in_(ids))).data
#         from api.v1.app import getWorkingVersion
#         from importlib import import_module
#         version = getWorkingVersion()
#         models = 'api.v1.models'
#         names = getattr(import_module(models), 'Names{}'.format(version))
#
#         aliases = AliasesSchema(many=True).dump(names.query.filter(names.Ensembl.in_(ids)).all()).data
#         #print(aliases, diseaseGenes)
#         ret = merge_by_key(aliases, diseaseGenes, 'Ensembl', 'GeneID')
#         ret = merge_by_key(ret, data, 'Ensembl', 'Gene_identifier')  #
#         for n in range(len(ret)):
#             ret[n]['id'] = ret[n]['Ensembl']
#         retObj = [{"data": datum, 'position': {"x": 0.0, "y": 0.0}, 'group': 'nodes', 'removed': False,
#                    'selected': False, 'seletable': True, 'locked': False, 'grabbable': True, 'classes': ""} for datum in ret]
#         for datum in retObj:
#             if datum["data"]["MIM_morbid_accession"] == '':
#                 datum['data']['MIM_morbid_accession'] = 'N/A'
#                 datum['data']['MIM_morbid_description'] = 'N/A'
#                 datum['data']['shape'] = 'ellipse'
#             else:
#                 datum['data']['shape'] = 'octagon'
#         # print(retObj)
#         return retObj
#
#     # class Meta:
#     #     model = GTEx
#
class AliasesSchema(ModelSchema):
    class Meta:
        fields = ('Ensembl', 'Symbol', 'Entrez', 'GeneType')
# was B rotem change to A
        model = NamesA
#

#
#
# class InteractionsSchema(ModelSchema):
#     @post_dump(pass_many=True)
#     def process_to_object(self, data, many):
#         if many:
#             keyfunc = lambda row: (row['source_id'], row['target_id'])
#             return [{'source_id': k[0],
#                      'target_id': k[1],
#                      'mi': [self.extract_mi_list(item) for item in list(g)]
#                      }
#                     for k, g in groupby(data, keyfunc)
#                     ]
#
#     def extract_mi_list(self, item):
#         return {k: v for k, v in item.items() if k not in ['source_id', 'target_id']}
#
#     class Meta:
#         model = Interactions
#
#
# class GTExSchema(ModelSchema):
#     @post_dump(pass_many=True)
#     def process_schema(self, data, many):
#         if many:
#             nodes = list(set(chain(*pluck(['SourceName', 'TargetName'], data))))
#             # print('Nodes: %s'%(str(nodes)))
#             edges = {(datum['SourceName'], datum['TargetName']): datum for datum in data}
#
#             q = Interactions.query.filter(Interactions.source_id.in_(nodes), Interactions.target_id.in_(nodes)).all()
#             from api.v1.app import getWorkingVersion
#             from importlib import import_module
#             version = getWorkingVersion()
#             models = 'api.v1.models'
#             names = getattr(import_module(models), 'Names{}'.format(version))
#             aliases = AliasesSchema(many=True).dump(names.query.filter(names.Ensembl.in_(nodes)).all()).data
#             aliasesDict = {}
#             for alias in aliases:
#                 aliasesDict[alias['Ensembl']] = alias['Symbol']
#             interactions = InteractionsSchema(many=True).dump(q).data
#
#             for i in interactions:
#                 key = (i['source_id'], i['target_id'])
#                 if key in edges:
#                     edges[key]['mi'] = i['mi']
#
#             for key in edges:
#                 edges[key]['source'] = edges[key]['SourceName']
#                 edges[key]['target'] = edges[key]['TargetName']
#
#             aliasNotFound = []
#             for key in edges:
#                 if not edges[key]['source'] in aliasesDict:
#                     aliasNotFound.append(key)
#                 if not edges[key]['target'] in aliasesDict:
#                     aliasNotFound.append(key)
#
#             for key in set(aliasNotFound):
#                 edges.pop(key)
#
#             for key in edges:
#                 edges[key]['sourceSymbol'] = aliasesDict[edges[key]['source']]
#                 edges[key]['targetSymbol'] = aliasesDict[edges[key]['target']]
#
#             return {'{}-{}'.format(datum['SourceName'], datum['TargetName']): self._format_edge(datum) for datum in
#                     edges.values()}
#
#     def _format_edge(self, datum):
#         #weight = datum['brain']
#         color = 1
#
#         #if weight < -0.1:
#         #    color = -1
#         #elif -0.1 <= weight <= 0.1:
#         #    color = 0
#
#         tissues = {}
#         for key in datum:
#             if not key in EDGE_ATTRIBUTES:
#                 if '_Weight' in key:
#                     if GTExTissues[key[:key.index('_Weight')]] in tissues:
#                         tissues[GTExTissues[key[:key.index('_Weight')]]]['Weight'] = float(datum[key])
#                     else:
#                         tissues[GTExTissues[key[:key.index('_Weight')]]] = {'Weight': float(datum[key])}
#                 elif '_Percentile' in key:
#                     if GTExTissues[key[:key.index('_Percentile')]] in tissues:
#                         tissues[GTExTissues[key[:key.index('_Percentile')]]]['Percentile'] = int(float(datum[key]))
#                     else:
#                         tissues[GTExTissues[key[:key.index('_Percentile')]]] = {'Percentile': int(float(datum[key]))}
#
#         return {
#             **pick(EDGE_ATTRIBUTES, datum),
#             'tissues': tissues,
#             'directed': False#,
#             #'weight': weight,
#             #'type': 'ppi',
#             #'color': color
#         }
#
#     class Meta:
#         model = AgeDifferentialGTEx
#
# class GTExCytoscapeJsonSchema(ModelSchema):
#     @post_dump(pass_many=True)
#     def process_schema(self, data, many):
#         if many:
#             nodes = list(set(chain(*pluck(['SourceName', 'TargetName'], data))))
#             # print('Nodes: %s'%(str(nodes)))
#             edges = {(datum['SourceName'], datum['TargetName']): datum for datum in data}
#
#             q = Interactions.query.filter(Interactions.source_id.in_(nodes), Interactions.target_id.in_(nodes)).all()
#             from api.v1.app import getWorkingVersion
#             from importlib import import_module
#             version = getWorkingVersion()
#             models = 'api.v1.models'
#             names = getattr(import_module(models), 'Names{}'.format(version))
#             aliases = AliasesSchema(many=True).dump(names.query.filter(names.Ensembl.in_(nodes)).all()).data
#             aliasesDict = {}
#             for alias in aliases:
#                 aliasesDict[alias['Ensembl']] = alias['Symbol']
#             interactions = InteractionsSchema(many=True).dump(q).data
#
#             for i in interactions:
#                 key = (i['source_id'], i['target_id'])
#                 if key in edges:
#                     edges[key]['mi'] = i['mi']
#
#             for key in edges:
#                 edges[key]['source'] = edges[key]['SourceName']
#                 edges[key]['target'] = edges[key]['TargetName']
#
#             aliasNotFound = []
#             for key in edges:
#                 if not edges[key]['source'] in aliasesDict:
#                     aliasNotFound.append(key)
#                 if not edges[key]['target'] in aliasesDict:
#                     aliasNotFound.append(key)
#
#             for key in set(aliasNotFound):
#                 edges.pop(key)
#
#             for key in edges:
#                 edges[key]['sourceSymbol'] = aliasesDict[edges[key]['source']]
#                 edges[key]['targetSymbol'] = aliasesDict[edges[key]['target']]
#
#             retObj = [{"data": self._format_edge(datum), 'position': {}, 'group': 'edges', 'removed': False,
#                        'selected': False, 'seletable': True, 'locked': False, 'grabbable': True, 'classes': ""} for
#                       datum in edges.values()]
#             for edge in retObj:
#                 for key in edge['data']:
#                     # print(type(edge['data'][key]))
#                     if type(edge['data'][key]) == Decimal:
#                         edge['data'][key] = float(edge['data'][key])
#                 edge['data']['id'] = '{}-{}'.format(edge['data']['SourceName'], edge['data']['TargetName'])
#
#             # print(retObj)
#             return retObj
#             # return {'{}-{}'.format(datum['SourceName'], datum['TargetName']): self._format_edge(datum) for datum in
#             #         edges.values()}
#
#
#     def _format_edge(self, datum):
#         #weight = datum['brain']
#         color = 1
#
#         #if weight < -0.1:
#         #    color = -1
#         #elif -0.1 <= weight <= 0.1:
#         #    color = 0
#
#         tissues = {}
#         for key in datum:
#             if not key in EDGE_ATTRIBUTES:
#                 if '_Weight' in key:
#                     if GTExTissues[key[:key.index('_Weight')]] in tissues:
#                         tissues[GTExTissues[key[:key.index('_Weight')]]]['Weight'] = float(datum[key])
#                     else:
#                         tissues[GTExTissues[key[:key.index('_Weight')]]] = {'Weight': float(datum[key])}
#                 elif '_Percentile' in key:
#                     if GTExTissues[key[:key.index('_Percentile')]] in tissues:
#                         tissues[GTExTissues[key[:key.index('_Percentile')]]]['Percentile'] = int(float(datum[key]))
#                     else:
#                         tissues[GTExTissues[key[:key.index('_Percentile')]]] = {'Percentile': int(float(datum[key]))}
#
#         return {
#             **pick(EDGE_ATTRIBUTES, datum),
#             'tissues': tissues,
#             'directed': False#,
#             #'weight': weight,
#             #'type': 'ppi',
#             #'color': color
#         }
#
#     class Meta:
#         model = AgeDifferentialGTEx
#
#
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
#
#
# class NamesBSchema(ModelSchema):
#     title = fields.Str(attribute='Symbol')
#     description = fields.Method('build_description')
#
#     def build_description(self, obj):
#         stmt = or_(self.context.SourceName == obj.Ensembl, self.context.TargetName == obj.Ensembl)
#         if self.context.query.filter(stmt).first() is not None:
#             interactions = True
#         else:
#             interactions = False
#
#         return {
#             'ensembl': obj.Ensembl,
#             'entrez': obj.Entrez,
#             'interactions': interactions
#         }
#
#     class Meta:
#         model = NamesB