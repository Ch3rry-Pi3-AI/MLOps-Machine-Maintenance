# 🏭 **MLOps Machine Maintenance — End-to-End CI/CD Automation Project**

This repository presents a **complete MLOps workflow** designed to predict when industrial machines may require maintenance or repair.
By combining **machine learning**, **containerisation**, **orchestration**, and **automation**, it delivers a **production-ready system** that continuously integrates, trains, and deploys updates — automatically.

<p align="center">
  <img src="img/flask/flask_app.png" alt="Flask Application Interface — MLOps Machine Maintenance" width="100%">
</p>



## 🌸 **Project Overview**

This project unifies the **Machine Learning lifecycle** with **MLOps automation**, demonstrating how to build, train, containerise, deploy, and maintain a model in a **scalable, reproducible, and cloud-deployed environment**.
The application estimates the **likelihood of machine efficiency issues** based on operational parameters, providing insights into **when maintenance is likely needed**.

Key technologies include **Python**, **Flask**, **Docker**, **Kubernetes (Minikube)**, **Google Cloud Platform (GCP)**, **Jenkins**, **ArgoCD**, and **GitHub Webhooks**.



## ⚙️ **Workflow Summary**

This project followed a structured 13-stage development lifecycle, each step building upon the last to achieve a seamless CI/CD automation pipeline.

### **00 — Project Setup**

Created the foundational project structure, virtual environment, and configuration files for reproducibility.

### **01 — Data Processing**

Prepared the raw machine sensor data, including cleaning, encoding, feature scaling, and splitting into train/test sets.

### **02 — Model Training**

Developed and evaluated a **Logistic Regression model** to predict machine maintenance likelihood, saving artefacts to disk.

### **03 — Training Pipeline**

Integrated preprocessing and model training into one **automated workflow script (`training_pipeline.py`)**, enabling full pipeline execution with a single command.

### **04 — Flask Application**

Built a **Flask web interface** that allows users to input machine parameters and receive maintenance predictions in real time.

### **05 — Docker and Kubernetes Manifests**

Created a **Dockerfile** to containerise the Flask app and developed **Kubernetes manifests** (`deployment.yaml` and `service.yaml`) for scalable deployment and public exposure.

### **06 — Google Cloud Platform Setup**

Provisioned a **GCP Virtual Machine** instance to host the entire workflow.
Configured the instance for **Docker installation** and VM networking.

### **07 — Minikube Installation and Setup**

Installed and configured **Minikube** within the VM to simulate a local Kubernetes cluster.
Deployed the containerised application for initial end-to-end testing.

### **08 — Jenkins Installation (Docker-in-Docker)**

Deployed **Jenkins** in a Docker container using a Docker-in-Docker (DinD) approach, ensuring CI/CD orchestration could build, push, and deploy containers dynamically.

### **09 — GitHub Integration with Jenkins**

Connected **Jenkins** to the GitHub repository using **personal access tokens**, allowing Jenkins to fetch source code directly from GitHub.

### **10 — Build and Push Docker Image**

Configured the Jenkins pipeline to:

1. Build Docker images from the source code.
2. Push images to a **DockerHub repository** using stored credentials.

This completed the **Continuous Integration (CI)** stage.

### **11 — Continuous Deployment with ArgoCD**

Installed and configured **ArgoCD** to handle Continuous Deployment (CD).
The Jenkins pipeline triggered ArgoCD to sync GitHub code changes with the Kubernetes cluster, deploying the latest image automatically.

### **12 — Webhooks Integration**

Introduced **GitHub Webhooks** to automate pipeline execution.
Now, whenever code is pushed to GitHub, Jenkins automatically triggers the pipeline, builds the Docker image, updates ArgoCD, and redeploys the application — achieving **true automation**.

### **13 — Final Automation**

At this stage, the project became fully operational:
A single **GitHub push** cascades through Jenkins, Docker, Kubernetes, and ArgoCD — updating the live Flask application automatically.



## 🧠 **Key Features**

* **End-to-End Automation** — Complete CI/CD workflow from data ingestion to live deployment.
* **Containerised ML Pipeline** — Ensures consistency across environments.
* **Kubernetes Orchestration** — Provides scalability and reliability.
* **GitOps with ArgoCD** — Automates syncing between GitHub and cluster state.
* **Webhook-Driven Triggers** — Eliminates manual builds; pipelines run on every push.
* **Cloud-Hosted Architecture** — Fully hosted on a Google Cloud VM instance.



## 🗂️ **Final Project Structure**

```text
mlops_machine_maintenance/
├── .venv/                            # 🧩 Local virtual environment
├── artifacts/
│   ├── raw/
│   │   └── data.csv                  # ⚙️ Raw machine sensor dataset
│   ├── processed/                    # 💾 Processed data and scaler
│   │   ├── X_train.pkl
│   │   ├── X_test.pkl
│   │   ├── y_train.pkl
│   │   ├── y_test.pkl
│   │   └── scaler.pkl
│   └── models/                       # 🧠 Trained model artefacts
│       └── model.pkl
├── manifests/                        # ☸️ Kubernetes configuration files
│   ├── deployment.yaml               # Defines pods, replicas, and container spec
│   └── service.yaml                  # LoadBalancer service exposing the app
├── pipeline/                         # ⚙️ Workflow orchestration
│   └── training_pipeline.py          # End-to-end data processing + model training
├── src/                              # 🧠 Core Python modules
│   ├── __init__.py
│   ├── custom_exception.py           # Unified error handling
│   ├── logger.py                     # Centralised logging configuration
│   ├── data_processing.py            # Preprocessing and scaling
│   └── model_training.py             # Model training and evaluation
├── static/                           # 🌈 Front-end styling and assets
│   ├── style.css
│   └── img/
├── templates/                        # 🧩 HTML templates for Flask
│   └── index.html
├── img/
│   └── flask/
├── app.py                            # 🌐 Flask app for prediction interface
├── Dockerfile                        # 🐳 Container build file
├── .gitignore                        # 🚫 Ignore rules for Git
├── .python-version                   # 🐍 Python version pin
├── pyproject.toml                    # ⚙️ Project metadata
├── requirements.txt                  # 📦 Python dependencies
├── setup.py                          # 🔧 Editable install support
└── uv.lock                           # 🔒 Locked dependency versions
```



## ✅ **Conclusion**

This project demonstrates how to operationalise a **machine learning model** using **real-world MLOps practices** — transforming it from a local experiment into a **cloud-deployed, continuously updated system**.

Through the integration of **GitHub**, **Jenkins**, **Docker**, **Kubernetes**, **ArgoCD**, and **Webhooks**, the pipeline now achieves **true continuous delivery**:
every code push automatically rebuilds, redeploys, and synchronises the live application.

This marks the completion of the **MLOps Machine Maintenance** project — a full demonstration of data science meeting production engineering.