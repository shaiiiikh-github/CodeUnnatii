import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model_leaf_disease.h5')

print(f"Input shape: {model.input_shape}")
print(f"Output classes: {model.output_shape[-1]}")

# Check if model has class names saved
if hasattr(model, 'class_names'):
    print("Class names from model:")
    for i, name in enumerate(model.class_names):
        print(f"  {i}: {name}")
else:
    print("No class_names attribute found in model")
    print("Checking model config...")
    try:
        config = model.get_config()
        print(config.get('class_names', 'Not found in config'))
    except:
        print("Not found in config either")