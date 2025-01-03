# Chapter 3: Cluster Setup and Configuration - Hands-on Labs

## Lab 1: Setting Up a Multi-Node Kubernetes Cluster
![Setting Up a Multi-Node Kubernetes Cluster](/Images/chapter03/ch03_lab01_cluster_setup.png)
### Objective
Set up a production-grade Kubernetes cluster with one control plane and two worker nodes using kubeadm.

### Prerequisites
- Three Ubuntu 20.04 servers
- Minimum 2 CPU and 2GB RAM per node
- Root access to all servers
- Network connectivity between nodes

### Steps

#### 1.1 Prepare All Nodes
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install container runtime (containerd)
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Configure system settings
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system

# Install containerd
sudo apt-get install -y containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd

# Install Kubernetes components
sudo apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

#### 1.2 Initialize Control Plane
```bash
# On control plane node only
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --control-plane-endpoint="LOAD_BALANCER_IP:6443" --upload-certs

# Save the join commands output for worker nodes

# Configure kubectl
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install network plugin (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

#### 1.3 Join Worker Nodes
```bash
# On worker nodes, use the join command from kubeadm init output
sudo kubeadm join LOAD_BALANCER_IP:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash>
```

### Verification
```bash
# Check node status
kubectl get nodes

# Verify system pods
kubectl get pods -n kube-system

# Test cluster functionality
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=NodePort
```

## Lab 2: Implementing High Availability
![Implementing High Availability](/Images/chapter03/ch03_lab02_ha_setup.png)
### Objective
Configure a highly available control plane with multiple master nodes.

### Steps

#### 2.1 Set Up Load Balancer
```bash
# Install HAProxy
sudo apt-get install -y haproxy

# Configure HAProxy
cat <<EOF | sudo tee /etc/haproxy/haproxy.cfg
frontend kubernetes
    bind *:6443
    mode tcp
    option tcplog
    default_backend kubernetes-master-nodes

backend kubernetes-master-nodes
    mode tcp
    balance roundrobin
    option tcp-check
    server master1 192.168.1.10:6443 check fall 3 rise 2
    server master2 192.168.1.11:6443 check fall 3 rise 2
    server master3 192.168.1.12:6443 check fall 3 rise 2
EOF

sudo systemctl restart haproxy
```

#### 2.2 Add Additional Control Plane Nodes
```bash
# On new control plane node
sudo kubeadm join LOAD_BALANCER_IP:6443 --token <token> \
    --discovery-token-ca-cert-hash sha256:<hash> \
    --control-plane --certificate-key <certificate-key>
```

## Lab 3: Storage Configuration
![Storage Configuration](/Images/chapter03/ch03_lab03_storage_config.png)
### Objective
Configure different storage solutions including local storage and dynamic provisioning.

### Steps

#### 3.1 Configure Local Storage
```bash
# Create storage class
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

# Create persistent volume
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - worker1
EOF
```

### Verification Tasks

1. Cluster Health Check
```bash
# Check node status
kubectl get nodes -o wide

# Verify control plane components
kubectl get pods -n kube-system

# Check etcd health
kubectl exec -n kube-system etcd-master1 -- etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health
```

2. Storage Verification
```bash
# Test PV/PVC binding
kubectl create -f test-pvc.yaml
kubectl get pv,pvc

# Verify pod can use storage
kubectl create -f test-pod.yaml
kubectl exec test-pod -- df -h
```

3. Network Verification
```bash
# Test pod-to-pod communication
kubectl run busybox1 --image=busybox -- sleep 3600
kubectl run busybox2 --image=busybox -- sleep 3600
kubectl exec busybox1 -- ping -c 4 busybox2.default.svc.cluster.local

# Test service resolution
kubectl exec busybox1 -- nslookup kubernetes.default
```

### Troubleshooting Guide

1. Node Issues
```bash
# Check kubelet status
systemctl status kubelet
journalctl -u kubelet

# Check certificates
kubeadm certs check-expiration
```

2. Network Issues
```bash
# Check CNI plugins
ls /etc/cni/net.d/
cat /etc/cni/net.d/10-calico.conflist

# Check pod networking
kubectl exec <pod-name> -- ip addr
```

3. Storage Issues
```bash
# Check PV/PVC status
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>

# Check storage provisioner
kubectl get sc
```
Advance Cluster Configuration Labs

## Lab 4: Advanced Cluster Configuration

### Objective
Configure advanced cluster features including custom schedulers, admission controllers, and resource management.

### Prerequisites
- Running Kubernetes cluster
- Administrative access
- kubectl configured

### 4.1 Custom Scheduler Implementation

#### Step 1: Create Custom Scheduler Configuration
```yaml
# custom-scheduler.yaml
apiVersion: v1
kind: Pod
metadata:
  name: custom-scheduler
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-scheduler
    - --address=127.0.0.1
    - --kubeconfig=/etc/kubernetes/scheduler.conf
    - --config=/etc/kubernetes/custom-scheduler-config.yaml
    image: k8s.gcr.io/kube-scheduler:v1.23.0
    name: custom-scheduler
    volumeMounts:
    - mountPath: /etc/kubernetes/scheduler.conf
      name: kubeconfig
    - mountPath: /etc/kubernetes/custom-scheduler-config.yaml
      name: scheduler-config
  volumes:
  - hostPath:
      path: /etc/kubernetes/scheduler.conf
      type: FileOrCreate
    name: kubeconfig
  - hostPath:
      path: /etc/kubernetes/custom-scheduler-config.yaml
      type: FileOrCreate
    name: scheduler-config
