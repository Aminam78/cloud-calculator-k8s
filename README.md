# ☁️ Cloud Calculator (Microservices on Kubernetes)

A distributed, cloud-native calculator application designed with **Microservices Architecture** and deployed on **Kubernetes**. This project demonstrates advanced concepts such as Service Discovery, Layer 7 Routing (Ingress), Stateful Sets (Database), and Orchestration.

## 🎓 Academic Context
This project was developed as the final assignment for the **Distributed Systems** course.

* **University:** Iran University of Science and Technology (IUST)
* **Degree:** M.Sc. in Computer Software Engineering
* **Student:** Amirhossein Amin Moghaddam ([@Aminam78](https://github.com/Aminam78))

---

## 🏗 Architecture

The application is decomposed into **4 stateless microservices** and **1 stateful database**, communicating via REST APIs:

1.  **Frontend Service (UI):**
    * Serves the Web UI (Flask + HTML/CSS).
    * Acts as the entry point for users via **Ingress**.
    * Forwards user requests to the Orchestrator.

2.  **Orchestrator Service (The Brain):**
    * Parses the mathematical expression.
    * Manages business logic and billing.
    * Delegates tasks to worker services.
    * Connects to **PostgreSQL** to manage user credits.

3.  **Worker Services (Primitives):**
    * **Add-Service:** Handles Addition (`+`) and Subtraction (`-`).
    * **Multi-Service:** Handles Multiplication (`*`) and Division (`/`).

4.  **Database (Persistence):**
    * **PostgreSQL** deployed via **Helm**.
    * Stores user credits and transaction history.
    * Uses **PersistentVolume (PV)** for data durability.

### 🧩 System Diagram

```mermaid
graph TD
    User((User)) -->|HTTP/Host: calculator.local| Ingress[NGINX Ingress]
    Ingress -->|Route /| Frontend[Frontend SVC]
    
    subgraph "Kubernetes Cluster"
        Frontend -->|POST /calculate| Orch[Orchestrator SVC]
        
        Orch -->|Logic| Add[Add SVC]
        Orch -->|Logic| Multi[Multi SVC]
        Orch -->|Billing| DB[(PostgreSQL)]
    end
 ```   
🛠 Tech Stack
Language: Python 3.9 (Flask)

Containerization: Docker

Orchestration: Kubernetes (Minikube)

Networking: NGINX Ingress Controller, ClusterIP

Database: PostgreSQL (Bitnami Helm Chart)

Package Manager: Helm

Version Control: Git & GitHub

📂 Project Structure
‍‍```‍‍‍‍‍Plaintext
cloud-calculator/
├── backend/
│   ├── orchestrator/       # Logic & DB interaction
│   ├── add_service/        # Worker (+ -)
│   └── multi_service/      # Worker (* /)
├── frontend/               # UI Service
├── k8s/                    # Kubernetes Manifests
│   ├── *-deployment.yaml   # Deployments with Resource Limits
│   ├── *-service.yaml      # ClusterIP Services
│   └── ingress.yaml        # Ingress Rules
└── README.md
```

🚀 Deployment Guide
Prerequisites:
Docker

Minikube

Kubectl

Helm

Step 1: Bootstrap Cluster & Addons

```Bash
minikube start -p distributed-systems
minikube addons enable ingress -p distributed-systems
```
Step 2: Deploy Database (PostgreSQL)
We use Helm to deploy a production-ready database.

```Bash
helm repo add bitnami [https://charts.bitnami.com/bitnami](https://charts.bitnami.com/bitnami)
helm install my-postgres bitnami/postgresql \
  --set persistence.enabled=true \
  --set persistence.size=2Gi \
  --set global.postgresql.auth.postgresPassword=password123
```
Step 3: Deploy Microservices
Apply all Kubernetes manifests (Deployments, Services, Ingress):

```Bash
kubectl apply -f k8s/
Step 4: Network Setup (Ingress)
Start the tunnel to assign an IP to Ingress:
```

```Bash
minikube tunnel -p distributed-systems
Add the domain to your hosts file (/etc/hosts or C:\Windows\System32\drivers\etc\hosts):
```

```Plaintext
127.0.0.1  calculator.local
```
Step 5: Usage
Open your browser and navigate to: http://calculator.local

📬 Contact
Created by Amirhossein Amin Moghadam.

GitHub: Aminam78