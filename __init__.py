from flask import Flask, render_template_string, jsonify
import matplotlib.pyplot as plt
import json
from datetime import datetime
from urllib.request import urlopen
import io
import base64
from collections import Counter

app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def hello_world():
    return render_template_string('<h2>Bienvenue sur ma page d\'accueil !</h2>')

# Route pour la page de contact
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Route pour l'histogramme
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# Route pour le graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Route pour afficher le graphique des commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Récupération des données de l'API GitHub
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des données : {e}'}), 500
    
    # Extraction des minutes des dates des commits
    minutes = []
    for commit in data:
        try:
            date_string = commit['commit']['author']['date']
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(date_object.minute)
        except KeyError:
            continue

    # Compter le nombre de commits par minute
    minute_counts = Counter(minutes)
    sorted_minutes = sorted(minute_counts.items())
    minutes_labels = [item[0] for item in sorted_minutes]
    commit_counts = [item[1] for item in sorted_minutes]

    # Générer le graphique
    plt.figure(figsize=(10, 6))
    plt.bar(minutes_labels, commit_counts, width=1.0)
    plt.title('Nombre de commits par minute')
    plt.xlabel('Minutes')
    plt.ylabel('Nombre de commits')
    plt.xticks(range(0, 60, 5))  # Intervalles de 5 minutes
    plt.grid(axis='y')

    # Convertir le graphique en image pour l'afficher dans le navigateur
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    # Rendre le graphique dans une page HTML
    return render_template_string("""
    <html>
        <head><title>Commits par minute</title></head>
        <body>
            <h1>Graphique : Nombre de commits par minute</h1>
            <div style="text-align: center;">
                <img src="data:image/png;base64,{{ graph_url }}" alt="Graphique des commits" />
            </div>
        </body>
    </html>
    """, graph_url=graph_url)

# Route pour la météo (pour information, si elle est utilisée)
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
