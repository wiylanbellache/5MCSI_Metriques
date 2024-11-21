from flask import Flask, render_template_string, jsonify
from datetime import datetime
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter

app = Flask(__name__)

# Route principale pour afficher le graphique des commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        response = urlopen(url)
        commits_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des données : {e}'}), 500
    
    # Extraire les minutes
    minutes = []
    for commit in commits_data:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_object.minute)
        except KeyError:
            continue
    
    # Compter les commits par minute
    minute_counts = Counter(minutes)
    sorted_minutes = sorted(minute_counts.items())
    return jsonify(sorted_minutes)


# Route pour la page d'accueil
@app.route('/')
def hello_world():
    return render_template_string('<h1>Bienvenue sur la page principale !</h1>')

# Autres routes (si nécessaires)
@app.route('/contact/')
def contact():
    return render_template("contact.html")

@app.route('/histogramme/')
def histogramme():
    return render_template("histogramme.html")

@app.route('/rapport/')
def mongraphique():
    return render_template("graphique.html")

# Route pour afficher la météo (optionnel)
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# Point d'entrée de l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
