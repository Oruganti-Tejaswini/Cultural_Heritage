import pandas as pd
import os

DATA_PATH = "data/"

# Save New Monument
def save_monument(new_entry):
    file_path = os.path.join(DATA_PATH, 'site_coordinates.xlsx')
    df = pd.read_excel(file_path)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(file_path, index=False)

# Save Tourist Stats Entry
def save_tourist_stats(new_entry):
    file_path = os.path.join(DATA_PATH, 'tourist_stats.csv')
    df = pd.read_csv(file_path)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(file_path, index=False)

# Save Unified Feedback Entry
def save_feedback(new_entry):
    file_path = os.path.join(DATA_PATH, 'user_feedback.csv')
    df = pd.read_csv(file_path)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(file_path, index=False)

