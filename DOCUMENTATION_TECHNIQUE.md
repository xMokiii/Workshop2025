# 📚 Documentation Technique - Projet IA Reconnaissance Fruits/Légumes

## 🎯 Vue d'ensemble du projet

Ce projet utilise l'intelligence artificielle pour reconnaître automatiquement différents types de fruits et légumes à partir de photos. C'est un système de **classification d'images** qui apprend à distinguer les caractéristiques visuelles de chaque aliment.

---

## 🧠 Les concepts de base

### **Intelligence Artificielle (IA)**
- C'est comme apprendre à un ordinateur à "voir" et "comprendre" les images
- L'ordinateur apprend en regardant des milliers d'exemples de photos

### **Deep Learning / Apprentissage profond**
- Technique qui simule le fonctionnement du cerveau humain
- Le réseau "apprend" progressivement à reconnaître les patterns (motifs) dans les images

### **CNN (Convolutional Neural Network)**
- Type de réseau de neurones spécialement conçu pour traiter les images
- Comme si l'ordinateur avait des "yeux" qui analysent l'image petit bout par petit bout

---

## 🛠️ Les outils utilisés

### **TensorFlow**
- **Qu'est-ce que c'est ?** Une bibliothèque (boîte à outils) créée par Google pour faire de l'IA
- **À quoi ça sert ?** À construire et entraîner des modèles d'IA facilement
- **Analogie :** C'est comme avoir tous les outils nécessaires pour construire une maison, mais pour construire un cerveau artificiel

### **Keras**
- **Qu'est-ce que c'est ?** Une interface simple qui utilise TensorFlow en arrière-plan
- **À quoi ça sert ?** À rendre la création de modèles d'IA plus facile et intuitive
- **Analogie :** C'est comme avoir un assistant qui vous aide à utiliser tous les outils TensorFlow

---

## 🏗️ Architecture du modèle (les "couches" du cerveau)

### **Sequential**
- **Qu'est-ce que c'est ?** Une façon de construire le modèle couche par couche
- **Analogie :** Comme empiler des couches de gâteau, une par une, dans l'ordre

### **Conv2D (Convolution 2D)**
- **Qu'est-ce que c'est ?** La "couche qui regarde" - elle analyse l'image pour trouver des motifs
- **32 filtres :** Le réseau apprend 32 "motifs" différents (bords, textures, couleurs, formes...)
- **(3,3) :** Taille de la "fenêtre" qui analyse l'image (regarde des blocs de 3x3 pixels)
- **activation='relu' :** Fonction qui aide le réseau à apprendre des relations complexes
- **Analogie :** Comme avoir 32 paires d'yeux différentes, chacune spécialisée pour voir un type de détail

### **MaxPooling2D**
- **Qu'est-ce que c'est ?** Réduit la taille de l'image en gardant les informations importantes
- **Analogie :** Comme faire un résumé d'un livre - on garde l'essentiel, on supprime les détails

### **Flatten**
- **Qu'est-ce que c'est ?** Transforme une matrice (grille 2D) en une ligne de nombres
- **Analogie :** Comme déplier une carte pliée pour la mettre à plat

### **Dense**
- **Qu'est-ce que c'est ?** Couche qui prend toutes les informations et fait des connexions
- **128 neurones :** 128 "cerveaux mini" qui traitent l'information
- **Analogie :** Comme avoir 128 assistants qui analysent toutes les informations collectées

### **Dropout**
- **Qu'est-ce que c'est ?** Technique pour éviter le "sur-apprentissage" (mémorisation par cœur)
- **0.5 :** Désactive aléatoirement 50% des connexions pendant l'entraînement
- **Analogie :** Comme faire réviser un étudiant en lui posant des questions variées pour qu'il comprenne vraiment

### **Dense final avec softmax**
- **num_classes :** Nombre de types de fruits/légumes (ex: 7 classes = pomme, banane, carotte, etc.)
- **softmax :** Transforme les résultats en probabilités qui s'additionnent à 100%
- **Exemple de sortie :** [0.05, 0.85, 0.10] = 5% pomme, 85% banane, 10% carotte

