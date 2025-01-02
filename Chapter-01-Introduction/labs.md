 Chapter 1: Hands-on Labs

 Lab 1: Setting Up Your First Kubernetes Environment
 

 Objective
Set up a local Kubernetes development environment using Minikube and perform basic operations.

 Prerequisites
- Computer with at least 2 CPUs and 2GB RAM
- Administrative access
- Internet connection

 Steps

 1. Install Required Tools
```bash
 Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

 Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

 Verify installations
kubectl version --client
minikube version
```

 2. Start Minikube Cluster
```bash
 Start with default configuration
minikube start

 Alternative: Start with specific resources
minikube start --cpus=2 --memory=2048mb --disk-size=20gb

 Verify cluster status
kubectl cluster-info
kubectl get nodes
```

 3. Explore Basic kubectl Commands
```bash
 View cluster nodes
kubectl get nodes -o wide

 View cluster namespaces
kubectl get namespaces

 View all pods in all namespaces
kubectl get pods --all-namespaces

 View cluster events
kubectl get events
```

 Verification
- Minikube status shows "Running"
- kubectl can connect to the cluster
- Node is in "Ready" state

 Lab 2: Basic Kubernetes Operations

 Objective
Learn fundamental Kubernetes operations using kubectl commands.

 Steps

 1. Create and Manage Pods
```bash
 Create a pod running nginx
kubectl run nginx-pod --image=nginx

 View pod details
kubectl get pod nginx-pod
kubectl describe pod nginx-pod

 Access pod logs
kubectl logs nginx-pod

 Execute command in pod
kubectl exec -it nginx-pod -- /bin/bash

 Delete pod
kubectl delete pod nginx-pod
```

 2. Working with Deployments
```bash
 Create a deployment
kubectl create deployment web-app --image=nginx --replicas=3

 View deployments
kubectl get deployments
kubectl describe deployment web-app

 Scale deployment
kubectl scale deployment web-app --replicas=5

 Delete deployment
kubectl delete deployment web-app
```

 3. Service Exposure
```bash
 Create a deployment
kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4

 Expose deployment as a service
kubectl expose deployment hello-node --type=NodePort --port=8080

 Get service information
kubectl get services
minikube service hello-node --url
```

 Verification Tasks
1. Verify pod creation and status
2. Check deployment scaling
3. Access exposed service
4. View application logs

 Lab 3: Namespace and Resource Management

 Objective
Learn to work with namespaces and manage resources within them.

 Steps

 1. Create and Manage Namespaces
```bash
 Create namespace
kubectl create namespace development

 View namespaces
kubectl get namespaces

 Set context to new namespace
kubectl config set-context --current --namespace=development
```

 2. Resource Creation in Namespace
```bash
 Create pod in namespace
kubectl run nginx --image=nginx -n development

 Create deployment in namespace
kubectl create deployment web --image=nginx -n development

 View resources in namespace
kubectl get all -n development
```

 3. Resource Quotas
```bash
 Create resource quota
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: development
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "6"
    limits.memory: 8Gi
EOF

 View quota
kubectl describe quota -n development
```

 Verification Tasks
1. Check namespace creation
2. Verify resource creation in correct namespace
3. Confirm resource quota enforcement

 Lab 4: Basic Troubleshooting

 Objective
Learn basic troubleshooting techniques for Kubernetes environments.

 Steps

 1. Checking Cluster Health
```bash
 Check node status
kubectl get nodes
kubectl describe nodes

 Check system pods
kubectl get pods -n kube-system
```

 2. Pod Troubleshooting
```bash
 Create a problematic pod
kubectl run problem-pod --image=nginx:invalid

 Check pod status
kubectl get pod problem-pod
kubectl describe pod problem-pod
kubectl logs problem-pod
```

 3. Service Debugging
```bash
 Check service endpoints
kubectl get endpoints

 Test service connectivity
kubectl run test-pod --image=busybox -- sleep 3600
kubectl exec -it test-pod -- wget -qO- http://service-name
```

 Verification Tasks
1. Identify issues in problem pod
2. Verify service connectivity
3. Check system components

 Additional Exercises

 Exercise 1: Pod Creation and Management
- Create pods with different images
- Use port forwarding to access applications
- Practice pod deletion and recreation

 Exercise 2: Deployment Manipulation
- Create deployments with various configurations
- Perform rolling updates
- Practice rollback operations

 Exercise 3: Service Creation
- Create different types of services
- Test service access
- Practice service deletion and recreation

 Clean Up Instructions
```bash
 Delete all resources in current namespace
kubectl delete all --all

 Stop Minikube cluster
minikube stop

 Optional: Delete Minikube cluster
minikube delete
```

 Troubleshooting Guide
- Common issues and solutions
- Command reference
- Resource verification steps