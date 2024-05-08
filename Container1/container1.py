from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/store-file', methods=['POST'])
def store_file():
    file_data = request.json
    file_name = file_data.get('file')
    data = file_data.get('data')

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        
        

        data_lines = data.split('\n')
        header = data_lines[0].split(',')
        header = [col.strip() for col in header]
        data_lines[0] = ','.join(header)
        data = '\n'.join(data_lines)

        with open(f'/Mann_PV_dir/{file_name}', 'w') as f:
            f.write(data)
    except Exception as e:
        return jsonify({"file": file_name, "error": f"Error while storing the file to the storage: {str(e)}"}), 500

    return jsonify({"file": file_name, "message": "Success."})

@app.route('/calculate', methods=['POST'])
def calculate():
    file_data = request.json
    file_name = file_data.get('file')

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    response = container2(file_data)
    return jsonify(response)

def container2(json_data):
    try:
        url = "http://k8s-service-c2:8000/calculate"
        response = requests.post(url, json=json_data).json()
        return response
    except requests.exceptions.RequestException as e:
        return {"file": json_data['file'], "error": f"Error communicating with Container 2: {str(e)}"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
