import time
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import pandas as pd

import xgboost as xgb
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap  # package used to calculate Shap values
pd.options.mode.chained_assignment = None
import pickle

"---------------------------- Load Data ------------------------------"

# path = os.path.join('..', '..', 'Data', 'Runing_ML_data', 'New_Verssion_data', 'hg37_Dataset',  'Toy_Example_Slim_Dataset_hg37-v1.6.csv')
path = os.path.join('..', '..', 'Data', 'Runing_ML_data', 'New_Verssion_data', 'hg37_Dataset',  'Full_Slim_Dataset_hg37-v1.6.csv')
Slim_dataset = pd.read_csv(path, engine='python')#low_memory=False,
print(Slim_dataset)

path = os.path.join('..', '..', 'Data', 'Birk data', 'MetaData', 'MetaData_New2.csv')
Metadata = pd.read_csv(path)
print(Metadata)

filename = os.path.join('..', '..', 'Final_Results', 'Random_Forest', 'AUC_plots', 'RF_best_parameters_dict.pkl')
infile = open(filename,'rb')
rf_best_parameters_dict = pickle.load(infile)
infile.close()

"-------------------------- Data PreProcessing ------------------------"

def preprocessing_data(Relevant_Data):

    one_hot_columns = ['Type', 'AnnoType', 'Consequence', 'Domain', 'Dst2SplType']  # , 'EnsembleRegulatoryFeature'

    # Get one hot encoding of columns B
    one_hot = pd.get_dummies(Relevant_Data[one_hot_columns])
    # Drop column B as it is now encoded
    Relevant_Data = Relevant_Data.drop(one_hot_columns, axis=1)
    # Join the encoded df
    Relevant_Data = Relevant_Data.join(one_hot)
    # print(relevant_data_1)
    cHmm_columns = Slim_dataset.columns[Slim_dataset.columns.str.contains(pat='cHmm_E')].tolist()
    fill_zero_columns = ['motifECount', 'motifEHIPos', 'motifEScoreChng', 'mirSVR-Score', 'mirSVR-E', 'mirSVR-Aln',
                         'tOverlapMotifs', 'motifDist'] + cHmm_columns  # motifs with high number of nan 97%
    Relevant_Data[fill_zero_columns] = Relevant_Data[fill_zero_columns].fillna(value=0)
    fill_common_columns = ['cDNApos', 'relcDNApos', 'CDSpos', 'relCDSpos', 'protPos', 'relProtPos', 'Dst2Splice',
                           'SIFTval', 'PolyPhenVal', 'GerpRS', 'GerpRSpval', 'GerpN', 'GerpS', 'all Enc',
                           'Grantham', 'All SpliceAI', 'All MMSp', 'Dist2Mutation', 'All 00bp', 'dbscSNV',
                           'RemapOverlapTF', 'RemapOverlapCL', 'Trace Features']  # Locations, is this right?
    for cl in list(Relevant_Data):
        Relevant_Data[cl] = Relevant_Data[cl].fillna(Relevant_Data[cl].value_counts().idxmax())
    return Relevant_Data


y_columns = Slim_dataset.columns[Slim_dataset.columns.str.contains(pat = 'disease_causing')].tolist()
print(y_columns)
non_relevant_columns = ['VariationID', 'OMIMs', 'Manifested_Tissues', '#Chr', 'Pos', 'ConsDetail', 'motifEName', 'GeneID_y', 'FeatureID', 'GeneName', 'CCDS', 'Intron', 'Exon', 'SIFTcat', 'PolyPhenCat', 'bStatistic', 'targetScan', 'dbscSNV-rf_score', 'oAA', 'Ref', 'nAA', 'Alt', 'Segway']# it will be good to replace oAA and nAA with blssuom64 matrix. What bStatistic doing?
non_relevant_columns = non_relevant_columns + y_columns
non_relevant_patient = ['#Chr', 'Pos', 'ConsDetail', 'motifEName', 'GeneID_y', 'FeatureID', 'GeneName', 'CCDS', 'Intron', 'Exon', 'SIFTcat', 'PolyPhenCat', 'bStatistic', 'targetScan', 'dbscSNV-rf_score', 'oAA', 'Ref', 'nAA', 'Alt', 'Segway']# it will be good to replace oAA and nAA with blssuom64 matrix. What bStatistic doing?

# Patient_relevant = Patient_data[set(list(Patient_data)) ^ set(non_relevant_patient)]
# relevant_columns = set(list(Slim_dataset)) ^ set(non_relevant_columns)
cols = Slim_dataset.columns
relevant_columns = [x for x in cols if x not in non_relevant_columns]
Slim_Relevant = Slim_dataset[relevant_columns]
Slim_Relevant = preprocessing_data(Slim_Relevant)

for y in y_columns:
    tissue = y.replace("_disease_causing", "")
    print('-----------------', tissue, '-----------------')
    try:
        best_parameters = rf_best_parameters_dict[tissue.strip()][1]
        model = RandomForestClassifier(**best_parameters)
        model.fit(Slim_Relevant, Slim_dataset[y])

        path = os.path.join('..', '..', 'Webtool_Files', 'Prediction_Models', tissue.strip() + '_RF_Model.pkl')
        with open(path, 'wb') as handle:
            pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        print(tissue, ' have no validated model.')

    features_dict = {feature: Slim_Relevant[feature].value_counts().idxmax() for feature in Slim_Relevant}
    path = os.path.join('..', '..', 'Webtool_Files', 'Prediction_Models', tissue.strip() + '_Features_dict.pkl')
    with open(path, 'wb') as handle:
        pickle.dump(features_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)