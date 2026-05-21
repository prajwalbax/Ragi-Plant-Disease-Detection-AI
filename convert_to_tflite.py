import tensorflow as tf

MODEL_DIR = r"C:\Users\praj\OneDrive\Desktop\RagiMilletCompleteDeployment\backend\my_model"

converter = tf.lite.TFLiteConverter.from_saved_model(
    MODEL_DIR
)

converter.optimizations = [

    tf.lite.Optimize.DEFAULT

]

tflite_model = converter.convert()

with open(

    "model.tflite",

    "wb"

) as f:

    f.write(
        tflite_model
    )

print(
    "TFLite model created."
)