# 🐳☸️ Dockerfile & Kubernetes Manifests — Setup Stage

This stage adds the **Dockerfile** and **Kubernetes manifests** required to containerise and deploy the **Flask application** for the **MLOps Machine Maintenance** project.
It focuses on **setting up** the container and Kubernetes configuration — preparing the groundwork for deployment, without yet deploying or integrating CI/CD.

## 🧩 Overview

At this stage, the project gains:

| Component                        | Purpose                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| 🐳 **Dockerfile**                | Defines how to build and run the Flask app as a container            |
| ☸️ **manifests/deployment.yaml** | Describes the Kubernetes Deployment (pods, replicas, container spec) |
| 🌐 **manifests/service.yaml**    | Exposes the Flask app through a LoadBalancer for external access     |

These files make the application portable, reproducible, and ready for cloud or local Kubernetes clusters (e.g., Minikube, GKE, or Docker Desktop).

## ⚙️ **Dockerfile Summary**

The `Dockerfile` creates a lightweight Python 3.12 container that:

1. Copies all project files into `/app`
2. Installs dependencies in editable mode (`pip install -e .`)
3. Exposes port **5000**
4. Launches the Flask app using `CMD ["python", "app.py"]`

### Example Build & Run (Local)

```bash
# Build container
docker build -t mlops-machine-maintenance:latest .

# Run locally
docker run -p 5000:5000 mlops-machine-maintenance:latest
```

Then open **[http://localhost:5000](http://localhost:5000)** in your browser.

## ☸️ **Kubernetes Manifests Summary**

The `manifests/` folder contains two YAML files that define how the Flask container is deployed and accessed within Kubernetes.

### `deployment.yaml`

Creates a **Deployment** named `mlops-machine-maintenance`:

* Runs **2 replicas** for basic availability
* Uses the image from:

  ```
  us-central1-docker.pkg.dev/sacred-garden-474511-b9/mlops-machine-maintenance/mlops-machine-maintenance:latest
  ```
* Exposes container port **5000**
* Requests minimal resources (`250m` CPU, `256Mi` memory)

### `service.yaml`

Defines a **Service** named `mlops-service`:

* Selects pods with `app: mlops-machine-maintenance`
* Type: **LoadBalancer**
* Maps external port **80** to internal port **5000**

### Apply the Manifests

```bash
kubectl apply -f manifests/
```

Then verify:

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

If no external IP is available, use:

```bash
kubectl port-forward svc/mlops-service 8080:80
```

Access the app at **[http://localhost:8080](http://localhost:8080)**

## 🗂️ **Updated Project Structure**

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

## ✅ **Expected Outcome**

After this stage:

* The **Dockerfile** correctly builds and runs the Flask app in a container.
* The **Kubernetes manifests** define a consistent, deployable setup.
* The project is now **deployment-ready**, with infrastructure configuration stored under `manifests/`.

## 🔎 Notes

* This stage focuses solely on **setting up** the containerisation and Kubernetes configuration — no CI/CD or deployment automation is included yet.
* You can later expand this to integrate with **GitHub Actions**, **GKE**, or **Kubeflow** for full production automation. 
