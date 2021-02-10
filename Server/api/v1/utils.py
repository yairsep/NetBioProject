from toolz import keyfilter, dissoc


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


def merge_dicts(*dictionaries):
    d = {}
    for dictionary in dictionaries:
        for key in dictionary:
            try:
                d[key].append(dictionary[key])
            except KeyError:
                d[key] = [dictionary[key]]
    return d


# TODO: Refactor to be more general
def merge_by_key(dict1, dict2, key1, key2):
    keyed_dict1 = {datum[key1]: datum for datum in dict1}
    keyed_dict2 = {datum[key2]: dissoc(datum, key2) for datum in dict2}
    # print('dict1 %d'%(len(keyed_dict1)))
    # print('dict2 %d'%(len(keyed_dict2)))
    keys = list(set(list(keyed_dict1.keys())).intersection(set(list(keyed_dict2.keys()))))

    merged = {}
    for key in keys:
        merged.update({key: {**keyed_dict1[key], **keyed_dict2[key]}})

    return list(merged.values())


GTExTissues = {
    'Adipose_Subcutaneous': 'Adipose - Subcutaneous',
    'Adipose_Visceral_Omentum': 'Adipose - Visceral (Omentum)',
    'Adrenal_Gland': 'Adrenal - Gland',
    'Artery_Aorta': 'Artery - Aorta',
    'Artery_Coronary': 'Artery - Coronary',
    'Artery_Tibial': 'Artery - Tibial',
    'Fallopian_Tube': 'Fallopian Tube',
    'Whole_Brain': 'Brain - Whole Brain',
    'Bladder': 'Bladder',
    'Brain_Amygdala': 'Brain - Amygdala',
    'Brain_Anterior_cingulate_cortex_BA24': 'Brain - Anterior cingulate cortex (BA24)',
    'Brain_Caudate_basal_ganglia': 'Brain - Caudate (basal ganglia)',
    'Brain_Cerebellar_Hemisphere': 'Brain - Cerebellar Hemisphere',
    'Brain_Cerebellum': 'Brain - Cerebellum',
    'Brain_Cortex': 'Brain - Cortex',
    'Brain_Frontal_Cortex_BA9': 'Brain - Frontal Cortex (BA9)',
    'Brain_Hippocampus': 'Brain - Hippocampus',
    'Brain_Hypothalamus': 'Brain - Hypothalamus',
    'Brain_Nucleus_accumbens_basal_ganglia': 'Brain - Nucleus accumbens (basal ganglia)',
    'Brain_Putamen_basal_ganglia': 'Brain - Putamen (basal ganglia)',
    'Brain_Spinal_cord_cervical_c_1': 'Brain - Spinal cord (cervical c-1)',
    'Brain_Substantia_nigra': 'Brain - Substantia nigra',
    'Breast_Mammary_Tissue': 'Breast - Mammary Tissue',
    'Cervix_Ectocervix': 'Cervix - Ectocervix',
    'Cervix_Endocervix': 'Cervix - Endocervix',
    'Colon_Sigmoid': 'Colon - Sigmoid',
    'Colon_Transverse': 'Colon - Transverse',
    'Esophagus_Gastroesophageal_Junction': 'Esophagus - Gastroesophageal Junction',
    'Esophagus_Mucosa': 'Esophagus - Mucosa',
    'Esophagus_Muscularis': 'Esophagus - Muscularis',
    'Heart_Atrial_Appendage': 'Heart - Atrial Appendage',
    'Heart_Left_Ventricle': 'Heart - Left Ventricle',
    'Kidney_Cortex': 'Kidney - Cortex',
    'Liver': 'Liver',
    'Lung': 'Lung',
    'Minor_Salivary_Gland': 'Minor Salivary Gland',
    'Muscle_Skeletal': 'Muscle - Skeletal',
    'Nerve_Tibial': 'Nerve - Tibial',
    'Ovary': 'Ovary',
    'Pancreas': 'Pancreas',
    'Pituitary': 'Pituitary',
    'Prostate': 'Prostate',
    'Skin_Not_Sun_Exposed_Suprapubic': 'Skin - Not Sun Exposed (Suprapubic)',
    'Skin_Sun_Exposed_Lower_leg': 'Skin - Sun Exposed (Lower leg)',
    'Small_Intestine_Terminal_Ileum': 'Small Intestine - Terminal Ileum',
    'Spleen': 'Spleen',
    'Stomach': 'Stomach',
    'Testis': 'Testis',
    'Thyroid': 'Thyroid',
    'Uterus': 'Uterus',
    'Vagina': 'Vagina',
    'Whole_Blood': 'Whole Blood',
    'Thyroid': 'Thyroid',
}

# sample_genes = [
#     "GCLC", "DAG1", "ENSG00000012048", "ENSG00000001629", "ENSG00000004864", "ENSG00000004779", "ENSG00000005194",
#     "ENSG00000005421", "ENSG00000005436", "ENSG00000006047", "ENSG00000006071", "ENSG00000006327", "ENSG00000006534",
#     "ENSG00000006555", "ENSG00000006576", "ENSG00000006659", "ENSG00000006695", "ENSG00000006712", "ENSG00000006744",
#     "ENSG00000007047", "ENSG00000007080"
# ]

sample_genes = [
    "SLC25A13", "BRCA1", "PON1", "CIAPIN1", "ALDH3B1", "DAG1", "NDUFAB1", "PAF1", "GCLC", "DMD", "COX10", "OPA1", "BX2",
    "ELAC2", "GNB1", "CCDC124", "LGALS14",
    "TNFRSF12A", "TP63", "SEC31A", "GAN", "TTC22", "ANKIB1", "GCFC2", "SYP", "SGCG", "SYN1", "MARK4", "PHTF2", "IL36RN",
    "ABCC8"
]

sample = [{
        'GeneName': 'TTN',
        'GeneID': 'ENSG00000155657',
        'Chr': '2',
        'Pos': 179639114,
        'Ref': 'C',
        'Alt': 'G',
        'Type': 'SNV',
        'Length': 0,
        'SITFval': None,
        'PolyPhenVal': None,
        'PHRED': 22.7,
        'Pathological_probability': 0.323333333,
    },
    {
        'GeneName': 'HTT',
        'GeneID': 'ENSG00000197386',
        'Chr': '4',
        'Pos': 3133374,
        'Ref': 'C',
        'Alt': 'T',
        'Type': 'SNV',
        'Length': 0,
        'SITFval': 0.1,
        'PolyPhenVal': 0.999,
        'PHRED': 24.4,
        'Pathological_probability': 0.32125,
    }
]
