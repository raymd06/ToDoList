import sqlite3

class ToDoModel:
    def __init__(self):
        # Initialise une instance de la base de données
        db = DataBaseMode("todolist.db")

    def get_all(self):
        # Récupère toutes les tâches en triant par état (checkbox) et date de création (ordre décroissant)
        query = "SELECT * FROM List ORDER BY checkbox ASC, datetime DESC"
        db = DataBaseMode("todolist.db")
        tasks = db.execute_query(query)
        return tasks

class DataBaseMode:
    def __init__(self, db_path): 
        # Initialise la connexion à la base de données avec le chemin spécifié
        self.db_path = db_path
   
    def execute_query(self, query, parameters=()):
        # Exécute une requête SQL avec ou sans paramètres
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            # Si la requête est une requête SELECT, retourne les résultats
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()  # Sinon, applique les changements à la base de données

    def create_table(self):
        # Crée la table List si elle n'existe pas déjà
        query = """
        CREATE TABLE IF NOT EXISTS List(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            datetime TEXT,
            checkbox INTEGER DEFAULT 0 
        )"""
        self.execute_query(query)

    def delete_table(self):
        # Supprime la table List
        query = "DROP TABLE List"
        self.execute_query(query)
        
    def insert_list(self, list_data):
        # Insère une nouvelle tâche dans la table List
        query = """
        INSERT INTO List (title, description, datetime)
        VALUES(?,?,?)"""
        self.execute_query(query, list_data)

    def delete_task(self, task_id):
        # Supprime une tâche spécifique en fonction de son id
        query = "DELETE FROM List WHERE id = ?"
        self.execute_query(query, (task_id,))
