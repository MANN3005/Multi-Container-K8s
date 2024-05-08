from flask import Flask, request, jsonify
import os
import pandas as pd

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    file_data = request.json
    file_name = file_data.get('file')
    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join('/Mann_PV_dir/', file_name)
    
    if not os.path.isfile(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    try:
        df = pd.read_csv(file_path)
        product = file_data.get('product')
        product_df = df[df['product'] == product]
        total_sum = int(product_df['amount'].sum())
        return jsonify({"file": file_name, "sum": total_sum})
    except Exception as e:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)