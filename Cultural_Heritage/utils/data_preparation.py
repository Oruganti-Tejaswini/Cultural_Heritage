import tensorflow as tf
import pandas as pd
import os
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = "data/Dance_Forms"
IMAGE_DIR = os.path.join(BASE_DIR, "Train")
LABEL_FILE = os.path.join(BASE_DIR, "train.csv")

# Load labels from excel
df = pd.read_csv(LABEL_FILE)

# Create absolute image paths
df['filepath'] = df['Image Name'].apply(lambda x: os.path.join(IMAGE_DIR, x))

# Filter out missing images if any
df = df[df['filepath'].apply(os.path.exists)]

# Encode labels
le = LabelEncoder()
df['label_enc'] = le.fit_transform(df['Label'])

# Split train/val
train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['label_enc'], random_state=42)
num_classes = len(le.classes_)
