import pandas as pd
import numpy as np

from football import main

def get_minutes_per_scored(row: pd.Series) -> pd.Series:
  if row["goals_scored"] == 0:
    return np.nan
  return row['minutes'] / row['goals_scored']


def affordable_fwds_for_year(year: int) -> pd.DataFrame:
  fwds = main.player_type_for_year(year, player_type="FWD")
  played_fwds = fwds.loc[fwds['minutes'] != 0]

  played_fwds[year] = played_fwds.apply(get_minutes_per_scored, axis=1)
  played_fwds.dropna(subset=[year], inplace=True)
  best_fwds = played_fwds.sort_values(by=year, ascending=False)
  return best_fwds[['first_name', 'second_name', year]]


def expected_vs_actual_goals_scored(player: pd.Series) -> pd.Series:
  expected_vs_actual_goals_conceded = np.nan
  player_gw = main.find_player_gw_this_year(player["first_name"], player["second_name"])
  for i in range(len(player_gw)):
    match = player_gw.iloc[-i]
    if match['minutes'] != 0:
      expected_vs_actual_goals_conceded = match['expected_goals'] - match['goals_scored']
      break
  player["overperformed_goals"] = expected_vs_actual_goals_conceded
  return player

def get_assists_per_minute(row: pd.Series) -> pd.Series:
  return row['assists'] / row['minutes']

def affordable_assisting_fwds_for_year(year: int) -> pd.DataFrame:
  fwds = main.player_type_for_year(year, player_type="FWD")
  played_fwds = fwds.loc[fwds['minutes'] != 0]

  played_fwds[year] = played_fwds.apply(get_assists_per_minute, axis=1)
  played_fwds.dropna(subset=[year], inplace=True)
  best_fwds = played_fwds.sort_values(by=year, ascending=False)
  return best_fwds[['first_name', 'second_name', year]]

def get_influence_per_minute(row: pd.Series) -> pd.Series:
  return row['influence'] / row['minutes']

def affordable_influence_fwds_for_year(year: int) -> pd.DataFrame:
  fwds = main.player_type_for_year(year, player_type="FWD")
  played_fwds = fwds.loc[fwds['minutes'] != 0]

  played_fwds[year] = played_fwds.apply(get_influence_per_minute, axis=1)
  played_fwds.dropna(subset=[year], inplace=True)
  best_fwds = played_fwds.sort_values(by=year, ascending=False)
  return best_fwds[['first_name', 'second_name', year]]
