from flask import Flask, render_template, request, redirect, url_for
from model import ToDoModel, DataBaseMode
from datetime import datetime

# Création de l'application Flask
app = Flask(__name__)

# Initialisation du modèle et de la base de données
model = ToDoModel()
db = DataBaseMode("todolist.db")
db.create_table()  # Création de la table si elle n'existe pas

# Route principale qui affiche la liste des tâches
@app.route("/")
def index():
    tasks = model.get_all()  # Récupère toutes les tâches depuis la base de données
    return render_template("index.html", tasks=tasks)  # Affiche la page avec les tâches

# Route pour ajouter une nouvelle tâche
@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")  # Récupère le titre de la tâche
    desc = request.form.get("desc")  # Récupère la description de la tâche
    dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  # Obtient la date et l'heure actuelles
    db.insert_list((task, desc, dt))  # Insère la nouvelle tâche dans la base de données
    return redirect(url_for("index"))  # Redirige vers la page principale

# Route pour supprimer une tâche
@app.route('/remove/<int:task_id>')
def remove_task(task_id):
    db.delete_task(task_id)  # Supprime la tâche de la base de données
    return redirect(url_for('index'))  # Redirige vers la page principale

# Route pour cocher/décocher une tâche
@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    query = "UPDATE List SET checkbox = CASE WHEN checkbox=1 THEN 0 ELSE 1 END WHERE id = ?"
    db.execute_query(query, (task_id,))  # Met à jour l'état de la tâche (complétée ou non)
    return redirect(url_for('index'))  # Redirige vers la page principale

# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(debug=True)  # Mode debug activé pour le développement
