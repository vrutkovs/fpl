import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

from football import main


def build_test_data_from_series(player: pd.Series) -> ([], [], [], []):
  X_train = []
  y_train = []
  for x in range(main.start_year, main.current_year):
    # Skip nans
    if np.isnan(player[x]):
      continue
    X_train.append([x])
    y_train.append(player[x])

  X_test = X_train + [[main.current_year]]
  y_test = y_train + [player[main.current_year]]
  return (X_train, y_train, X_test, y_test)

def predict_this_year_linear(player: pd.Series) -> pd.Series:
  X_train, y_train, X_test, y_test = build_test_data_from_series(player)
  model = LinearRegression()
  model.fit(X_train, y_train)
  player["prediction_linear"] = model.predict([[main.current_year]])[0]
  player["prediction_linear_score"] = model.score(X_test, y_test)
  return player

def predict_this_year_svr(player: pd.Series) -> pd.Series:
  X_train, y_train, X_test, y_test = build_test_data_from_series(player)
  model = SVR(kernel='rbf')
  model.fit(X_train, y_train)
  player["prediction_svr"] = model.predict([[main.current_year]])[0]
  player["prediction_svr_score"] = model.score(X_test, y_test)
  return player
