# 🍎🥕 Workshop 2025 - Reconnaissance IA de Fruits & Légumes

## 🎯 Vue d'ensemble du projet

Ce projet utilise l'**Intelligence Artificielle** pour reconnaître automatiquement différents types de fruits et légumes à partir de photos. C'est un système de **classification d'images** qui apprend à distinguer les caractéristiques visuelles de chaque aliment.

**Technologies utilisées :** Python, TensorFlow, Keras, Flask, MySQL, Bcrypt

---

## 🚀 Installation et Configuration

### **1. Prérequis**
- Python 3.8+
- MySQL Server
- Jupyter Notebook (optionnel)

### **2. Installation des dépendances**
```bash
pip install tensorflow keras flask mysql-connector-python bcrypt
```

### **3. Configuration de la base de données**

#### **Création de la base de données**
```sql
-- Se connecter à MySQL
mysql -u root -p

-- Créer la base de données
CREATE DATABASE ia_project;

-- Utiliser la base
USE ia_project;

-- Créer la table utilisateurs
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

#### **Vérification**
```sql
-- Voir la structure de la table
DESCRIBE users;

-- Voir le contenu (vide au début)
SELECT * FROM users;
```

---

## 🧠 Partie IA - Entraînement du modèle

### **Structure du dataset**
```
dataset/
├── banane/          # 490 images de bananes
├── Carrot/          # 581 images de carottes  
├── Coconut/         # 500 images de noix de coco
├── pomme/           # 444 images de pommes
├── Potato/          # 78 images de pommes de terre
└── Tomato/          # 830 images de tomates
```

### **Commandes Jupyter Notebook**

#### **1. Imports et configuration**
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Configuration
IMG_SIZE = (64, 64)
BATCH_SIZE = 16
SEED = 123
```

#### **2. Chargement et préparation des données**
```python
# Charger le dataset
dataset_directory = "dataset"

# Créer les datasets d'entraînement et de validation
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_directory,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_directory,
    validation_split=0.2,
    subset="validation", 
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Nombre de classes (types de fruits/légumes)
num_classes = len(train_ds.class_names)
print(f"Nombre de classes: {num_classes}")
print(f"Classes: {train_ds.class_names}")
```

#### **3. Normalisation des pixels**
```python
# Normaliser les pixels de 0-255 à 0-1
train_ds = train_ds.map(lambda x, y: (x/255.0, y))
val_ds = val_ds.map(lambda x, y: (x/255.0, y))
```

**Explication :**
- **Pourquoi ?** Les images ont des pixels de 0 à 255 (niveaux de couleur)
- **Transformation :** On divise par 255 pour avoir des valeurs entre 0 et 1
- **Avantage :** Plus facile pour l'IA d'apprendre avec des nombres plus petits
- **lambda :** Fonction anonyme (sans nom) pour appliquer la transformation

#### **4. Construction du modèle CNN**
```python
model = Sequential([
    # Couche de convolution 1
    Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(2,2),
    
    # Couche de convolution 2  
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    
    # Couches de classification
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Voir l'architecture
model.summary()
```

**Explication des couches :**
- **Sequential :** Construction couche par couche
- **Conv2D(32, (3,3)) :** 32 filtres qui analysent des blocs 3x3 pixels
- **MaxPooling2D :** Réduit la taille en gardant l'essentiel
- **Flatten :** Transforme la matrice 2D en vecteur 1D
- **Dense(128) :** 128 neurones pour les connexions
- **Dropout(0.5) :** Désactive 50% des connexions (évite le sur-apprentissage)
- **Dense(num_classes) :** Une sortie par type de fruit/légume

#### **5. Compilation et entraînement**
```python
# Compiler le modèle
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entraîner le modèle
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
    verbose=1
)

# Sauvegarder le modèle
model.save('model1.keras')
```

