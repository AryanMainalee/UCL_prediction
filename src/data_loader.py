import pandas as pd
import os

def load_team_details(filepath:str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        print(f"File not found in {filepath}.")

    df = pd.read_csv(filepath)
    
    #trimming team names before returning
    if 'team_name' in df.columns:
        df['team_name'] = df['team_name'].str.strip()
    if 'club_name' in df.columns:
        df['club_name'] = df['club_name'].str.strip()
        
    return df
