import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

ds = pd.read_csv("datasets/icu.csv")
rem = [] #to remove
dataset = ds[[x for x in ds if "Unnamed" not in x and x not in rem]]

X = dataset[[x for x in dataset if x!="ADMIT"]].values
y = dataset.iloc[:, -1].values #Dependent variable (to be predicted): "ADMIT" column

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scaling didn't seem to do so well
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

param_grid = [{
    "early_stopping": [True],
    "hidden_layer_sizes": [(64, 32, 10), (128, 64, 32, 10), (512, 128, 64, 10), (512, 128, 64, 32, 10)],
    "solver": ["adam"],
    "learning_rate_init": [0.001, 0.005, 0.01],
    "max_iter": [200, 500, 1000],
}]

grid = GridSearchCV(estimator=MLPClassifier(), param_grid=param_grid, n_jobs=-1, cv=5)
grid_result = grid.fit(X_train, y_train)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

model = grid_result.best_estimator_

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc}")

# Retrain on entire dataset for production version
model.fit(X, y)
joblib.dump(model, 'model.pkl')
