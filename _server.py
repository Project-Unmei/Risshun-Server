import autocv
import os
import json
from flask import Flask, request, abort, jsonify, render_template, send_file
from dotenv import dotenv_values

# Check .env file exists
currDir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(f"{currDir}/.env.example"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables, convert them to absolute path
ENV = dict(dotenv_values(f"{currDir}/.env.example"))
for key, value in ENV.items():
    ENV[key] = f"{currDir}/{value}"


# Creates the object from autocv for generation
CVGeneration = autocv.docx_template(autocv.csv_to_dict(ENV["LUT_PATH"]), ENV["TEMPLATE_PATH"], ENV["OUTPUT_DIR"])

app = Flask(__name__)

# Replace with your actual API key
API_KEY = 'TESTAPIKEY'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])   
def handle_request():
    # Check if the 'X-API-KEY' header is present and contains the correct API key
    if request.headers.get('X-API-KEY') == API_KEY:
        # Check if the request contains a JSON payload
        if request.is_json:
            json_payload = request.get_json()
            try:
                outputPath = CVGeneration.find_and_replace_single(json_payload)
            except:
                print("Error: AutoCV has failed in generation.")
                return jsonify({"message": "AutoCV has failed in generation."}), 500
            return send_file(outputPath, as_attachment=True)
        else:
            return jsonify({"message": "Missing JSON in request"}), 400
    else:
        abort(401)

if __name__ == '__main__':
    app.run(port=6969, debug=True)
