import pandas as pd
from imblearn.under_sampling import RandomUnderSampler

df = pd.read_csv("datasets/dataset.csv")

df['ADMIT'] = df['ADMIT'].apply(lambda x: 1 if x == 'Critical care unit' else 0)

# Specify the column you want to undersample
# Replace 'target_column' with the actual name of the column you want to undersample
X = df.drop('ADMIT', axis=1)
y = df['ADMIT']

# Initialize the RandomUnderSampler
rus = RandomUnderSampler(sampling_strategy='majority', random_state=42)

# Perform the undersampling
X_resampled, y_resampled = rus.fit_resample(X, y)

# Display the value counts after undersampling
print("Value counts after undersampling:")
print(y_resampled.value_counts())

df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='ADMIT')], axis=1)

df_resampled.to_csv("datasets/icu.csv")
