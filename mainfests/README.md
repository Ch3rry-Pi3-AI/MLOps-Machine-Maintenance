# `manifests/` README — Kubernetes Deployment for the Flask App

This folder contains the **Kubernetes configuration** to run the **MLOps Machine Maintenance** Flask application on a cluster. It includes a **Deployment** that runs your containerised app and a **Service** that exposes it to users.

## 📁 Folder Overview

```text
manifests/
├── deployment.yaml   # App pods, container image, resources, pod labels
└── service.yaml      # Public-facing Service (LoadBalancer) on port 80 → container 5000
```

## 🚀 What These Manifests Do

### `deployment.yaml`

Creates a ReplicaSet with **2 pods** running the image:

```
us-central1-docker.pkg.dev/sacred-garden-474511-b9/mlops-machine-maintenance/mlops-machine-maintenance:latest
```

Key points:

* **replicas: 2** for basic high availability
* **label** `app: mlops-machine-maintenance` used by the Service to target pods
* **containerPort: 5000** matches your Flask app
* **resource requests** ensure scheduler placement: `cpu: 250m`, `memory: 256Mi`
* **imagePullPolicy: Always** pulls the latest `:latest` tag on each rollout

### `service.yaml`

Creates a public **LoadBalancer**:

* **port 80** externally routes to **targetPort 5000** in the pods
* Uses selector `app: mlops-machine-maintenance` to route traffic to the Deployment’s pods

On cloud providers like GKE, AKS, or EKS, the LoadBalancer will allocate a public IP for you.

## 🧩 How to Deploy

From the repo root (where `manifests/` lives):

```bash
# 1) Create or select a namespace (optional but recommended)
kubectl create namespace mlops || true
kubectl config set-context --current --namespace=mlops

# 2) Apply all manifests
kubectl apply -f manifests/

# 3) Verify rollout
kubectl rollout status deployment/mlops-machine-maintenance

# 4) Check Service and get external IP (cloud clusters)
kubectl get svc mlops-service -o wide
```

If you don’t get an external IP (e.g., on Minikube or kind), you can port-forward for local testing:

```bash
kubectl port-forward svc/mlops-service 8080:80
# Visit http://localhost:8080
```

## 🧪 Quick Health Checks

Useful commands while debugging:

```bash
kubectl get pods -o wide
kubectl logs deploy/mlops-machine-maintenance
kubectl describe deploy/mlops-machine-maintenance
kubectl describe svc/mlops-service
```

## 🔐 Pulling from Artifact Registry

If your registry requires auth, configure an image pull secret and reference it in the Deployment:

```bash
kubectl create secret docker-registry gar-pull \
  --docker-server=us-central1-docker.pkg.dev \
  --docker-username=_json_key \
  --docker-password="$(cat key.json)" \
  --docker-email=you@example.com

# Then add under spec.template.spec:
# imagePullSecrets:
# - name: gar-pull
```

## ✅ Suggested Production Enhancements

These are safe, incremental improvements you can add:

1. **Set resource limits**

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

2. **Add probes** so Kubernetes knows when the app is healthy and ready

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 20
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 5
```

3. **Pin image versions** instead of `:latest` for reproducible rollouts
   Example: `...:v0.1.3`

4. **Environment variables and config**
   Use a ConfigMap/Secret for non-code configuration (e.g., feature flags, API keys), and mount or inject them via `env`.

5. **Autoscaling**
   Horizontal Pod Autoscaler (HPA) to scale based on CPU/Memory:

```bash
kubectl autoscale deployment mlops-machine-maintenance --cpu-percent=70 --min=2 --max=6
```

## 🧱 Rollback and Updates

```bash
# Update images
kubectl set image deployment/mlops-machine-maintenance mlops-machine-maintenance=REGISTRY/IMAGE:TAG

# Check rollout
kubectl rollout status deployment/mlops-machine-maintenance

# Rollback if needed
kubectl rollout undo deployment/mlops-machine-maintenance
```

## 📌 Notes

* Ensure the **container port (5000)** matches your Flask app and Dockerfile.
* The **Service** publishes port **80** externally to meet common HTTP expectations.
* For private registries, configure **imagePullSecrets** as shown above.

With these manifests, your Flask-based **MLOps Machine Maintenance** app is ready to run behind a managed load balancer on your Kubernetes cluster.
