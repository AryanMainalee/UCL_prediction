import pandas as pd
import os

output_path = r"C:\Datascience\UCL_prediction\data\processed"

def load_team_details(filepath:str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f"No file in {filepath}.")
                
    df = pd.read_csv(filepath)
    
    required_columns = [
        "club_id",
        "club_code",
        "name",
        "domestic_competition_id",
    ]
    
    #throwing an error if column doesn't exist to prevent missing column later
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing Column(s): {missing_columns}.")
        
    df_cleaned = df[required_columns].copy()

    df_cleaned['club_id'] = pd.to_numeric(df['club_id'], errors="coerce").fillna(-1)
    before = len(df)
    df_cleaned = df_cleaned[df_cleaned['club_id'] >= 0]
    df_cleaned['club_id'] = df_cleaned['club_id'].astype(int)
    print(f"Dropped {before - len(df_cleaned)} rows with invalid club IDs.")
        
        
    for col in ["club_code", "name", "domestic_competition_id"]:
        df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)
        
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].str.strip()
            df_cleaned[col] = df_cleaned[col].astype(str)
    
    #removing duplicate clubs
    dupes = df["club_id"].duplicated().sum()
    if dupes:
        print(f"Dropping {dupes} duplicate club_id rows")
        df = df.drop_duplicates(subset="club_id", keep="first")

    
    if "name" in df_cleaned.columns:
        df_cleaned["cleaned_name"] = df_cleaned["name"].str.lower()
        
        
    df_cleaned = df_cleaned.sort_values(by="club_id", ascending=True)
    
    
    
    return df_cleaned.reset_index(drop=True)


def load_game_details(filepath:str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError(f"No file in {filepath}.")
    
    df = pd.read_csv(filepath)
    
    required_columns = [
        "game_id", "competition_id", "season", "date", 
        "home_club_id", "away_club_id", 
        "home_club_goals", "away_club_goals"
    ]
        
    #throwing an error if column doesn't exist to prevent missing column later
    missing_columns = [
    col for col in required_columns
    if col not in df.columns
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing Column(s): {missing_columns}.")
    
    df_cleaned = df[required_columns].copy()
    
    #removing invalid rows
    before = len(df)
    id_columns = ["game_id","home_club_id", "away_club_id"] 
    goal_columns = ["home_club_goals", "away_club_goals"]
    
    for cols in id_columns + goal_columns:
        df_cleaned[cols] = pd.to_numeric(df[cols], errors="coerce")
    
    for cols in id_columns:
        df_cleaned = df_cleaned[df_cleaned[cols] > 0]
    for cols in goal_columns:
        df_cleaned = df_cleaned[df_cleaned[cols] >= 0]
    
    df_cleaned = df_cleaned[id_columns + goal_columns].astype(int)
        
    print(f"Dropped {before - len(df_cleaned)} rows with invalid Game ID, club ID or goals")
    
    df_cleaned["competition_id"] = df["competition_id"].str.strip().str.lower()
    
    df_cleaned["season"] = pd.to_numeric(df["season"], errors="coerce")
    
    df_cleaned["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    
    #removing duplicate rows
    dupes = df_cleaned["game_id"].duplicated().sum()
    if dupes:
        df_cleaned.drop_duplicates(subset="game_id", keep="first")
        print(f"Dropped {dupes} duplicate rows.")
    
    df_cleaned = df_cleaned.sort_values(by="game_id", ascending=True)
    
    return df_cleaned.reset_index(drop= True)