#### **6. Test de prédiction**
```python
def predict_image(img_path):
    # Charger et redimensionner l'image
    img = image.load_img(img_path, target_size=(64,64))
    
    # Convertir en tableau de nombres
    x = image.img_to_array(img)
    
    # Ajouter une dimension pour le batch
    x = np.expand_dims(x, axis=0)
    
    # Normaliser
    x = x / 255.0
    
    # Prédire
    preds = model.predict(x)
    class_idx = np.argmax(preds)
    
    # Récupérer le nom de la classe
    class_names = train_ds.class_names
    fruit_name = class_names[class_idx]
    
    print(f"C'est probablement une/un {fruit_name}")
    print(f"Confiance: {preds[0][class_idx]*100:.1f}%")
```

---

## 🌐 Application Web Flask

### **Lancement de l'application**
```bash
python app.py
```
L'application sera accessible sur `http://localhost:5000`

### **Structure de l'application**
```
Workshop2025/
├── app.py                    # Application Flask principale
├── model1.keras             # Modèle IA entraîné
├── login/                   # Pages de connexion
├── register/                # Pages d'inscription  
├── homepage/                # Page d'accueil
├── dataset/                 # Images d'entraînement
└── validation/              # Images de test
```

---

## 🔐 Sécurité - Hashage et Salage des Mots de Passe

### **Pourquoi crypter les mots de passe ?**

**❌ Dangereux (sans cryptage) :**
```sql
-- Mot de passe visible en clair dans la base
INSERT INTO users (username, password) VALUES ('alice', 'secret123');
```

**✅ Sécurisé (avec bcrypt) :**
```sql
-- Mot de passe crypté (impossible à lire)
INSERT INTO users (username, password) VALUES ('alice', '$2b$12$LQv3c1yqBWVHxkd0LHAkC...');
```

### **Qu'est-ce que le "salage" (salt) ?**

Le **salt** est un **assaisonnement unique** ajouté à chaque mot de passe :
- Même mot de passe + salt différent = hash complètement différent
- Empêche les attaques par dictionnaire pré-calculées

**Analogie :** C'est comme ajouter du sel à un plat - même ingrédient, goût complètement différent !

### **Processus détaillé**

#### **1. Inscription (Register)**
```python
# Étape 1: Récupérer le mot de passe
password = request.form["password"]  # Ex: "secret123"

# Étape 2: Convertir en bytes (format ordinateur)
password_bytes = password.encode('utf-8')  # b'secret123'

# Étape 3: Générer un salt unique
salt = bcrypt.gensalt()  # b'$2b$12$abcdefghijklmnopqrstuv'

# Étape 4: Hacher avec le salt
hashed_password = bcrypt.hashpw(password_bytes, salt)
# Résultat: b'$2b$12$abcdefghijklmnopqrstuv...xyz789'

# Étape 5: Convertir pour la base de données
hashed_password_str = hashed_password.decode('utf-8')

# Étape 6: Stocker en base
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
               (username, hashed_password_str))
```

#### **2. Connexion (Login)**
```python
# Étape 1: Récupérer les identifiants
username = request.form["username"]
password = request.form["password"]

# Étape 2: Chercher l'utilisateur en base
cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
user = cursor.fetchone()

if user:
    # Étape 3: Préparer pour la comparaison
    stored_password = user[1].encode('utf-8')  # Hash de la base
    password_bytes = password.encode('utf-8')   # Mot de passe tapé
    
    # Étape 4: Vérifier avec bcrypt
    if bcrypt.checkpw(password_bytes, stored_password):
        return redirect(f"/homepage?username={username}")
    else:
        return "Identifiants incorrects"
```

### **Exemple concret**

**Inscription d'Alice avec "secret123" :**
1. Mot de passe: `"secret123"`
2. Salt généré: `$2b$12$abcdefghijklmnopqrstuv`
3. Hash final: `$2b$12$abcdefghijklmnopqrstuv...xyz789`
4. Stocké en base: `$2b$12$abcdefghijklmnopqrstuv...xyz789`

