from flask import Flask, request, abort, jsonify, render_template

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
            print(json_payload)
            return jsonify({"message": "JSON received"}), 200
        else:
            return jsonify({"message": "Missing JSON in request"}), 400
    else:
        abort(401)

if __name__ == '__main__':
    app.run(port=5000)
