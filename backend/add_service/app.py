from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    return jsonify({"result": data['a'] + data['b']})

@app.route('/subtract', methods=['POST'])
def subtract():
    data = request.json
    return jsonify({"result": data['a'] - data['b']})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "add-service"}), 200

if __name__ == '__main__':
    # Runs on port 5001 locally to avoid conflict
    app.run(host='0.0.0.0', port=5001)