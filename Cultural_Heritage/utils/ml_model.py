import tensorflow as tf
from tensorflow.keras import layers, models
import os

# Paths
BASE_DIR = "data/Dance_Forms"
TRAIN_DIR = os.path.join(BASE_DIR, "Train")
MODEL_PATH = os.path.join(BASE_DIR, "dance_model.h5")

# Image Parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# Load dataset directly from folder structure
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.2,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Get class names
class_names = train_ds.class_names
print(f"Detected classes: {class_names}")

# Prefetch for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# Define model
model = models.Sequential([
    layers.Rescaling(1./255, input_shape=(224, 224, 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Train model
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10
)

# Save model
model.save(MODEL_PATH)
print("✅ Model trained and saved successfully!")