---

## 📊 Préparation des données

### **Normalisation des pixels**
```python
train_ds = train_ds.map(lambda x, y: (x/255.0, y))
```
- **Pourquoi ?** Les images ont des pixels de 0 à 255 (niveaux de gris/couleur)
- **Transformation :** On divise par 255 pour avoir des valeurs entre 0 et 1
- **Avantage :** Plus facile pour l'IA d'apprendre avec des nombres plus petits
- **Analogie :** Comme convertir des euros en centimes pour faire des calculs plus simples

### **Configuration des images**
- **Taille :** 64x64 pixels (standardisation)
- **Batch size :** 16 images traitées à la fois
- **Seed :** 123 (pour que l'ordre soit toujours le même - reproductibilité)

---

## 🔍 Fonction de prédiction

### **Comment ça marche ?**

1. **Chargement de l'image**
   - Prend la photo et la redimensionne à 64x64 pixels

2. **Préparation**
   - Transforme l'image en tableau de nombres
   - Normalise les pixels (÷255)
   - Ajoute une dimension pour le traitement par lot

3. **Prédiction**
   - Le modèle analyse l'image
   - Retourne des probabilités pour chaque classe

4. **Résultat**
   - Trouve la classe avec la plus haute probabilité
   - Affiche le nom du fruit/légume détecté

---

## 🌐 Application Web (app.py)

### **Flask**
- **Qu'est-ce que c'est ?** Framework pour créer des sites web en Python
- **À quoi ça sert ?** À transformer notre modèle d'IA en application web utilisable

### **Structure de l'application**

#### **Authentification**
- **Login/Register :** Système de connexion utilisateur
- **Base de données :** Stockage des comptes utilisateurs (MySQL)

#### **Upload d'images**
- **Fonctionnalité :** L'utilisateur peut uploader une photo
- **Traitement :** L'image est analysée par le modèle d'IA
- **Résultat :** Affichage de la prédiction

#### **Interface utilisateur**
- **Design :** Style cyberpunk/retro avec effets de glow
- **Expérience :** Interface intuitive pour les utilisateurs lambda

---

## 🎮 Comment utiliser l'application

1. **Créer un compte** → Page d'inscription
2. **Se connecter** → Page de connexion
3. **Uploader une photo** → Interface d'upload
4. **Voir le résultat** → L'IA prédit le type de fruit/légume

---

## 🔧 Vocabulaire technique simplifié

| Terme technique | Explication simple |
|----------------|-------------------|
| **Modèle** | Le "cerveau" de l'IA qui a appris à reconnaître |
| **Entraînement** | Phase où l'IA apprend avec des milliers d'exemples |
| **Prédiction** | Quand l'IA "devine" ce qu'elle voit sur une nouvelle image |
| **Classe** | Un type de fruit/légume (ex: "pomme", "banane") |
| **Probabilité** | Pourcentage de confiance (ex: 85% banane) |
| **Dataset** | Collection de milliers d'images d'entraînement |
| **Validation** | Test du modèle avec des images qu'il n'a jamais vues |

---

## 🚀 Points clés à retenir

- **L'IA apprend** en regardant des milliers d'exemples
- **Plus il y a d'exemples**, plus l'IA est précise
- **Le modèle analyse** les images par petits blocs (3x3 pixels)
- **Chaque couche** a un rôle spécifique dans l'analyse
- **L'application web** rend l'IA accessible à tous
- **La normalisation** rend l'apprentissage plus efficace

---

## 🔐 Sécurité : Cryptage et Salage des Mots de Passe

### **Pourquoi crypter les mots de passe ?**

Imaginez que quelqu'un vole votre base de données. Si les mots de passe sont stockés en clair :
- ❌ **Danger** : `password: "monmotdepasse123"` → Visible par tous !
- ✅ **Sécurité** : `password: "$2b$12$LQv3c1yqBWVHxkd0LHAkC..."` → Impossible à lire !

### **Qu'est-ce que le "salage" (salt) ?**

Le **salt** est comme un **assaisonnement unique** pour chaque mot de passe :
- Même mot de passe + salt différent = hash complètement différent
- Empêche les attaques par dictionnaire pré-calculées

**Analogie :** C'est comme ajouter du sel à un plat - même ingrédient de base, goût complètement différent !

---

## 🔧 Code détaillé : Inscription (Register)

### **Étape 1 : Récupération du mot de passe**
```python
password = request.form["password"]
```
**Explication :** L'utilisateur tape "monmotdepasse123" dans le formulaire

### **Étape 2 : Conversion en bytes**
```python
password_bytes = password.encode('utf-8')
```
**Explication :** 
- Les ordinateurs travaillent avec des bytes (0 et 1)
- `encode('utf-8')` transforme le texte en bytes


### **Étape 3 : Génération du salt**
```python
salt = bcrypt.gensalt()
```
**Explication :**
- Génère un salt **unique et aléatoire** pour chaque mot de passe
- **Exemple :** `b'$2b$12$abcdefghijklmnopqrstuv'`
- Le `12` indique la "difficulté" (plus c'est élevé, plus c'est sécurisé mais lent)

### **Étape 4 : Hachage avec salt**
```python
hashed_password = bcrypt.hashpw(password_bytes, salt)
```
**Explication :**
- Combine le mot de passe + le salt
- Applique l'algorithme bcrypt
- **Résultat :** `b'$2b$12$abcdefghijklmnopqrstuv...'` (60+ caractères)

### **Étape 5 : Conversion pour stockage**
```python
hashed_password_str = hashed_password.decode('utf-8')
```
**Explication :**
- Convertit les bytes en string pour la base de données
- **Avant :** `b'$2b$12$...'` (bytes)
- **Après :** `'$2b$12$...'` (string)

### **Étape 6 : Stockage en base**
```python
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
               (username, hashed_password_str))
```
**Explication :** Stocke le hash (jamais le mot de passe original !)

---

## 🔍 Code détaillé : Connexion (Login)

### **Étape 1 : Récupération des données**
```python
username = request.form["username"]
password = request.form["password"]
```
**Explication :** L'utilisateur tape ses identifiants

### **Étape 2 : Recherche en base**
```python
cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
user = cursor.fetchone()
```
**Explication :**
- Cherche l'utilisateur par nom
- Récupère le hash stocké
- **user[0]** = username, **user[1]** = password hashé

### **Étape 3 : Préparation pour vérification**
```python
stored_password = user[1].encode('utf-8')  # Hash de la base
password_bytes = password.encode('utf-8')   # Mot de passe tapé
```
**Explication :**
- Convertit tout en bytes pour la comparaison
- **stored_password** = hash stocké en base
- **password_bytes** = mot de passe tapé par l'utilisateur

### **Étape 4 : Vérification avec bcrypt**
```pythons
if bcrypt.checkpw(password_bytes, stored_password):
    return redirect(f"/homepage?username={username}")
else:
    return "Identifiants incorrects"
```
**Explication :**
- `bcrypt.checkpw()` compare automatiquement
- Extrait le salt du hash stocké
- Re-hash le mot de passe tapé avec ce salt
- Compare les deux hashs

---

## 🔬 Exemple concret pas à pas

1. **Mot de passe original :** `"secret123"`
2. **Salt généré :** `$2b$12$abcdefghijklmnopqrstuv`
3. **Hash final :** `$2b$12$abcdefghijklmnopqrstuv...xyz789`
4. **Stocké en base :** `$2b$12$abcdefghijklmnopqrstuv...xyz789`


## 🛡️ Avantages de bcrypt

| Avantage | Explication |
|----------|-------------|
| **Salt automatique** | Chaque mot de passe a un salt unique |
| **Coût adaptatif** | Plus lent = plus sécurisé (ajustable) |
| **Résistant aux attaques** | Très difficile à cracker |
| **Standard industrie** | Utilisé par de nombreuses applications |
| **Inclut le salt** | Le salt est stocké avec le hash |

---



