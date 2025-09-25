import mysql.connector

def get_user_credits(cursor, username):
    #ICI CA SERT A RÉCUPÉRER LES CREDITS DE L'UTILISATEUR
    try:
        cursor.execute("SELECT credits FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result[0] or 0
        return 0
    except Exception as e:
        print(f"Erreur lors de la récupération des crédits: {e}")
        return 0

def add_credits(db, cursor, username, fruit_detected):
    #ICI CA SERT A AJOUTER DES CREDITS BASÉS SUR LE FRUIT DETECTÉ
    
    credit_values = {
        'Pomme': 2,
        'Banane': 1,
        'Carotte': 3,
        'Tomate': 2,
        'Coco': 5,
        'Pomme de terre': 1
    }
    
    try:
        credits_to_add = credit_values.get(fruit_detected, 1)
        current_credits = get_user_credits(cursor, username)
        new_credits = current_credits + credits_to_add
        
        #ICI CA SERT A METTRE À JOUR LES CREDITS DANS LA BASE DE DONNÉES
        cursor.execute("UPDATE users SET credits = %s WHERE username = %s", (new_credits, username))
        db.commit()
        
        return {
            "credits_added": credits_to_add,
            "total_credits": new_credits,
            "fruit": fruit_detected
        }
    except Exception as e:
        print(f"Erreur lors de l'ajout des crédits: {e}")
        return None