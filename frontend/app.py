from flask import Flask, render_template, request
import requests
import os

# Flask automatically serves files from 'static' folder at /static endpoint
app = Flask(__name__)

# K8s Service Discovery Configuration
# Updated to point to the Orchestrator 
ORCHESTRATOR_URL = os.getenv('ORCHESTRATOR_URL', 'http://localhost:5000')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = ""
    error = None
    
    if request.method == 'POST':
        expression = request.form.get('expression')
        try:
            # Send request to the Orchestrator Microservice
            response = requests.post(f"{ORCHESTRATOR_URL}/calculate", json={"expression": expression}, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                result = data.get('result')
            else:
                error = data.get('error', 'Unknown error from orchestrator')
                
        except requests.exceptions.ConnectionError:
            error = f"Could not connect to Orchestrator service at {ORCHESTRATOR_URL}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            
    return render_template('index.html', result=result, expression=expression, error=error)

if __name__ == '__main__':
    # Frontend runs on port 8080
    app.run(host='0.0.0.0', port=8080)