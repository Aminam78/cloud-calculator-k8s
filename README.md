# ☁️ Cloud Calculator (Microservices on Kubernetes)

A distributed, microservices-based calculator application designed to perform mathematical operations in a cloud environment. This project demonstrates the implementation of a distributed system using **Docker**, **Kubernetes (Minikube)**, and **Python (Flask)**.

## 🎓 Academic Context
This project was developed as the final assignment for the **Distributed Systems** course.

* **University:** Iran University of Science and Technology (IUST)
* **Degree:** M.Sc. in Computer Software Engineering
* **Student:** Amirhossein Amin Moghadam ([@Aminam78](https://github.com/Aminam78))

---

## 🏗 Architecture
The application is decomposed into independent microservices to ensure scalability, maintainability, and fault isolation:

1.  **Frontend Service (UI):**
    * A web-based interface built with **Flask** (Python) + HTML/CSS.
    * Acts as a Gateway/Reverse Proxy.
    * Accepts user input and communicates with the Backend service via HTTP requests.
    * Exposed to the outside world via a **NodePort** Service.

2.  **Backend Service (Compute):**
    * An API-based service built with **Flask** (Python).
    * Performs the actual mathematical calculations.
    * Internal service, not exposed directly to the public internet (ClusterIP).

3.  **Database (Redis) & Scaling:** *(Planned/Bonus Features)*
    * **Redis:** For persisting calculation history.
    * **HPA:** Horizontal Pod Autoscaling for handling high traffic loads.

---

## 🛠 Tech Stack

* **Language:** Python 3.9
* **Framework:** Flask
* **Containerization:** Docker
* **Orchestration:** Kubernetes (Minikube)
* **Registry:** Docker Hub
* **Version Control:** Git & GitHub

---

## 📂 Project Structure
```
cloud-calculator/
├── backend/                # Calculation Microservice
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # User Interface Microservice
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── static/             # CSS files
│   └── templates/          # HTML files
├── k8s/                    # Kubernetes Manifests
│   ├── backend.yaml        # Deployment & Service for Backend
│   └── frontend.yaml       # Deployment & Service for Frontend
└── README.md
```


## 🚀 Deployment

### Prerequisites

- [Docker](https://www.docker.com/)
    
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
    
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
    

### Steps to Run

1. **Start Minikube:**
    
 
    
    ```Bash
    minikube start
    ```
    
2. **Apply Kubernetes Manifests:**
    
    Navigate to the project root and run:
    ```Bash
    kubectl apply -f k8s/backend.yaml
    kubectl apply -f k8s/frontend.yaml
    ```
    
3. **Check Status:**
    
    Ensure all pods are running:
    
    ```Bash
    kubectl get pods
    kubectl get svc
    ```
    
4. **Access the Application:**
    
    Since the frontend is exposed via NodePort, use Minikube to get the URL:
    
    ```Bash
    minikube service frontend-svc
    ```
    

---

## 📬 Contact

Created by **Amirhossein Amin Moghaddam**.

Feel free to reach out for any questions regarding the implementation details.

- **GitHub:** [Aminam78](https://github.com/Aminam78)
    
- **University:** [IUST](http://www.iust.ac.ir/)