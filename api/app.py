import pickle
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

departements = pd.read_csv('../assets/data/departement.csv', sep=';')

with open("../assets/models/random-forest-regressor-all.pkl", "rb") as f:
    model = pickle.load(f)

regresssor = model['model']
scaler = model['scaler']

def predictPrice(metre_carre, population, surface):
    x = pd.DataFrame([[metre_carre,	population,	surface]], columns=regresssor.feature_names_in_)
    x = pd.DataFrame(scaler.transform(x), columns=regresssor.feature_names_in_)
    v = regresssor.predict(x)[0]
    return v

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-secret-key'

cors = CORS(app, resources={r'/*': {'origin': '*'}})

@app.route('/estimate', methods=['GET'])
def estimate():

    try:
        surface = request.args.get('surface')
        departement = request.args.get('departement')
    
        dep_info = departements[departements['code_departement'] == departement]
        population = dep_info['population'].values[0]
        metre_carre = dep_info['metre carre'].values[0]
    
        estimation = round(predictPrice(metre_carre, population, surface), 2)
    except:
        estimation = 'Error'
    
    result = {'estimation': estimation}
    return jsonify(result)

if __name__ == '__main__':
    app.run()