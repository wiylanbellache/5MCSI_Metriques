from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from collections import Counter
from datetime import datetime
from flask import jsonify
                                                                                                                                       
app = Flask(__name__)
@app.route('/commits/')
def commits():
    return render_template('commits.html')


@app.route("/contact/")
def contact():
    return render_template("contact.html")
# return "<h2>Ma page de contact</h2>"
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  @app.route('/commits-data/')
def commits_data():
    # URL de l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    
    if response.status_code == 200:
        commits = response.json()
        minutes = []
        
        for commit in commits:
            # Extraire les minutes des dates des commits
            commit_date = commit.get('commit', {}).get('author', {}).get('date')
            if commit_date:
                date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
                minutes.append(date_object.minute)
        
        # Compter les commits par minute
        minutes_count = Counter(minutes)
        formatted_data = [{'minute': k, 'count': v} for k, v in minutes_count.items()]
        
        return jsonify(results=formatted_data)
    else:
        return jsonify({'error': 'Failed to fetch data from GitHub API'}), 500

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
