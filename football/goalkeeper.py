import pandas as pd
import numpy as np

from football import main

def getMinutesPerConceded(row: pd.Series) -> pd.Series:
  if row["goals_conceded"] == 0:
    return np.nan
  return row['minutes'] / row['goals_conceded']


def affordable_gks_for_year(year: int) -> pd.DataFrame:
  gks = main.player_type_for_year(year, player_type="GK")
  played_gks = gks.loc[gks['minutes'] != 0]

  played_gks[year] = played_gks.apply(getMinutesPerConceded, axis=1)
  played_gks.dropna(subset=[year], inplace=True)
  best_gks = played_gks.sort_values(by=year, ascending=False)
  return best_gks[['first_name', 'second_name', year]]


def expected_vs_actual_goals_conceded(player: pd.Series) -> pd.Series:
  expected_vs_actual_goals_conceded = np.nan
  player_gw = main.find_player_gw_this_year(player["first_name"], player["second_name"])
  for i in range(len(player_gw)):
    match = player_gw.iloc[-i]
    if match['minutes'] != 0:
      expected_vs_actual_goals_conceded = match['expected_goals_conceded'] - match['goals_conceded']
      break
  player["overperformed_goals"] = expected_vs_actual_goals_conceded
  return player


def saves_goals_conceded(player: pd.Series) -> pd.Series:
  saves_vs_goals_conceded = np.nan
  player_gw = main.find_player_gw_this_year(player["first_name"], player["second_name"])
  for i in range(len(player_gw)):
    match = player_gw.iloc[-i]
    if match['minutes'] != 0:
      saves_vs_goals_conceded = match['saves'] - match['goals_conceded']
      break
  player["overperformed_saves"] = saves_vs_goals_conceded
  return player
