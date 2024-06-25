import json
import subprocess
import pandas as pd

try:
    from flask import Flask, jsonify
except ImportError:
    subprocess.check_call(["pip", "install", "flask"])
    from flask import Flask, jsonify

import csprng
import tester

app = Flask(__name__)

# Create an instance of your class
rng = csprng.CSPRNG(32)

# Define a route that calls the class method
@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = rng.rand_int(0, 100)
    return jsonify({'random_number': random_number})

@app.route('/csv_to_json', methods=['GET'])
def csv_to_json():
    df = pd.read_csv('array.csv')
    return jsonify(df.to_dict(orient='records'))

@app.route('/txt_to_json', methods=['GET'])
def txt_to_json():
    with open('system_info.txt', 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
