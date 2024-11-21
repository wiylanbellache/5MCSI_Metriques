from flask import Flask, jsonify, render_template_string, render_template
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
import json
from urllib.request import urlopen

app = Flask(__name__)

# Route pour afficher le graphique des commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    try:
        # Appel à l'API GitHub
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        
        commits_data = response.json()
        
        # Extraire les minutes des dates des commits
        minutes = [
            datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').minute
            for commit in commits_data if 'commit' in commit and 'author' in commit['commit']
        ]
        
        # Compter le nombre de commits par minute
        minute_counts = Counter(minutes)
        sorted_minutes = sorted(minute_counts.items())
        minutes_labels = [item[0] for item in sorted_minutes]
        commit_counts = [item[1] for item in sorted_minutes]
        
        # Générer le graphique
        plt.figure(figsize=(10, 6))
        plt.bar(minutes_labels, commit_counts)
        plt.title('Nombre de commits par minute')
        plt.xlabel('Minute')
        plt.ylabel('Nombre de commits')
        plt.xticks(range(0, 60, 5))  # Intervalles de 5 minutes
        plt.grid(axis='y')
        
        # Convertir le graphique en image pour l'envoyer au client
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()
        
        # Retourner le graphique sous forme d'image HTML
        return render_template_string("""
        <html>
            <head><title>Commits par minute</title></head>
            <body>
                <h1>Graphique : Nombre de commits par minute</h1>
                <img src="data:image/png;base64,{{ graph_url }}" />
            </body>
        </html>
        """, graph_url=graph_url)

    except requests.RequestException as e:
        return jsonify({'error': f"Erreur lors de l'appel à l'API GitHub: {str(e)}"}), 500


# Route de contact (si nécessaire)
@app.route('/contact/')
def contact():
    return "<h2>Page de Contact</h2>"

# Route météo
@app.route('/tawarano/')
def meteo():
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        return jsonify(results=results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route principale (page d'accueil)
@app.route('/')
def hello_world():
    return "<h1>Bienvenue sur mon site Flask !</h1>"

if __name__ == "__main__":
    app.run(debug=True)
