from flask import Flask, request, redirect, session, Response, send_from_directory
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'Workshop2025-FlaskApp-SecretKey-'

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory('public', filename)

#ICI CA SERT A CHOPER LE FICHIER SCRIPT.JS
@app.route('/script.js')
def serve_script():
    return send_from_directory('homepage', 'script.js')

#ICI CA SERT A CHOPER LES FICHIERS STATICS GENRE CSS ET JS
@app.route('/<path:filename>')
def serve_static(filename):
    if filename.endswith('.css'):
        folder = filename.split('_')[0]
    elif filename.endswith('.js'):
        folder = 'homepage'
    else:
        folder = 'static'
    return send_from_directory(folder, filename)

db = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="ia_project"
)
cursor = db.cursor()
#ICI CA SERT A REDIRIGER VERS LA PAGE DE LOGIN
@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT username, password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[1].encode('utf-8')
            password_bytes = password.encode('utf-8')
            
            if bcrypt.checkpw(password_bytes, stored_password):
                session['username'] = username
                session['logged_in'] = True
                return redirect("/homepage")
            else:
                return "Identifiants incorrects"
        else:
            return "Identifiants incorrects"
    #ICI CA SERT A AFFICHER LE MESSAGE DE SUCCES SI L'UTILISATEUR S'EST INSCRIT AVEC SUCCES
    message = request.args.get('message', '')
    
    with open('login/login.html', encoding='utf-8') as f:
        content = f.read()
    
    if message:
        content = content.replace('<!-- MESSAGE_PLACEHOLDER -->', f'<div class="success-message">{message}</div>')
    
    return Response(content, mimetype='text/html; charset=utf-8')

#ICI CA SERT A INSCRIRE UN NOUVEAU UTILISATEUR
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        
        hashed_password_str = hashed_password.decode('utf-8')

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password_str))
        db.commit()
        
        return redirect("/login?message=Utilisateur créé avec succès ! Vous pouvez maintenant vous connecter.")
    
    with open('register/register.html', encoding='utf-8') as f:
        content = f.read()
    
    return Response(content, mimetype='text/html; charset=utf-8')

#ICI CA SERT A REDIRIGER VERS LA PAGE DE HOMEPAGE
@app.route("/homepage")
def homepage():
    if not session.get('logged_in'):
        return redirect("/login")
    
    username = session.get('username', 'Utilisateur')
    
    with open('homepage/homepage.html', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('username', username)
    
    return Response(content, mimetype='text/html; charset=utf-8')

#ICI CA SERT A DECONNECTER L'UTILISATEUR
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

#ICI CA SERT A LANCER L'APPLICATION
if __name__ == "__main__":
    app.run(debug=True)