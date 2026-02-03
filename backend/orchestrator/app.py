from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import re
import psycopg2
import time

app = Flask(__name__)
CORS(app)

# --- Configs ---
ADD_SERVICE_URL = os.getenv('ADD_SERVICE_URL', 'http://localhost:5001')
MULTI_SERVICE_URL = os.getenv('MULTI_SERVICE_URL', 'http://localhost:5002')

# Database Config (Default values matching Helm chart)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password123')

# --- Database Functions ---
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    """Create table if not exists and seed a default user."""
    # Retry logic because DB might take time to start in K8s
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Create Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS credits (
                    username VARCHAR(50) PRIMARY KEY,
                    balance INT NOT NULL
                );
            """)
            # Create a test user 'admin' with 1000 credits
            cur.execute("INSERT INTO credits (username, balance) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;", ('admin', 1000))
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Database initialized successfully.")
            break
        except Exception as e:
            print(f"⏳ Waiting for DB... ({e})")
            time.sleep(3)
            retries -= 1

# Initialize DB on startup
init_db()

def process_billing(username, cost):
    """
    Deducts credit. Returns new balance if successful, None if insufficient funds.
    Also creates user with 100 credits if they don't exist (Registration logic).
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Auto-register user with 100 credits if new
        cur.execute("INSERT INTO credits (username, balance) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;", (username, 100))
        
        # Check and Update Balance (Atomic Update)
        cur.execute("""
            UPDATE credits 
            SET balance = balance - %s 
            WHERE username = %s AND balance >= %s
            RETURNING balance;
        """, (cost, username, cost))
        
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if row:
            return row[0] # Returns new balance
        else:
            return None # Insufficient funds
            
    except Exception as e:
        print(f"Billing Error: {e}")
        raise e

# --- Logic Functions ---
def call_service(url, operation, a, b):
    try:
        resp = requests.post(f"{url}/{operation}", json={"a": float(a), "b": float(b)}, timeout=5)
        if resp.status_code == 200:
            return resp.json()['result']
        raise Exception(resp.json().get('error', 'Unknown error'))
    except Exception as e:
        raise Exception(f"Service call failed: {str(e)}")

def solve_expression(tokens):
    cost = 0
    # 1. Multiply/Divide
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/'):
            op = 'multiply' if tokens[i] == '*' else 'divide'
            val1 = tokens[i-1]; val2 = tokens[i+1]
            result = call_service(MULTI_SERVICE_URL, op, val1, val2)
            tokens[i-1] = result
            del tokens[i:i+2]
            i -= 1 
            cost += 3 # Expensive operation
        else:
            i += 1
            
    # 2. Add/Subtract
    i = 0
    while i < len(tokens):
        if tokens[i] in ('+', '-'):
            op = 'add' if tokens[i] == '+' else 'subtract'
            val1 = tokens[i-1]; val2 = tokens[i+1]
            result = call_service(ADD_SERVICE_URL, op, val1, val2)
            tokens[i-1] = result
            del tokens[i:i+2]
            i -= 1
            cost += 1 # Cheap operation
        else:
            i += 1
            
    return tokens[0], cost

@app.route('/calculate', methods=['POST'])
def calculate():
    # --- ARTIFICIAL DELAY FOR SCALING DEMO ---
    time.sleep(0.5)
    # -----------------------------------------

    data = request.json
    expr = data.get('expression', '')
    username = data.get('username', 'guest')
    
    try:
        # Basic Parsing
        expr = expr.replace(" ", "")
        tokens = re.split(r'(\+|\-|\*|/)', expr)
        tokens = [t for t in tokens if t]
        
        # 1. Compute Result
        final_result, total_cost = solve_expression(tokens)
        
        # 2. Process Billing
        new_balance = process_billing(username, total_cost)
        
        if new_balance is None:
            return jsonify({
                "error": "Insufficient Credit! Please recharge.",
                "cost": total_cost
            }), 402 # Payment Required
            
        return jsonify({
            "result": final_result,
            "cost": total_cost,
            "balance": new_balance,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)