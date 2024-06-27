from sklearn.preprocessing import Imputer

imp = Imputer(missing_values=0, strategy='mean', axis=0)
imp.fit_transform(X_train)