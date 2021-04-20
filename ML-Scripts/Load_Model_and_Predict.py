
import os
import pandas as pd
pd.options.mode.chained_assignment = None
import pickle
from sklearn.ensemble import RandomForestClassifier

"---------------------------- Load Data ------------------------------"
file_name = 'CardiomyopathyOtB0551_CADD_GRCh37-v1.6.csv' #TODO: Get the name from args[0]
short_name = file_name.split('_')[0]
patient_cadd_path = os.path.join('..', 'Data', file_name)
Patient_CADD_data = pd.read_csv(patient_cadd_path)

trace_features_path = os.path.join('..', 'Data', 'df_complete_dataset.csv') #TODO: Get the name from args[1]
TRACE_data = pd.read_csv(trace_features_path)

tissue = 'Heart - Left Ventricle' #TODO: Get the tissue from args[2]
relevant_model_path = os.path.join('..', 'Prediction_Models', tissue.strip() + '_RF_Model.pkl') #TODO: Add the folder to the cluster
with open(relevant_model_path, 'rb') as handle:
    model = pickle.load(handle)

features_model_path = os.path.join('..', 'Prediction_Models', 'Lung' + '_Features_dict.pkl')
with open(features_model_path, 'rb') as handle:
    model_features_dict = pickle.load(handle)

"-------------------------- Data PreProcessing ------------------------"

def edit_trace_data(TRACE_data):

    TRACE_data = TRACE_data.rename(columns={'Unnamed: 0': 'GeneID_y'})
    trace_features = list(TRACE_data)
    relevant_trace_features = [x for x in trace_features if "_causal" not in x]
    Relevant_TRACE = TRACE_data[relevant_trace_features]
    Relevant_TRACE = Relevant_TRACE[Relevant_TRACE.filter(regex='^((?!embedding).)*$').columns]
    Relevant_TRACE = Relevant_TRACE.fillna(0)
    return Relevant_TRACE

def edit_cadd_data(Relevant_Data):
    cols = list( Relevant_Data)
    print('Relevant_Data',cols)
    one_hot_columns = ['Type', 'AnnoType', 'Consequence', 'Domain', 'Dst2SplType']  # , 'EnsembleRegulatoryFeature'

    # Get one hot encoding of columns B
    one_hot = pd.get_dummies(Relevant_Data[one_hot_columns])
    # Drop column B as it is now encoded
    Relevant_Data = Relevant_Data.drop(one_hot_columns, axis=1)
    # Join the encoded df
    Relevant_Data = Relevant_Data.join(one_hot)
    print('relevant_data_1: ', Relevant_Data)
    cHmm_columns = Relevant_Data.columns[Relevant_Data.columns.str.contains(pat='cHmm_E')].tolist()
    fill_zero_columns = ['motifECount', 'motifEHIPos', 'motifEScoreChng', 'mirSVR-Score', 'mirSVR-E', 'mirSVR-Aln','tOverlapMotifs', 'motifDist'] + cHmm_columns  # motifs with high number of nan 97%
    Relevant_Data[fill_zero_columns] = Relevant_Data[fill_zero_columns].fillna(value=0)
    fill_common_columns = ['cDNApos', 'relcDNApos', 'CDSpos', 'relCDSpos', 'protPos', 'relProtPos', 'Dst2Splice',
                           'SIFTval', 'PolyPhenVal', 'GerpRS', 'GerpRSpval', 'GerpN', 'GerpS', 'all Enc',
                           'Grantham', 'All SpliceAI', 'All MMSp', 'Dist2Mutation', 'All 00bp', 'dbscSNV',
                           'RemapOverlapTF', 'RemapOverlapCL', 'Trace Features']  # Locations, is this right?
    for cl in list(Relevant_Data):
        # print(cl)
        # print(Relevant_Data[cl])
        try:
            Relevant_Data[cl] = Relevant_Data[cl].fillna(Relevant_Data[cl].value_counts().idxmax())
        except:
            Relevant_Data[cl] = Relevant_Data[cl].fillna(0)
    return Relevant_Data

def merge_trace_and_cadd_data(Edited_CADD_data, Relevant_TRACE):
    Model_input = pd.merge(Edited_CADD_data, Relevant_TRACE, how='inner', on='GeneID_y')
    return Model_input

Relevant_TRACE = edit_trace_data(TRACE_data)
print(Relevant_TRACE)
non_relevant_patient = ['#Chr', 'Pos', 'ConsDetail', 'motifEName',  'FeatureID', 'GeneName', 'CCDS', 'Intron', 'Exon', 'SIFTcat', 'PolyPhenCat', 'bStatistic', 'targetScan', 'dbscSNV-rf_score', 'oAA', 'Ref', 'nAA', 'Alt', 'Segway']# it will be good to replace oAA and nAA with blssuom64 matrix. What bStatistic doing?
relevant_cols = [c for c in list(Patient_CADD_data) if c not in non_relevant_patient]
Edited_CADD_data = edit_cadd_data(Patient_CADD_data[relevant_cols])
print(Edited_CADD_data)

Model_input = merge_trace_and_cadd_data(Edited_CADD_data, Relevant_TRACE)
relevant_input_cols = [c for c in list(Model_input) if c != 'GeneID_y']
Model_input = Model_input[relevant_input_cols]

"--------------------- Deal with Missed Features ----------------------------------"

model_features = [*model_features_dict]
print(model_features)
missed_features_in_patient = [x for x in model_features if x not in list(Model_input)]
print('missed_features_in_patient', missed_features_in_patient)
missed_features_in_model = [x for x in list(Model_input) if x not in model_features]
print('missed_features_in_model', missed_features_in_model)
for missed_f in missed_features_in_patient:
    Model_input[missed_f] = model_features_dict[missed_f]
relevant_input_cols_2 = [f for f in list(Model_input) if f not in missed_features_in_model]

"--------------------- Prioritize Patient Variants ----------------------------------"

patient_predict_proba = model.predict_proba(Model_input[relevant_input_cols_2]) #[common_features]
print(patient_predict_proba)
patient_predictions = patient_predict_proba[:, 1]
prediction_df = pd.DataFrame(patient_predictions, columns=['Pathological_probability'])
Results_df = pd.concat([Patient_CADD_data, prediction_df], axis=1)
Relevant_Results = Results_df[['GeneName', 'GeneID_y', '#Chr', 'Pos', 'Ref', 'Alt', 'Type', 'Length','SIFTval', 'PolyPhenVal', 'PHRED', 'Pathological_probability']]
Relevant_Results = Relevant_Results.sort_values('Pathological_probability', ascending=False)
print(Relevant_Results)
out_put_path = os.path.join('..', 'Data', short_name + '_' + tissue + '_Prediction_output.csv')
Relevant_Results.to_csv(out_put_path, index=False)
