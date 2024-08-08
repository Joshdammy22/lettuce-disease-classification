import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image


# Load the models
model_phase_one = load_model(r'C:\Users\Other\Desktop\Enhancing Lettuce Crop Managemen\lettuce_crop_management\model_checkpoint_47-0.94.keras')
model_phase_two = load_model(r'C:\Users\Other\Desktop\Enhancing Lettuce Crop Managemen\lettuce_crop_management\best_modelMobileNetV2.keras')



def classify_health(image_path):
    """
    Classify the health of the lettuce plant.
    
    Args:
        image_path (str): Path to the image to be classified.
        
    Returns:
        tuple: (health_status, confidence_score)
    """
    # Load the image as grayscale and resize to expected input shape of the model
    img = load_img(image_path, color_mode='grayscale', target_size=(200, 200))  # Ensure correct target size
    image_array = img_to_array(img)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    image_array = image_array / 255.0  # Normalize the image to [0, 1]

    # Make predictions
    prediction = model_phase_one.predict(image_array)
    
    # Debugging: print the raw prediction
    print(f"Raw prediction: {prediction}")

    confidence_score = prediction[0][0]  # Confidence score for healthy class
    
    # Debugging: print the confidence score
    print(f"Confidence score: {confidence_score}")

    if confidence_score > 0.5:
        return 'Healthy', confidence_score
    else:
        return 'Diseased', confidence_score



def classify_disease(image_path):
    """
    Classify the disease of the lettuce plant and provide confidence score.
    
    Args:
        image_path (str): Path to the image to be classified.
        
    Returns:
        tuple: (disease_name, confidence_score)
    """
    # Load the image and prepare it for the model
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(200, 200))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Make prediction
    predictions = model_phase_two.predict(image_array)
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
