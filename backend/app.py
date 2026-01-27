from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Receives a JSON payload like {"expression": "2+2"}
    Returns {"result": 4, "status": "success"}
    """
    data = request.json
    if not data or 'expression' not in data:
        return jsonify({"error": "No expression provided", "status": "error"}), 400
    
    expression = data.get('expression')
    
    try:
        # Basic validation to allow only math characters (for security)
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
             return jsonify({"error": "Invalid characters. Only numbers and +, -, *, / allowed.", "status": "error"}), 400

        # Compute the result
        # In production, use a library like 'numexpr', but 'eval' is fine for this assignment.
        result = eval(expression) 
        
        # Format result (remove .0 if it's an integer)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        return jsonify({"result": result, "status": "success"})
        
    except ZeroDivisionError:
        return jsonify({"error": "Cannot divide by zero", "status": "error"}), 400
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "pod": os.getenv("HOSTNAME", "unknown")}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)