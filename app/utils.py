import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image

import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use relative paths for loading the models
model_phase_one = load_model(os.path.join(BASE_DIR, '..', 'first-classification_mobilenetv2-functional-model.keras'))
model_phase_two = load_model(os.path.join(BASE_DIR, '..', 'second-classification-mobilenetv2-model.keras'))


def load_and_preprocess_image(img_path):
    """
    Load and preprocess the image for model prediction.
    
    Args:
        img_path (str): Path to the image file.
        
    Returns:
        np.ndarray: Preprocessed image array.
    """
    img = Image.open(img_path).resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def classify_health(image_path):
    img_array = load_and_preprocess_image(image_path)
    prediction = model_phase_one.predict(img_array)
    confidence_score = prediction[0][0]
    
    # Debugging output
    print(f"Raw prediction: {prediction}")
    print(f"Confidence score: {confidence_score}")

    if confidence_score < 0.5:
        return 'Healthy', confidence_score
    else:
        return 'Diseased', confidence_score

def classify_disease(image_path):
    """
    Classify the disease of the lettuce plant using phase two model.
    
    Args:
        image_path (str): Path to the image to be classified.
        
    Returns:
        tuple: (disease_name, confidence_score)
    """
    img_array = load_and_preprocess_image(image_path)
    
    # Make predictions
    predictions = model_phase_two.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions)  # Confidence score of the predicted class

    # Map the predicted index to the disease name
    class_labels = ["Wilt_and_leaf_blight_on_lettuce", "Septoria_Blight_on_lettuce", 
                    "Powdery_mildew_on_lettuce", "Downy_mildew_on_lettuce"]
    disease_name = class_labels[predicted_class_index]
    
    return disease_name, confidence_score

def get_disease_info(disease_name):
    """
    Retrieve disease information based on the disease name.
    
    Args:
        disease_name (str): Name of the disease.
        
    Returns:
        dict: Disease details including description, causes, solutions, and recommendations.
    """
    disease_details = {
        "Wilt_and_leaf_blight_on_lettuce": {
            'description': 'Description for Wilt and leaf blight',
            'causes': 'Causes for Wilt and leaf blight',
            'solutions': 'Solutions for Wilt and leaf blight',
            'recommendations': 'Recommendations for Wilt and leaf blight'
        },
        "Septoria_Blight_on_lettuce": {
            'description': 'Description for Septoria Blight',
            'causes': 'Causes for Septoria Blight',
            'solutions': 'Solutions for Septoria Blight',
            'recommendations': 'Recommendations for Septoria Blight'
        },
        "Powdery_mildew_on_lettuce": {
            'description': 'Description for Powdery mildew',
            'causes': 'Causes for Powdery mildew',
            'solutions': 'Solutions for Powdery mildew',
            'recommendations': 'Recommendations for Powdery mildew'
        },
        "Downy_mildew_on_lettuce": {
            'description': 'Description for Downy mildew',
            'causes': 'Causes for Downy mildew',
            'solutions': 'Solutions for Downy mildew',
            'recommendations': 'Recommendations for Downy mildew'
        }
    }

    return disease_details.get(disease_name, {
        'description': 'No information available',
        'causes': 'No information available',
        'solutions': 'No information available',
        'recommendations': 'No information available'
    })
