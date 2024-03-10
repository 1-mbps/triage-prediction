import pandas as pd

# Data taken from https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/spss/
keep = ['AGE', 'SEX', 'ARREMS', 'TEMPF', 'PULSE', 'RESPR', 'BPSYS', 'BPDIAS',
       'POPCT', 'CEBVD', 'CHF', 'EDHIV', 'NOCHRON',"ADMIT", "IMMEDR", "DOA", "DIEDED", "LEFTAMA", "RFV1", "RFV2", "RFV3"]

keep2012 = keep+['DIABETES', 'EDDIAL', 'MIHX', 'DEMENTIA', 'LEFTBTRI']
keep2013 = keep+['DIABETES', 'EDDIAL', 'MIHX', 'DEMENTIA', 'LWBS']
keep2014 = keep+['DIABTYP1', 'DIABTYP2', 'DIABTYP0', 'ESRD', 'ALZHD', 'CAD', 'LWBS']

datasets = []
for x in range(2012,2022): #Loop through all the datasets from 2012-2019
    print(f"Doing: {x}")
    filename = f"datasets/ed{x}-spss.sav"
    if x == 2012:
        df = pd.read_spss(filename, usecols=keep2012)
        df = df.rename(columns={'DEMENTIA': 'ALZHD', 'MIHX': 'CAD', 'LEFTBTRI':'LWBS'})
    elif x == 2013:
        df = pd.read_spss(filename, usecols=keep2013) #Remove all the columns not in the list "keep"
        df = df.rename(columns={'DEMENTIA': 'ALZHD', 'MIHX': 'CAD'})
    else:
        df = pd.read_spss(filename, usecols=keep2014) #Remove all the columns not in the list "keep"
        df = df.rename(columns={'ESRD': 'EDDIAL'})
        df = df.assign(DIABETES=[0 for x in range(len(df))])
    for index, row in df.iterrows():
        if x > 2013 and (row['DIABTYP0'] == 'Yes' or row['DIABTYP1'] == 'Yes' or row['DIABTYP2'] == 'Yes'):
            df.loc[index, 'DIABETES'] = 1
        if row['DIEDED'] == 'Yes':
            df.loc[index, 'ADMIT'] = 'Critical care unit'
    delete = ['DIABTYP0','DIABTYP1','DIABTYP2','DIEDED']
    for c in delete:
        if c in df:
            del df[c]
    datasets.append(df)
    
d = pd.concat(datasets, axis=0, ignore_index=True)
d.to_csv("datasets/dataset_unclean.csv")