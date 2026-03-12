import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model_leaf_disease.h5')

# Your current CLASS_NAMES (50 entries)
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust',
    'Apple___healthy', 'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy', 'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy',
    'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy', 'Tomato_healthy'
]

print(f"Model outputs: {model.output_shape[-1]} classes")
print(f"CLASS_NAMES has: {len(CLASS_NAMES)} entries")
print(f"Match: {'✅ YES' if model.output_shape[-1] == len(CLASS_NAMES) else '❌ NO'}")
print()

# Search for dataset folder
import os
search_dirs = [
    r"C:\Users\SHABBIR\Documents\CU\SmartAgro",
    r"C:\Users\SHABBIR\Documents\CU",
    r"C:\Users\SHABBIR\Documents",
    r"C:\Users\SHABBIR\Desktop",
]

print("🔍 Searching for dataset folders...")
for search_dir in search_dirs:
    if not os.path.exists(search_dir):
        continue
    for root, dirs, files in os.walk(search_dir):
        if 'Apple___Apple_scab' in dirs or 'Apple___healthy' in dirs:
            print(f"\n✅ FOUND DATASET AT: {root}")
            folders = sorted([d for d in dirs])
            print(f"📊 Total folders: {len(folders)}")
            print(f"\nCorrect CLASS_NAMES = [")
            for i, name in enumerate(folders):
                print(f"    '{name}',  # {i}")
            print(f"]")
            exit()

print("\n❌ Dataset folder not found on common paths")
print("Please tell me where your training dataset is located!")