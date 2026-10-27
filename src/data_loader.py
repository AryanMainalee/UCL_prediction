import pandas as pd
import os

def load_team_details(filepath:str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        print(f"File not found in {filepath}.")

    df = pd.read_csv(filepath)
    
    required_columns = [
        "club_id",
        "club_code",
        "name",
        "domestic_competition_id",
    ]
    col_to_use = [cols for cols in required_columns if cols in df.columns]
    df_cleaned = df[col_to_use].copy()
    
    #throwing an error if column doesn't exist to prevent missing column later
    missing_columns = [
    col for col in required_columns
    if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing Column(s): {missing_columns}.")
    

    if "club_id" in col_to_use:
        df_cleaned['club_id'] = pd.to_numeric(df['club_id'], errors="coerce").fillna(-1)
        df_cleaned = df_cleaned[df_cleaned['club_id'] >= 0]
        df_cleaned['club_id'] = df_cleaned['club_id'].astype(int)
        
    for col in ["club_code", "name", "domestic_competition_id"]:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].str.strip()
            df_cleaned[col] = df_cleaned[col].astype(str)
    
    if "name" in df_cleaned.columns:
        df_cleaned["name"] = df_cleaned["name"].str.lower()
    
    return df_cleaned.reset_index(drop=True)


