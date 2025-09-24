from flask import Flask, request, redirect, render_template_string, send_from_directory
import mysql.connector

app = Flask(__name__)


@app.route('/<path:filename>')
def serve_static(filename):
    if filename.endswith('.css'):
        folder = filename.split('_')[0] if '_' in filename else 'static'
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

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(f"/homepage?username={username}")
        else:
            return "Identifiants incorrects"
    
    with open('login/login.html') as f:
        return f.read()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return "Utilisateur créé !"
    
    with open('register/register.html') as f:
        return f.read()

@app.route("/homepage")
def homepage():
    username = request.args.get('username', 'Utilisateur')
    
    
    with open('homepage/homepage.html') as f:
        content = f.read()
    
    
    content = content.replace(
        '<h1>Bienvenue sur la homepage</h1>',
        f'<h1>Bienvenue sur la homepage {username}</h1>'
    )
    
    return content

if __name__ == "__main__":
    app.run(debug=True)
