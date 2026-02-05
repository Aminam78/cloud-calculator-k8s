# **☁️ Cloud Calculator (Microservices on Kubernetes)**

A distributed, cloud-native calculator application designed with **Microservices Architecture** and deployed on **Kubernetes**. This project demonstrates advanced concepts such as Service Discovery, Layer 7 Routing (Ingress), Stateful Sets (Database), and Orchestration.

## **🎓 Academic Context**

This project was developed as the final assignment for the **Distributed Systems** course.

* **University:** Iran University of Science and Technology (IUST)  
* **Degree:** M.Sc. in Computer Software Engineering  
* **Student:** Amirhossein Amin Moghaddam ([@Aminam78](https://github.com/Aminam78))

## **🏗 Architecture**

The application is decomposed into **4 stateless microservices** and **1 stateful database**, communicating via REST APIs:

1. **Frontend Service (UI):**  
   * Serves the Web UI (Flask \+ HTML/CSS).  
   * Acts as the entry point for users via **Ingress**.  
   * Forwards user requests to the Orchestrator.  
2. **Orchestrator Service (The Brain):**  
   * Parses the mathematical expression.  
   * Manages business logic and billing.  
   * Delegates tasks to worker services.  
   * Connects to **PostgreSQL** to manage user credits.  
3. **Worker Services (Primitives):**  
   * **Add-Service:** Handles Addition (+) and Subtraction (-).  
   * **Multi-Service:** Handles Multiplication (\*) and Division (/).  
4. **Database (Persistence):**  
   * **PostgreSQL** deployed via **Helm**.  
   * Stores user credits and transaction history.  
   * Uses **PersistentVolume (PV)** for data durability.

### **🧩 System Diagram**

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

## **🛠 Tech Stack**

* **Language:** Python 3.9 (Flask)  
* **Containerization:** Docker  
* **Orchestration:** Kubernetes (Minikube)  
* **Networking:** NGINX Ingress Controller, ClusterIP  
* **Database:** PostgreSQL (Bitnami Helm Chart)  
* **Package Manager:** Helm  
* **Version Control:** Git & GitHub

## **📂 Project Structure**

cloud-calculator/  
├── backend/  
│   ├── orchestrator/       \# Logic & DB interaction  
│   ├── add\_service/        \# Worker (+ \-)  
│   └── multi\_service/      \# Worker (\* /)  
├── frontend/               \# UI Service  
├── k8s/                    \# Kubernetes Manifests  
│   ├── \*-deployment.yaml   \# Deployments with Resource Limits  
│   ├── \*-service.yaml      \# ClusterIP Services  
│   └── ingress.yaml        \# Ingress Rules  
└── README.md

## **🚀 Deployment Guide**

### **Prerequisites**

* [Docker](https://www.docker.com/)  
* [Minikube](https://minikube.sigs.k8s.io/docs/start/)  
* [Kubectl](https://kubernetes.io/docs/tasks/tools/)  
* [Helm](https://helm.sh/)

### **Step 1: Bootstrap Cluster & Addons**
```bash
minikube startminikube start \-p distributed-systems  
minikube addons enable ingress \-p distributed-systems
```

### **Step 2: Deploy Database (PostgreSQL)**

We use Helm to deploy a production-ready database.
```bash
helm repo add bitnami [https://charts.bitnami.com/bitnami](https://charts.bitnami.com/bitnami)
helm install my-postgres bitnami/postgresql \
  --set persistence.enabled=true \
  --set persistence.size=2Gi \
  --set global.postgresql.auth.postgresPassword=password123 \
  --set volumePermissions.enabled=true
```

### **Step 3: Deploy Microservices**

Apply all Kubernetes manifests (Deployments, Services, Ingress):

```bash
kubectl apply \-f k8s/
```
### **Step 4: Access the Application (Port Forwarding)**

Due to network isolation in some environments (like WSL2), we use Port Forwarding to securely access the internal service from the host machine.

Run the following command in a separate terminal:

```bash
   # Forwards local port 8080 to the Frontend Service port 80
   kubectl port-forward service/frontend-svc 8080:80 --address 0.0.0.0
```

### **Step 5: Usage**

Open browser at: http://localhost:8080

Enter a username (e.g., admin).

Enter an expression.

See the result and updated balance.

## 📈 **Bonus Features Implemented**

### 1. Database & Billing (15%)

- Integrated **PostgreSQL** to store user credits.
    
- Implemented billing logic (deducting costs per operation).
    
- Data persistence ensured via PVC.

### 2. Horizontal Scaling Demo (15%)

We demonstrated the system's ability to handle increased load by scaling replicas.

Benchmark Script: final_benchmark.py sends 50 concurrent requests.

Scenario:

1 Replica: Low throughput, high latency (Bottleneck).

5 Replicas: High throughput, low latency (Parallel Processing).

- How to run the benchmark:

```bash
# 1. Ensure port-forward is running on port 8080
# 2. Run the script
python final_benchmark.py
```

## **📬 Contact**

Created by **Amirhossein Amin Moghaddam**.

* **GitHub:** [Aminam78](https://github.com/Aminam78)