**Connexion d'Alice avec "secret123" :**
1. Mot de passe tapé: `"secret123"`
2. Hash récupéré: `$2b$12$abcdefghijklmnopqrstuv...xyz789`
3. Salt extrait: `$2b$12$abcdefghijklmnopqrstuv`
4. Re-hash: `$2b$12$abcdefghijklmnopqrstuv...xyz789`
5. Comparaison: ✅ Identique → Connexion réussie !

---

## 🗄️ Base de données MySQL - Commandes utiles

### **Connexion et navigation**
```sql
-- Se connecter
mysql -u root -p

-- Voir toutes les bases
SHOW DATABASES;

-- Utiliser une base
USE ia_project;

-- Voir les tables
SHOW TABLES;
```

### **Gestion des utilisateurs**
```sql
-- Voir tous les utilisateurs
SELECT * FROM users;

-- Voir un utilisateur spécifique
SELECT * FROM users WHERE username = 'alice';

-- Compter les utilisateurs
SELECT COUNT(*) FROM users;

-- Supprimer un utilisateur
DELETE FROM users WHERE username = 'alice';

-- Modifier un mot de passe (si nécessaire)
UPDATE users SET password = 'nouveau_hash' WHERE username = 'alice';
```

### **Maintenance**
```sql
-- Voir la structure de la table
DESCRIBE users;

-- Voir la taille de la base
SELECT table_schema AS 'Database', 
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'ia_project';

-- Optimiser les tables
OPTIMIZE TABLE users;
```

---

## 🎮 Utilisation de l'application

### **1. Première utilisation**
1. Créer un compte → Page d'inscription
2. Se connecter → Page de connexion  
3. Accéder à l'interface → Page d'accueil

### **2. Test de l'IA**
1. Uploader une photo de fruit/légume
2. L'IA analyse l'image
3. Affichage du résultat avec pourcentage de confiance

### **3. Images de test**
Le dossier `validation/` contient des images de test :
- `banane1.jpg`, `carotte.jpg`, `coconut1.jpg`
- `patatoe1.jpg`, `pomme1.jpg`, `tomato1.jpg`

---

## 🔧 Dépannage

### **Erreurs courantes**

#### **"Import could not be resolved"**
```bash
# Vérifier l'installation
pip list | findstr -i "flask mysql bcrypt"

# Réinstaller si nécessaire
pip install --upgrade flask mysql-connector-python bcrypt
```

#### **Erreur de connexion MySQL**
```bash
# Vérifier que MySQL est démarré
# Windows: Services → MySQL
# Linux/Mac: sudo service mysql start

# Vérifier la configuration dans app.py
host="localhost"
user="admin" 
password="admin"
database="ia_project"
```

#### **Erreur "Module not found"**
```bash
# Installer dans l'environnement correct
python -m pip install package_name

# Ou créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 📊 Performance et améliorations

### **Métriques du modèle**
- **Précision d'entraînement :** ~95%
- **Précision de validation :** ~90%
- **Temps d'entraînement :** ~30 minutes (10 epochs)

### **Améliorations possibles**
1. **Plus d'images :** Augmenter le dataset
2. **Data augmentation :** Rotation, zoom, contraste
3. **Architecture :** ResNet, EfficientNet
4. **Hyperparamètres :** Learning rate, batch size

---

## 📚 Ressources et documentation

- **TensorFlow :** https://tensorflow.org
- **Flask :** https://flask.palletsprojects.com
- **MySQL :** https://dev.mysql.com/doc
- **Bcrypt :** https://pypi.org/project/bcrypt

---

## 🚀 Points clés à retenir

- ✅ **L'IA apprend** en regardant des milliers d'exemples
- ✅ **Les mots de passe** sont cryptés avec bcrypt + salt unique
- ✅ **Le modèle analyse** les images par blocs de 3x3 pixels
- ✅ **L'application web** rend l'IA accessible à tous
- ✅ **La base de données** stocke les comptes utilisateurs sécurisés

---

*Projet développé dans le cadre du Workshop 2025 - Reconnaissance IA de Fruits & Légumes*