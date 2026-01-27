from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# K8s Service Discovery Configuration
# This ENV variable will be injected by Kubernetes Deployment later.
# Default is localhost for local testing.
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    expression = ""
    error = None
    
    if request.method == 'POST':
        expression = request.form.get('expression')
        try:
            # Send request to the Backend Microservice
            # We use the internal K8s DNS name provided in BACKEND_URL
            response = requests.post(f"{BACKEND_URL}/calculate", json={"expression": expression}, timeout=5)
            data = response.json()
            
            if response.status_code == 200 and data.get('status') == 'success':
                result = data['result']
            else:
                error = data.get('error', 'Unknown error form backend')
                
        except requests.exceptions.ConnectionError:
            error = f"Could not connect to backend service at {BACKEND_URL}"
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            
    return render_template('index.html', result=result, expression=expression, error=error)

if __name__ == '__main__':
    # Frontend runs on port 8080 to avoid conflict if running locally
    app.run(host='0.0.0.0', port=8080)