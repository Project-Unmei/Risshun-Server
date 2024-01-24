import risshun
import os
import json
from flask_cors import CORS

from flask import Flask, request, abort, jsonify, render_template, send_file, make_response
from dotenv import dotenv_values

# Check .env file exists
currDir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(f"{currDir}/.env"):
    raise Exception("Please create a .env file with the required environment variables. See .env.example for an example.")

# Load environment variables, convert them to absolute path
ENV = dict(dotenv_values(f"{currDir}/.env"))
#for key, value in ENV.items():
#    ENV[key] = f"{currDir}/{value}"

# Creates the object from autocv for generation
CVGeneration = risshun.docx_template(ENV["TEMPLATE_PATH"],
                                    ENV["RESUME_PATH"],
                                    ENV["OUTPUT_DIR"], 
                                    openai_key=ENV["OPENAI_KEY"], 
                                    silent=False)

app = Flask(__name__)
CORS(app)

# Replace with your actual API key
API_KEY = 'TESTAPIKEY'



@app.route('/', methods=['GET'])
def home():
    return render_template("local-portal/index.html")



@app.route('/api/cv/return', methods=['GET'])
def return_cv():
    # Check if the 'X-API-KEY' header is present and contains the correct API key
    if request.headers.get('X-API-KEY') == API_KEY:
        tempID = request.args.get('id')
        # Check if the output directory contains the file
        if os.path.exists(f"{ENV['OUTPUT_DIR']}/{tempID}.docx"):
            return send_file(f"{ENV['OUTPUT_DIR']}/{tempID}.docx", as_attachment=True)
        else:
            return jsonify({"message": "File not found"}), 404
    else:
        abort(401)



@app.route('/api/cv/generate', methods=['POST'])   
def handle_request():
    
    # Check if the 'X-API-KEY' header is present and contains the correct API key
    if request.headers.get('X-API-KEY') == API_KEY:
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
            return jsonify({"message": f"CV Generated, use get request at /api/cv/return?id={json_payload['UID']}"}), 200
        else:
            return jsonify({"message": "Missing JSON in request"}), 400
    else:
        abort(401)



if __name__ == '__main__':
    app.run(port=6969, debug=True)
