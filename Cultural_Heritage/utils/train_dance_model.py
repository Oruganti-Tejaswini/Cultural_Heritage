import pandas as pd
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

# Paths
DATA_DIR = "data/Dance_Forms/train"
LABEL_FILE = "data/Dance_Forms/train.csv"
MODEL_PATH = "models/dance_model.h5"

# Load label file
df = pd.read_csv(LABEL_FILE)

# Clean data
df = df.dropna()
df['Image'] = df['Image'].astype(str)
df['Label'] = df['target'].astype(str)

# Prepare train/test split
train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['Label'], random_state=42)

# Image Data Generator
datagen = ImageDataGenerator(rescale=1./255)

train_gen = datagen.flow_from_dataframe(
    train_df,
    directory=DATA_DIR,
    x_col="Image",
    y_col="target",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)

val_gen = datagen.flow_from_dataframe(
    val_df,
    directory=DATA_DIR,
    x_col="Image",
    y_col="Label",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical"
)

# Build CNN Model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(len(train_gen.class_indices), activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train model
history = model.fit(train_gen, validation_data=val_gen, epochs=10)

# Save model
os.makedirs("models", exist_ok=True)
model.save(MODEL_PATH)

# Save class mapping
label_map = train_gen.class_indices
inv_map = {v: k for k, v in label_map.items()}
pd.Series(inv_map).to_csv("models/dance_label_map.csv")

print("✅ Model trained and saved!")
