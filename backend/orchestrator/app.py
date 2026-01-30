from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re

app = Flask(__name__)
CORS(app)

# Service Discovery Environment Variables
# Default urls are for local testing (Note the different ports)
ADD_SERVICE_URL = os.getenv('ADD_SERVICE_URL', 'http://localhost:5001')
MULTI_SERVICE_URL = os.getenv('MULTI_SERVICE_URL', 'http://localhost:5002')

def call_service(url, operation, a, b):
    try:
        # Sending request to worker microservices
        resp = requests.post(f"{url}/{operation}", json={"a": float(a), "b": float(b)}, timeout=5)
        if resp.status_code == 200:
            return resp.json()['result']
        raise Exception(resp.json().get('error', 'Unknown error'))
    except Exception as e:
        raise Exception(f"Service call failed: {str(e)}")

def solve_expression(tokens):
    """
    Solves the math expression respecting order of operations:
    1. Multiplication and Division
    2. Addition and Subtraction
    """
    # --- Step 1: Multiplication and Division ---
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/'):
            op = 'multiply' if tokens[i] == '*' else 'divide'
            val1 = tokens[i-1]
            val2 = tokens[i+1]
            
            # Call Multi-Service
            result = call_service(MULTI_SERVICE_URL, op, val1, val2)
            
            # Update tokens list with result
            tokens[i-1] = result
            del tokens[i:i+2]
            i -= 1 
        else:
            i += 1
            
    # --- Step 2: Addition and Subtraction ---
    i = 0
    while i < len(tokens):
        if tokens[i] in ('+', '-'):
            op = 'add' if tokens[i] == '+' else 'subtract'
            val1 = tokens[i-1]
            val2 = tokens[i+1]
            
            # Call Add-Service
            result = call_service(ADD_SERVICE_URL, op, val1, val2)
            
            tokens[i-1] = result
            del tokens[i:i+2]
            i -= 1
        else:
            i += 1
            
    return tokens[0]

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expr = data.get('expression', '')
    
    try:
        # Simple Parser: "2+2*3" -> ['2', '+', '2', '*', '3']
        expr = expr.replace(" ", "")
        tokens = re.split(r'(\+|\-|\*|/)', expr)
        # Filter out empty strings
        tokens = [t for t in tokens if t]
        
        final_result = solve_expression(tokens)
        return jsonify({"result": final_result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "orchestrator"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)