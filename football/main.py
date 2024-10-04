import pandas as pd
import numpy as np

start_year = 2020
current_year = 2024

def player_type_for_year(year: int, player_type: str) -> pd.DataFrame:
  folderlabel = foldername_from_year(year)
  df = pd.read_csv(f"data/{folderlabel}/cleaned_players.csv", encoding = "iso-8859-1")
  return df[df["element_type"]==player_type]

def foldername_from_year(year: int) -> str:
  next_year = year + 1 - 2000
  return f"{year}-{next_year}"

def year_from_foldername(foldername: str) -> int:
  return int(foldername.split("-")[0])

# Drop players unavailable for this round
current_year_folderlabel = foldername_from_year(current_year)
raw_players = pd.read_csv(f"data/{current_year_folderlabel}/players_raw.csv", encoding = "iso-8859-1")


# Drop players unavailable for this round

def chance_of_playing_this_round(player: pd.Series) -> int:
  found_players = raw_players[
    (raw_players["first_name"]==player["first_name"]) & 
    (raw_players["second_name"]==player["second_name"])
  ]
  if found_players.empty:
    player["chance_to_play"] = 0
    return player
    result
  first_row = found_players.fillna(100).iloc[0]["chance_of_playing_this_round"]
  player["chance_to_play"] = first_row.astype(int)
  return player

def get_player_id(first_name: str, second_name: str) -> int:
  found_players = raw_players[
    (raw_players["first_name"]==first_name) & 
    (raw_players["second_name"]==second_name)
  ]
  if found_players.empty:
    return 0
  first_row = found_players.fillna(100).iloc[0]["id"]
  return first_row.astype(int)

def find_player_gw_this_year(first_name: str, second_name: str) -> pd.DataFrame:
  player_id = get_player_id(first_name, second_name)
  path = f"data/{current_year_folderlabel}/players/{first_name}_{second_name}_{player_id}/gw.csv"
  try:
    return pd.read_csv(path, encoding = "iso-8859-1")
  except:
    # TODO: handle unicode errors
    return pd.DataFrame()
