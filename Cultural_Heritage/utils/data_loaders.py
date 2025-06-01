import pandas as pd
import os

DATA_PATH = "data/"

# Clean column names function
def clean_columns(df):
    df.columns = df.columns.str.strip().str.title()
    return df

def load_places():
    file_path = os.path.join(DATA_PATH, "Top_Indian_Places_to_Visit.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError("The places data file is missing!")
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.title().str.replace(" ", "_")
    return df

def load_login_data():
    file_path = os.path.join(DATA_PATH, "login_details.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['Email'] = df['Email'].astype(str)
        df['DOB'] = df['DOB'].astype(str)
    else:
        df = pd.DataFrame(columns=["Email", "DOB"])
    return df

def save_login_data(df):
    file_path = os.path.join(DATA_PATH, "login_details.csv")
    df.to_csv(file_path, index=False)

# Load Monuments
def load_monuments():
    df = pd.read_excel(os.path.join(DATA_PATH, 'site_coordinates.xlsx'))
    df = clean_columns(df)
    df.fillna("Unknown", inplace=True)
    return df

# Load Tourist Stats

def load_tourist_stats():
    df = pd.read_csv(DATA_PATH + "tourist_stats.csv")
    df.columns = df.columns.str.strip()
    state_columns = [col for col in df.columns if col not in ['Year', 'Type', 'Total']]

    df_melted = df.melt(id_vars=["Year", "Type"],
                        value_vars=state_columns,
                        var_name="State",
                        value_name="Tourist_Count")

    df_melted['Year'] = df_melted['Year'].astype(int)
    df_melted['Tourist_Count'] = df_melted['Tourist_Count'].astype(int)

    return df_melted


# Load Unified Feedback
def load_feedback():
    df = pd.read_csv(os.path.join(DATA_PATH, 'user_feedback.csv'))
    df.columns = df.columns.str.strip().str.title()
    return df


