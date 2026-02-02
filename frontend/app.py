from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Orchestrator URL
ORCHESTRATOR_URL = os.getenv('ORCHESTRATOR_URL', 'http://localhost:5000')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = ""
    error = None
    balance = None
    cost = None
    
    if request.method == 'POST':
        expression = request.form.get('expression')
        username = request.form.get('username') # Get username
        
        try:
            # Send username and expression to Orchestrator
            response = requests.post(f"{ORCHESTRATOR_URL}/calculate", 
                                   json={"expression": expression, "username": username}, 
                                   timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                result = data.get('result')
                balance = data.get('balance') # Get balance info
                cost = data.get('cost')
            elif response.status_code == 402: # Insufficient funds
                error = data.get('error')
            else:
                error = data.get('error', 'Unknown error')
                
        except Exception as e:
            error = f"Connection Error: {str(e)}"
            
    return render_template('index.html', result=result, expression=expression, error=error, balance=balance, cost=cost)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)