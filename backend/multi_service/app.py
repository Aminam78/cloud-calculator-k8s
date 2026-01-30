from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.json
    return jsonify({"result": data['a'] * data['b']})

@app.route('/divide', methods=['POST'])
def divide():
    data = request.json
    b = data['b']
    if b == 0:
        return jsonify({"error": "Division by zero"}), 400
    return jsonify({"result": data['a'] / b})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "multi-service"}), 200

if __name__ == '__main__':
    # Runs on port 5002 locally to avoid conflict
    app.run(host='0.0.0.0', port=5002)