import urllib.request
import os

MODELS = [
    "ssd_mobilenetv1_model-weights_manifest.json",
    "ssd_mobilenetv1_model-shard1",
    "ssd_mobilenetv1_model-shard2",
    "face_landmark_68_model-weights_manifest.json",
    "face_landmark_68_model-shard1",
    "face_recognition_model-weights_manifest.json",
    "face_recognition_model-shard1",
    "face_recognition_model-shard2"
]

BASE_URL = "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/"
DIR = "c:/Projects/online-exam/frontend/public/models"

os.makedirs(DIR, exist_ok=True)

for model in MODELS:
    url = BASE_URL + model
    path = os.path.join(DIR, model)
    print(f"Downloading {model}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(f"Saved to {path}")
    except Exception as e:
        print(f"Failed to download {model}: {e}")

print("Done!")
