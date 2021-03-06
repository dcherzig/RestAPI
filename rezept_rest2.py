import sqlite3
from flask import Flask, jsonify, request
from sqlite3 import Error
import os


app = Flask(__name__)
cwd = os.getcwd
#======================##initialize the db and fill in the first data##=============#
database = ".\database.db"

connection = sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES)
with open('schema.sql') as f:
  connection.executescript(f.read())
cur = connection.cursor()
data = [{'titel': 'Risotto', 'zutaten':'Reis, Bouillon, Zwiebeln', 'beschreibung': 'Reis anduensten, abloeschen mit Bouillon, koecheln lassen'}, {'titel': 'Pancakes', 'zutaten':'Eier, Milch, Mehl', 'beschreibung': 'Alles zusammenmischen, kurz stehen lassen und dann in die Pfanne geben'}, {'titel': 'Pancakes', 'zutaten':'Eier, Milch, Mehl', 'beschreibung': 'Alles, kurz stehen lassen und dann in die Pfanne geben'}]
sql = "INSERT INTO rezepte(titel, zutaten, beschreibung) VALUES (?, ?,?);"

for rezept in data:
  cur.execute(sql, (rezept['titel'], rezept['zutaten'], rezept['beschreibung']))

connection.commit()
connection.close()
#=================================================================================#

#======================##Functions for the API##==================================#

def get_db():
  """Verbindung mit der sqlite3 Datenbank mit Name: database
  return: connection"""
  conn = None
  try:
    conn = sqlite3.connect(database)
  except Error as e:
    print(e)
  return conn


def get_post():
  """Input: -
  Funktion um alle Rezepte auszuwählen
  Output: alle Rezepte in der Datenbank inkl. Titel, Zutaten und Beschreibung"""
  try:
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM rezepte')
    rezepte = [dict(id=row[0], titel=row[1], zutaten=row[2], beschreibung = row[3]) for row in cursor.fetchall()]
    if rezepte is not None:
      return rezepte
  except Exception:
    raise
  


def get_id(id):
  """Input: id
  Funktion um ein Rezept anhand der id auszuwählen
  Output: Rezept inkl. Titel, Zutaten und Beschreibung
  """
  try:
    db = get_db()
    cursor = db.cursor()
    rezept = None
    cursor.execute('SELECT * FROM rezepte WHERE id = ?', (id,))
    rows = cursor.fetchall()
    for r in rows:
      rezept = r
    if rezept is not None:
      return rezept
  except Exception:
    raise



def insert_post(new_titel, new_zutaten, new_beschreibung):
  """Input: titel, Zutaten, Beschreibung
  Funktion um ein neues Rezept zu erstellen
  Output: Neues Rezept wird in die Datenbank eingefügt"""
  try:
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO rezepte (titel, zutaten, beschreibung) VALUES (?,?,?)', (new_titel, new_zutaten, new_beschreibung))
    db.commit()
    return True
  except Exception:
    raise
  


def update_post(titel, zutaten, beschreibung, id):
  """Input: titel, Zutaten, Beschreibung, id
  Funktion um ein bestehendes Rezept anhand der id auszuwählen und anzupassen
  Output: aktualisiertes Rezept wird in der Datenbank eingefügt"""
  try:
    db = get_db()
    updated_rezept = {
      "id": id,
      "titel": titel,
      "zutaten": zutaten,
      "beschreibung": beschreibung,
    }
    db.execute('UPDATE rezepte SET titel = ?, zutaten = ?, beschreibung = ?' 'WHERE id = ?', (titel, zutaten, beschreibung, id))
    db.commit()
    return updated_rezept
  except Exception:
    raise


def delete_post(id):
  """Input: id
  Funktion um ein Rezept aus der Datenbank zu löschen
  Output: Rezept wird in der Datenbank gelöscht"""
  try:
    db = get_db()
    #cursor = db.cursor()
    db.execute('DELETE FROM rezepte WHERE id= ?', (id,))
    db.commit()
    return "Das Rezept mit der id: {} wurde geloescht".format(id)
  except Exception:
    raise
  



##routes for the flask application:
@app.route('/')
def welcome():
  return "Willkommen zu unserer Rezeptdatenbank"

@app.route('/rezepte', methods=["GET", "POST"])
def rezepte():
  """GET und POST - Route von Rezepten
  Input: -
  Output: Rezepte bzw. neues Rezept in der Datenbank"""
  if request.method == "GET":
    return jsonify(get_post())
  if request.method == "POST":
    try:
      new_titel = request.form["titel"]
      new_zutaten = request.form["zutaten"]
      new_beschreibung = request.form["beschreibung"]
      insert_post(new_titel, new_zutaten, new_beschreibung)
      return f"Rezept wurde erfolgreich kreiert", 201
    except Exception as e:
      return f"Fehler beim Hinzufuegen des Rezepts", 400

    

@app.route('/rezept/<int:id>', methods=["GET", "PUT", "DELETE"])
def get_rezept_id(id):
  """GET, PUT, DELETE-Routen für ein Rezept anhand der id
  Input: id
  Output: Ein Rezept, das verändert, gelesen oder gelöscht wird """
  if request.method == "GET":
    try:
      rezept = get_id(id)
      if rezept is None:
        return f"Fehler beim Laden", 404
      return jsonify(rezept)
    except Exception as e:
      return jsonify(f"Fehler beim Laden des Rezepts: {e}")
  if request.method == "PUT":
    try:
      titel = request.form["titel"]
      zutaten = request.form["zutaten"]
      beschreibung = request.form["beschreibung"]
      update_post(titel, zutaten, beschreibung, id) 
      return f"Rezept wurde erfolgreich geaendert"
    except Exception as e:
      return f"Fehler beim Aendern des Rezepts", 400
  if request.method == "DELETE":
    try:
      if id in get_id(id):
        return delete_post(id)
      return f"Dieses Rezept existiert nicht", 400
    except Exception as e:
      return f"Fehler beim Loeschen des Rezepts", 400

@app.errorhandler(405)
def page_not_found(e):
  return f"Diese Methode ist nicht erlaubt"  

@app.errorhandler(404)
def page_not_found(e):
  return f"Diese Seite konnte leider nicht gefunden werden"  

@app.errorhandler(400)
def bad_request(message):
  return f"Server kann die Anfrage leider nicht verarbeiten"


@app.errorhandler(500)
def internal_error(e):
  return f"Ein unvorhergesehener Fehler ist aufgetreten"

if __name__=="__main__":

  app.run(debug=True)