```

#### Step 2: Create Scheduler Configuration
```yaml
# custom-scheduler-config.yaml
apiVersion: kubescheduler.config.k8s.io/v1beta2
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: custom-scheduler
  plugins:
    score:
      disabled:
      - name: NodeResourcesLeastAllocated
      enabled:
      - name: NodeResourcesMostAllocated
        weight: 1
```

#### Step 3: Test Custom Scheduler
```yaml
# test-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: custom-scheduled-pod
spec:
  schedulerName: custom-scheduler
  containers:
  - name: nginx
    image: nginx
```

### 4.2 Advanced Admission Controller Setup

#### Step 1: Create Webhook Configuration
```yaml
# webhook-config.yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: pod-policy.example.com
webhooks:
- name: pod-policy.example.com
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    operations: ["CREATE"]
    resources: ["pods"]
    scope: "Namespaced"
  clientConfig:
    service:
      namespace: default
      name: validation-webhook
      path: "/validate"
    caBundle: ${CA_BUNDLE}
  admissionReviewVersions: ["v1"]
  sideEffects: None
  timeoutSeconds: 5
```

#### Step 2: Deploy Webhook Server
```yaml
# webhook-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: validation-webhook
spec:
  replicas: 2
  selector:
    matchLabels:
      app: validation-webhook
  template:
    metadata:
      labels:
        app: validation-webhook
    spec:
      containers:
      - name: webhook
        image: webhook-server:v1
        ports:
        - containerPort: 443
        volumeMounts:
        - name: webhook-certs
          mountPath: /etc/webhook/certs
          readOnly: true
      volumes:
      - name: webhook-certs
        secret:
          secretName: webhook-certs
```

### 4.3 Advanced Resource Management

#### Step 1: Configure Resource Quotas
```yaml
# advanced-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    requests.nvidia.com/gpu: 1
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["high"]
```

#### Step 2: Implement LimitRanges
```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-limit-range
spec:
  limits:
  - default:
      cpu: 500m
      memory: 512Mi
    defaultRequest:
      cpu: 200m
      memory: 256Mi
    max:
      cpu: "1"
      memory: 1Gi
    min:
      cpu: 100m
      memory: 128Mi
    type: Container
```

### 4.4 Advanced Node Configuration

#### Step 1: Configure Node Labels and Taints
```bash
# Add specialized node labels
kubectl label node worker1 node-type=compute
kubectl label node worker2 node-type=memory

# Add node taints
kubectl taint nodes worker1 dedicated=gpu:NoSchedule
```

#### Step 2: Create Node Affinity Rules
```yaml
# node-affinity-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node-type
            operator: In
            values:
            - compute
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "gpu"
    effect: "NoSchedule"
  containers:
  - name: gpu-container
    image: gpu-workload:v1
```

### Verification Tasks

1. Custom Scheduler Verification
```bash
# Check scheduler logs
kubectl logs -n kube-system custom-scheduler

# Verify pod scheduling
kubectl get pod custom-scheduled-pod -o wide
```

2. Admission Controller Testing
```bash
# Test pod creation with webhook
kubectl create -f test-pod.yaml

# Check webhook logs
kubectl logs -l app=validation-webhook
```

3. Resource Management Verification
```bash
# Check quota usage
kubectl describe resourcequota compute-resources

# Verify limit ranges
kubectl describe limitrange cpu-limit-range
```

### Troubleshooting Guide

1. Scheduler Issues
```bash
# Check scheduler status
kubectl get pods -n kube-system | grep scheduler
kubectl describe pod custom-scheduler -n kube-system

# Check scheduler logs
kubectl logs custom-scheduler -n kube-system
```

2. Admission Controller Issues
```bash
# Verify webhook configuration
kubectl get validatingwebhookconfigurations
kubectl describe validatingwebhookconfigurations pod-policy.example.com

# Check webhook connectivity
kubectl exec -it validation-webhook -- curl -k https://localhost:443/validate
```

3. Resource Management Issues
```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Verify quota enforcement
kubectl describe namespace default
```

### Best Practices
1. Always test custom schedulers in a non-production environment first
2. Implement gradual rollout of admission controllers
3. Monitor resource quotas and adjust as needed
4. Keep node labels and taints documented
5. Regular audit of custom configurations