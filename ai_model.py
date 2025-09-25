import random

def detect_fruit(image_bytes):

    fruits = ['Pomme', 'Banane', 'Carotte', 'Tomate', 'Coco', 'Pomme de terre']
    
    # Simulation d'analyse (à remplacer par modèle IA)
    detected_fruit = random.choice(fruits)
    confidence = round(random.uniform(0.7, 0.99), 2)
    
    return {
        "object": detected_fruit,
        "confidence": confidence,
        "status": "Détecté avec succès"
    }