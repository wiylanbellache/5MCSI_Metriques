from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def contact():
    return render_template("contact.html")
# return "<h2>Ma page de contact</h2>"
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
  @app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
  
@app.route('/commits_graph/')
def commits_graph():
    return render_template('commits.html')

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route('/commits/')
def commits():
    # URL de l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Appel à l'API GitHub
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Impossible de récupérer les données depuis GitHub'}), 500
    
    commits_data = response.json()
    
    # Extraire les minutes des dates des commits
    minutes = []
    for commit in commits_data:
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

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
