import risshun
import os
import json
import webbrowser
from flask_cors import CORS

from flask import Flask, request, abort, jsonify, render_template, send_file, make_response
from dotenv import dotenv_values

# Check .env file exists
currDir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(f"{currDir}/.env"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

 
# Grabs environment variables from defined path
ENV = dict(dotenv_values(f"{currDir}/.env"))

# If WORKING_DIR is not set, add currDir in front of each value, otherwise, add the WORKING_DIR in front of each value
if "WORKING_DIR" in ENV.keys():
    for key, value in ENV.items():
        if key != "WORKING_DIR" and key != "OPENAI_KEY":
            ENV[key] = f"{ENV['WORKING_DIR']}/{value}"
else:
    for key, value in ENV.items():
        ENV[key] = f"{currDir}/{value}"

# Creates the object from autocv for generation
CVGeneration = risshun.docx_template(config = ENV)

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template("local-portal/index.html")



@app.route('/api/cv/return', methods=['GET'])
def return_cv():
    # Check if the 'X-API-KEY' header is present and contains the correct API key
    tempID = request.args.get('id')
    # Check if the output directory contains the file
    if os.path.exists(f"{ENV['OUTPUT_DIR']}/{tempID}.docx"):
        return send_file(f"{ENV['OUTPUT_DIR']}/{tempID}.docx", as_attachment=True)
    else:
        return jsonify({"message": "File not found"}), 404


@app.route('/api/cv/generate', methods=['POST'])   
def handle_request():
    # Check if the request contains a JSON payload
    if request.is_json:
        json_payload = request.get_json()
        try:
            outputPath = CVGeneration.find_and_replace_single(json_payload)
        except Exception as e:
            print("Error: AutoCV has failed in generation.")
            # Print the error
            print(e)
            return jsonify({"message": "AutoCV has failed in generation."}), 500
        print(outputPath)
        return send_file(outputPath, as_attachment=True)
    else:
        return jsonify({"message": "Missing JSON in request"}), 400



if __name__ == '__main__':
    webbrowser.open_new_tab('http://localhost:6969/')
    app.run(port=6969, debug=True)
    
