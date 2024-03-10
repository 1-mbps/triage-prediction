import pandas as pd
import numpy as np

d = pd.read_csv("datasets/dataset_unclean.csv")

ds = d.copy()

# I wrote this code in 2020; I was 17 and I had no idea what I was doing. I'll change this to use sklearn pipelines someday
sbs=[x for x in ds if "RFV" not in x and x!="IMMEDR"]
ds['SEX'] = ds['SEX'].replace(['Male'], 0)
ds['SEX'] = ds['SEX'].replace(['Female'], 1)
ds['LWBS'].replace(['Yes'], np.nan) #Left without being seen = null
ds['LEFTAMA'].replace(['Yes'], np.nan) #Left against medical advice = null
ds['DOA'].replace(['Yes'], np.nan) #Dead on arrival = null
ds = ds.replace(['No', 'Public service (nonambulance)', 'Personal transportation'], 0)
ds = ds.replace(['Yes', 'Ambulance'], 1)
ds = ds.replace(['Blank', 'Unknown', 'nan', 'Entire item blank', 'Unknown (data not available)', 'Unknown (no data available)', 'Data not available (Unknown)', "'None' box and all item fields are blank", 'P or Palp', 'DOPP or DOPPLER', 'P, Palp, DOPP or DOPPLER', 'P, Palp, DOP or DOPPLER', 'DOP or DOPPLER', "Entire item blank, including 'None' box", "Entire item blank, including None box"], np.nan)
ds["ADMIT"] = ds["ADMIT"].replace(['Cardiac catheterization lab', 'Mental health or detox unit', 'Operating room', 'Other bed/unit', 'Stepdown unit', 'Stepdown or telemetry unit'], 'Hospitalization')
ds = ds.dropna(subset=["RFV1", "RFV2", "RFV3"],thresh=1,axis=0)
ds["ADMIT"] = ds["ADMIT"].replace(['Not applicable'], 'Discharge')
ds["AGE"] = ds["AGE"].replace(["Under one year"], 0)
ds["AGE"] = ds["AGE"].replace(["93 years and over"], 93)
ds["AGE"] = ds["AGE"].replace(["94 years and over"], 94)
ds["AGE"] = ds["AGE"].replace(["100 years and over"], 100)
# ds = ds.dropna(axis=0)
ds["IMMEDR"] = ds["IMMEDR"].replace(['No triage', 'Visit occured in ESA that does not conduct nursing triage', 'No triage for this visit but ESA does conduct triage', 'Visit occurred in ESA that does not conduct nursing triage'], np.nan)
ds = ds.dropna(subset=sbs,axis=0)

# conditions = [] #List of RFVs
# for x in range(1,4): #Loop through RFV columns 1-3
#     for x in ds["RFV"+str(x)]: #Loop through entries in each RFV column
#         conditions.append(x) #Get each reason for visit
# unique, counts = np.unique(conditions, return_counts=True)
# cdict = dict(zip(unique, counts)) #Store in dictionary, in tuple form: (RFV, number of times it appeared)
# cnts = sorted(cdict, key=cdict.get) #Sort RFVs by frequency
# li = cnts[:400] #Get 670 least frequently occuring variables
dataset = ds.copy()
# dataset = dataset.replace(li, 'Other') #Replace them with "Other"
# dataset = pd.get_dummies(dataset, columns=['RFV1', 'RFV2', 'RFV3']) #Turn into buckets (one-hot encoding)
# # At this point, the one-hot encoding includes the column name. There are 3 RFV columns – this means that, for example,
# # "RFV1_Chest pain" and "RFV2_Chest pain" are considered as two different variables.
# for x in cnts[400:]:
#     if 'nan' in x.lower():
#         continue
#     if 'RFV1_'+x in dataset: #The if-else abuse is because some RFVs don't appear in every RFV column.
#         if 'RFV2_'+x in dataset and 'RFV3_'+x in dataset: #This is probably the worst way to do this... but it works
#             #New column "Chest pain" = "RFV1_Chest pain" + "RFV2_Chest pain" + "RFV3_Chest pain"
#             dataset[x] = dataset['RFV1_'+x] + dataset['RFV2_'+x] + dataset['RFV3_'+x]
#         elif 'RFV2_'+x in dataset and 'RFV3_'+x not in dataset:
#             dataset[x] = dataset['RFV1_'+x] + dataset['RFV2_'+x]
#         elif 'RFV2_'+x not in dataset and 'RFV3_'+x in dataset:
#             dataset[x] = dataset['RFV1_'+x] + dataset['RFV3_'+x]
#         else:
#             dataset[x] = dataset['RFV1_'+x]
#     elif 'RFV2_'+x in dataset:
#         if 'RFV3_'+x in dataset:
#             dataset[x] = dataset['RFV2_'+x] + dataset['RFV3_'+x]
#         else:
#             dataset[x] = dataset['RFV2_'+x]
#     else:
#         dataset[x] = dataset['RFV3_'+x]

for x in dataset:
    if 'RFV' in x:
        del dataset[x] #Remove the old RFV columns

for c in ['LWBS', 'LEFTAMA', 'DOA']:
    del dataset[c]

hospital_predictions = dataset[["ADMIT", "IMMEDR"]]
dataset = dataset[[x for x in dataset if x not in ["ADMIT", "IMMEDR"] and "Unnamed" not in x]+['ADMIT']] #Move "ADMIT" to the last column for convenience
dataset.to_csv("datasets/dataset.csv")
hospital_predictions.to_csv("datasets/hospital_predictions.csv")