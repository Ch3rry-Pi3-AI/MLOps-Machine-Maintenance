# ☸️ **Minikube Installation and Setup on GCP VM Instance**

This section guides you through installing and configuring **Minikube** and **kubectl** on your **Google Cloud Platform (GCP) virtual machine instance**.
After completing these steps, you will have a fully functional **local Kubernetes cluster** running inside your GCP VM.

## 🧩 **1️⃣ Access the Minikube Documentation**

Go to the official Minikube installation guide:
👉 [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)

Scroll down to the **Installation** section and select **Linux**.

You will see the following commands for installing Minikube on Linux.

## ⚙️ **2️⃣ Install Minikube**

Copy and paste the following commands into your **VM instance terminal**:

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

If the installation is successful, the terminal will show output similar to:

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  133M  100  133M    0     0   160M      0 --:--:-- --:--:-- --:--:--  160M
```

This confirms that **Minikube** was successfully downloaded and installed.

## 🚀 **3️⃣ Start Minikube**

Run the following command to start Minikube:

```bash
minikube start
```

Expected output:

```bash
😄  minikube v1.37.0 on Ubuntu 24.04 (amd64)
✨  Automatically selected the docker driver. Other choices: ssh, none
📌  Using Docker driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.48 ...
💾  Downloading Kubernetes v1.34.0 preload ...
    > preloaded-images-k8s-v18-v1...:  337.07 MiB / 337.07 MiB  100.00% 203.01 
    > gcr.io/k8s-minikube/kicbase...:  488.50 MiB / 488.52 MiB  100.00% 114.26 
🔥  Creating docker container (CPUs=2, Memory=3900MB) ...
🐳  Preparing Kubernetes v1.34.0 on Docker 28.4.0 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
💡  kubectl not found. If you need it, try: 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

This confirms that Minikube is running successfully on your GCP VM.

## 🧠 **4️⃣ Install kubectl**

Next, you’ll install `kubectl`, the Kubernetes command-line tool used to interact with your cluster.

Visit the official installation page:
👉 [https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

Under the **Install kubectl on Linux** section, copy and run the first command:

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Now install `kubectl` using **snap**:

```bash
sudo snap install kubectl --classic
```

You should see:

```bash
kubectl 1.34.1 from Canonical✓ installed
```

Verify the installation:

```bash
kubectl version --client
```

Expected output:

```bash
Client Version: v1.34.1
Kustomize Version: v5.7.1
```

This confirms that **kubectl** has been successfully installed.

## 🧩 **5️⃣ Verify Minikube and kubectl Setup**

Check the Minikube cluster status:

```bash
minikube status
```

Expected output:

```bash
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

List the active nodes in your cluster:

```bash
kubectl get nodes
```

Expected output:

```bash
Kubernetes control plane is running at https://192.168.49.2:8443
CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

Finally, check Docker to confirm that Minikube is running as a container:

```bash
docker ps
```

You should see an active Minikube container in the list.

## ✅ **6️⃣ Summary**

You have successfully:

1. Installed **Minikube** on your GCP virtual machine
2. Installed **kubectl** for managing Kubernetes resources
3. Verified that Minikube and Docker are running correctly

Your GCP VM is now set up as a **local Kubernetes environment**, ready to deploy and test the **MLOps Machine Maintenance** application within containers.
