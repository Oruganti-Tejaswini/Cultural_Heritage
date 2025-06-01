import os

# Root directory where AR model images are stored
AR_DATA_PATH = "data/AR_Models"

# Ensure root directory exists
os.makedirs(AR_DATA_PATH, exist_ok=True)


# Create or get state and place folders dynamically
def ensure_folder(state, place=None):
    state_path = os.path.join(AR_DATA_PATH, state)
    os.makedirs(state_path, exist_ok=True)

    if place:
        place_path = os.path.join(state_path, place)
        os.makedirs(place_path, exist_ok=True)
        return place_path
    else:
        return state_path


# List existing states
def list_states():
    return sorted([
        d for d in os.listdir(AR_DATA_PATH)
        if os.path.isdir(os.path.join(AR_DATA_PATH, d)) and not d.startswith('.')
    ])


# List places under selected state
def list_places(state):
    state_path = os.path.join(AR_DATA_PATH, state)
    if not os.path.exists(state_path):
        return []
    return sorted([
        d for d in os.listdir(state_path)
        if os.path.isdir(os.path.join(state_path, d)) and not d.startswith('.')
    ])


# Upload image files into correct state/place
def save_uploaded_images(state, place, files):
    place_path = ensure_folder(state, place)
    for file in files:
        file_path = os.path.join(place_path, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())


# List images under state/place
def list_images(state, place=None):
    images = []
    if place:
        folder_path = os.path.join(AR_DATA_PATH, state, place)
        if os.path.exists(folder_path):
            images = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if not f.startswith('.') and f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]
    else:
        state_path = os.path.join(AR_DATA_PATH, state)
        for place_folder in list_places(state):
            folder_path = os.path.join(state_path, place_folder)
            images += [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if not f.startswith('.') and f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]
    return images
