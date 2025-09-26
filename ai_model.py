import tensorflow as tf
import numpy as np
from PIL import Image
import io

model = None
class_names = ['Apple', 'Banana', 'Carrot', 'Coconut']

def load_model():
    """Charge le modèle TensorFlow"""
    global model
    try:
        #ICI CA SERT A UTILISER LE MODÈLE OPTIMISÉ AVEC WEIGHTS & BIASES
        model = tf.keras.models.load_model("model_best.keras")
        return True
    except Exception as e:
        return False

def preprocess_image(image_bytes):
    #ICI CA SERT A PRÉPROCESSE L'IMAGE POUR LE MODÈLE
    try:
        # Convertir bytes en image PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionner à 180x180 (taille du modèle)
        image = image.resize((180, 180))
        
        # Convertir en array numpy
        img_array = np.array(image)
        
        # Normaliser (diviser par 255)
        img_array = img_array.astype(np.float32) / 255.0
        
        # Ajouter dimension batch
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        return None

def detect_fruit(image_bytes):
    #ICI CA SERT A DÉTECTER LE FRUIT DANS L'IMAGE
    global model
    
    # Si le modèle n'est pas chargé, essayer de le charger
    if model is None:
        if not load_model():
            return {
                "object": "Erreur",
                "confidence": 0.0,
                "status": "Modèle non disponible"
            }
    
    try:
        # Préprocesser l'image
        processed_image = preprocess_image(image_bytes)
        if processed_image is None:
            return {
                "object": "Erreur",
                "confidence": 0.0,
                "status": "Erreur de préprocessing"
            }
        
        # Faire la prédiction
        predictions = model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Mapper les classes (car modèle utilise l'anglais)
        class_mapping = {
            'Apple': 'Pomme',
            'Banana': 'Banane', 
            'Carrot': 'Carotte',
            'Coconut': 'Coco'
        }
        
        predicted_class = class_names[predicted_class_idx]
        french_name = class_mapping.get(predicted_class, predicted_class)
        
        return {
            "object": french_name,
            "confidence": confidence,
            "status": "Détecté avec succès"
        }
        
    except Exception as e:
        return {
            "object": "Erreur",
            "confidence": 0.0,
            "status": f"Erreur de prédiction: {str(e)}"
        }

# Charger le modèle au démarrage
load_model()