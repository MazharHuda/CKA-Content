# Chapter 2: Core Concepts - Hands-on Labs

## Lab 1: Understanding Control Plane Components

![Control Plane Architecture](/Images/chapter02/ch02_lab01_control_plane.png)

### Objective
Explore and understand the core components of the Kubernetes control plane.

### Prerequisites
- Access to a Kubernetes cluster
- kubectl command-line tool
- Administrative access

### Steps

#### 1.1 Examining Control Plane Components
```bash
# View all pods in kube-system namespace
kubectl get pods -n kube-system

# Examine API server details
kubectl describe pod kube-apiserver-<node-name> -n kube-system

# View controller manager configuration
kubectl describe pod kube-controller-manager-<node-name> -n kube-system

# Check scheduler status
kubectl describe pod kube-scheduler-<node-name> -n kube-system
```

#### 1.2 Analyzing etcd
```bash
# View etcd pod details
kubectl describe pod etcd-<node-name> -n kube-system

# Create a test etcd backup
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

### Verification
- [ ] All control plane components are running
- [ ] etcd backup is created successfully
- [ ] Component logs show no errors

## Lab 2: Working with Basic Kubernetes Objects

![Basic Kubernetes Objects](/Images/chapter02/ch02_lab02_basic_objects.png)

### Objective
Create and manage fundamental Kubernetes objects including Pods, ReplicaSets, and Deployments.

### Steps

#### 2.1 Creating and Managing Pods
```bash
# Create a simple pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
EOF

# Verify pod creation
kubectl get pod nginx-pod
kubectl describe pod nginx-pod

# Access pod logs
kubectl logs nginx-pod

# Execute commands in pod
kubectl exec -it nginx-pod -- /bin/bash
```

#### 2.2 Working with ReplicaSets
```bash
# Create a ReplicaSet
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
EOF

# Scale ReplicaSet
kubectl scale replicaset frontend --replicas=5

# Verify scaling
kubectl get rs frontend
kubectl describe rs frontend
```

#### 2.3 Implementing Deployments
```bash
# Create a Deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
EOF

# Perform rolling update
kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1

# Check rollout status
kubectl rollout status deployment/nginx-deployment

# Rollback if needed
kubectl rollout undo deployment/nginx-deployment
```

### Verification Tasks
1. Verify pod status and logs
2. Check ReplicaSet scaling
3. Confirm Deployment updates
4. Test rollback functionality

## Lab 3: Networking and Services

![Kubernetes Networking and Services](/Images/chapter02/ch02_lab03_networking.png)

### Objective
Implement and test various Service types and networking configurations.

### Steps

#### 3.1 Creating Different Service Types
```bash
# Create ClusterIP Service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
EOF

# Create NodePort Service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30007
EOF
```

#### 3.2 Testing Service Connectivity
```bash
# Create test pod
kubectl run test-pod --image=busybox -- sleep 3600

# Test ClusterIP service
kubectl exec -it test-pod -- wget -qO- http://my-service

# Test NodePort service
kubectl exec -it test-pod -- wget -qO- http://node-ip:30007
```

[Continue with more lab sections...]

#### 3.3 Advanced Networking Labs

### Lab 4: Network Policies and Pod Communication

#### Objective
Implement and test Network Policies to control pod-to-pod communication.

#### Steps

##### 4.1 Create Test Pods and Services
```bash
# Create pods in different namespaces
kubectl create namespace prod
kubectl create namespace dev

# Create pods in prod namespace
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: frontend
  namespace: prod
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
EOF

# Create backend pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: backend
  namespace: prod
  labels:
    app: db
spec:
  containers:
  - name: mysql
    image: mysql:5.7
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
EOF
```

##### 4.2 Implement Network Policies
```bash
# Create default deny policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: prod
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# Create policy allowing frontend to backend communication
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: TCP
      port: 3306
EOF
```

##### 4.3 Testing Network Policies
```bash
# Test connectivity before and after policy
kubectl exec -n prod frontend -- curl -s backend
kubectl exec -n prod frontend -- mysql -h backend -u root -p

# Test blocked communication
kubectl run -n dev test-pod --image=nginx
kubectl exec -n dev test-pod -- curl -s backend.prod
```

#### Verification Tasks
- [ ] Confirm default deny policy blocks all traffic
- [ ] Verify frontend can access backend
- [ ] Confirm other pods cannot access backend

### Lab 5: Storage Configuration

#### Objective
Configure and test different types of storage in Kubernetes.

#### Steps

##### 5.1 Create Persistent Volume
```bash
# Create PV using NFS
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: /mnt/data
    server: nfs-server.example.com
EOF

# Create PV using hostPath (for testing)
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
EOF
```

##### 5.2 Create and Bind PVC
```bash
# Create PVC
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
EOF

# Verify PVC binding
kubectl get pvc
kubectl get pv
```

##### 5.3 Use Storage in Pods
```bash
# Create pod with PVC
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  containers:
    - name: task-pv-container
      image: nginx
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
EOF
```

#### Verification Tasks
- [ ] Check PV status
- [ ] Verify PVC binding
- [ ] Test data persistence

### Lab 6: Security Implementation

#### Objective
Implement basic security measures including RBAC and Secrets.

#### Steps

##### 6.1 Create Service Account and RBAC
```bash
# Create Service Account
kubectl create serviceaccount pod-reader

# Create Role
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
EOF

# Create RoleBinding
kubectl create rolebinding read-pods \
  --role=pod-reader \
  --serviceaccount=default:pod-reader
```

[Continue with more security labs...]

### Lab 7: Comprehensive Storage Management in Kubernetes

#### Objective
Master different storage concepts in Kubernetes including PV, PVC, StorageClasses, and dynamic provisioning.

#### Prerequisites
- Running Kubernetes cluster
- kubectl access
- Storage provider (cloud provider or local storage)

### Part 1: Basic Storage Operations

#### 7.1 Working with Persistent Volumes (PV)

```bash
# Create a basic Persistent Volume
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-demo
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/data
EOF

# Verify PV creation
kubectl get pv pv-demo
kubectl describe pv pv-demo
```

#### 7.2 Creating Persistent Volume Claims (PVC)

```bash
# Create a PVC to bind with PV
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
EOF

# Check PVC status
kubectl get pvc pvc-demo
kubectl describe pvc pvc-demo
```

### Part 2: Advanced Storage Configurations

#### 7.3 Implementing Storage Classes

```bash
# Create StorageClass for dynamic provisioning
cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
reclaimPolicy: Delete
allowVolumeExpansion: true
EOF

# Create PVC using StorageClass
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  storageClassName: fast-storage
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF
```

#### 7.4 Using Storage in Pods

```bash
# Create Pod with PVC
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: storage-pod
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: data-volume
      mountPath: /usr/share/nginx/html
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: pvc-demo
EOF

# Verify storage mounting
kubectl exec storage-pod -- df -h
kubectl exec -it storage-pod -- bash -c "echo 'Hello from PV' > /usr/share/nginx/html/index.html"
```

### Part 3: Storage Operations and Management

#### 7.5 Volume Expansion (if supported)

```bash
# Edit PVC to request more storage
kubectl patch pvc dynamic-pvc -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'

# Monitor expansion status
kubectl describe pvc dynamic-pvc
```

#### 7.6 Backup and Restore

```bash
# Create a backup job
cat <<EOF | kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: volume-backup
spec:
  template:
    spec:
      containers:
      - name: backup
        image: debian
        command: ["tar", "czf", "/backup/data.tar.gz", "/data"]
        volumeMounts:
        - name: data-volume
          mountPath: /data
        - name: backup-volume
          mountPath: /backup
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: pvc-demo
      - name: backup-volume
        hostPath:
          path: /mnt/backup
      restartPolicy: Never
EOF
```

### Part 4: Practical Exercises

#### Exercise 1: Multi-Pod Storage Access

```bash
# Create shared PV
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: shared-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: nfs-server.default.svc.cluster.local
    path: "/"
EOF

# Create multiple pods accessing same storage
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: reader-pod
spec:
  containers:
  - name: reader
    image: nginx
    volumeMounts:
    - name: shared-data
      mountPath: /data
      readOnly: true
  volumes:
  - name: shared-data
    persistentVolumeClaim:
      claimName: shared-pvc
---
apiVersion: v1
kind: Pod
metadata:
  name: writer-pod
spec:
  containers:
  - name: writer
    image: nginx
    volumeMounts:
    - name: shared-data
      mountPath: /data
  volumes:
  - name: shared-data
    persistentVolumeClaim:
      claimName: shared-pvc
EOF
```

### Verification Tasks

1. Basic Storage Verification
```bash
# Check PV status
kubectl get pv
kubectl get pvc

# Verify pod storage
kubectl exec storage-pod -- df -h
kubectl exec storage-pod -- ls -l /usr/share/nginx/html
```

2. Storage Class Verification
```bash
# Check StorageClass
kubectl get sc
kubectl describe sc fast-storage

# Verify dynamic provisioning
kubectl get pv | grep dynamic-pvc
```

3. Data Persistence Test
```bash
# Write data
kubectl exec storage-pod -- sh -c "echo 'test data' > /usr/share/nginx/html/test.txt"

# Delete and recreate pod
kubectl delete pod storage-pod
kubectl apply -f storage-pod.yaml

# Verify data persistence
kubectl exec storage-pod -- cat /usr/share/nginx/html/test.txt
```

### Troubleshooting Guide

1. Common Issues:
- PVC stuck in Pending state
- Volume mount failures
- Permission issues
- Storage class not found

2. Debug Commands:
```bash
# Check PV/PVC events
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>

# Check pod events
kubectl describe pod <pod-name>

# Check mount points
kubectl exec <pod-name> -- mount | grep <mount-path>
```

### Clean Up
```bash
# Delete resources
kubectl delete pod storage-pod
kubectl delete pvc pvc-demo dynamic-pvc
kubectl delete pv pv-demo
kubectl delete sc fast-storage
```
Security 
### Lab 8: Kubernetes Security Implementation

#### Objective
Implement and understand Kubernetes security concepts including RBAC, Security Contexts, Network Policies, and Secrets.

#### Prerequisites
- Running Kubernetes cluster
- kubectl with admin access
- OpenSSL for certificate generation

### Part 1: RBAC Configuration

#### 8.1 Creating Service Accounts and Role-Based Access Control

```bash
# Create namespace for testing
kubectl create namespace security-test

# Create Service Account
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: security-test
EOF

# Create Role
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: security-test
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
EOF

# Create RoleBinding
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: security-test
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: security-test
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF
```

#### 8.2 Testing RBAC Configuration

```bash
# Create test pod with service account
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: rbac-test-pod
  namespace: security-test
spec:
  serviceAccountName: app-service-account
  containers:
  - name: curl
    image: curlimages/curl
    command: ["sleep", "3600"]
EOF

# Test permissions
kubectl exec -n security-test rbac-test-pod -- \
  curl -s -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  https://kubernetes.default.svc/api/v1/namespaces/security-test/pods/
```

### Part 2: Security Contexts

#### 8.3 Implementing Pod Security Contexts

```bash
# Create pod with security context
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: security-context-pod
  namespace: security-test
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: sec-ctx-demo
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: sec-ctx-vol
      mountPath: /data/demo
  volumes:
  - name: sec-ctx-vol
    emptyDir: {}
EOF

# Verify security context
kubectl exec -n security-test security-context-pod -- id
kubectl exec -n security-test security-context-pod -- ls -l /data/demo
```

### Part 3: Network Policies

#### 8.4 Implementing Network Security

```bash
# Create test deployments
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: security-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: security-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: nginx
        image: nginx
EOF

# Create default deny policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: security-test
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

# Create allowed communication policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-to-backend
  namespace: security-test
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 80
EOF
```

### Part 4: Secrets Management

#### 8.5 Creating and Using Secrets

```bash
# Create secret from literal values
kubectl create secret generic app-secrets \
  --namespace=security-test \
  --from-literal=db-password='MySecretPassword123' \
  --from-literal=api-key='ApiKey123456'

# Create secret from files
echo -n 'admin' > ./username.txt
echo -n 'S3cret!' > ./password.txt
kubectl create secret generic user-creds \
  --namespace=security-test \
  --from-file=./username.txt \
  --from-file=./password.txt

# Create pod using secrets
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
  namespace: security-test
spec:
  containers:
  - name: test-container
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: db-password
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secrets"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: user-creds
EOF
```

### Part 5: Certificate Management

#### 8.6 Creating and Managing TLS Certificates

```bash
# Generate private key and CSR
openssl genrsa -out app.key 2048
openssl req -new -key app.key -out app.csr -subj "/CN=myapp.security-test.svc"

# Create CertificateSigningRequest
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: app-csr
spec:
  request: $(cat app.csr | base64 | tr -d '\n')
  signerName: kubernetes.io/kubelet-serving
  usages:
  - digital signature
  - key encipherment
  - server auth
EOF

# Approve certificate
kubectl certificate approve app-csr
```

### Verification Tasks

1. RBAC Verification
```bash
# Test service account permissions
kubectl auth can-i list pods --as=system:serviceaccount:security-test:app-service-account -n security-test
kubectl auth can-i create pods --as=system:serviceaccount:security-test:app-service-account -n security-test
```

2. Security Context Verification
```bash
# Verify user and group settings
kubectl exec -n security-test security-context-pod -- id
kubectl exec -n security-test security-context-pod -- ls -la /data/demo
```

3. Network Policy Testing
```bash
# Test network connectivity
kubectl exec -n security-test deploy/frontend -- curl -s backend
kubectl exec -n security-test deploy/frontend -- curl -s backend-svc
```

4. Secrets Verification
```bash
# Verify secret mounting
kubectl exec -n security-test secret-test-pod -- ls -l /etc/secrets
kubectl exec -n security-test secret-test-pod -- env | grep DB_PASSWORD
```

### Clean Up
```bash
# Remove all resources
kubectl delete namespace security-test
kubectl delete csr app-csr
rm app.key app.csr username.txt password.txt
```

Troubleshooting

### Lab 9: Kubernetes Troubleshooting Scenarios

#### Objective
Learn to diagnose and resolve common Kubernetes issues across different components and resources.

#### Prerequisites
- Running Kubernetes cluster
- kubectl with admin access
- Basic understanding of Kubernetes components

### Part 1: Pod Troubleshooting

#### 9.1 Diagnosing Pod Issues

```bash
# Create a pod with common issues
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: troubleshoot-pod
spec:
  containers:
  - name: nginx
    image: nginx:invalid-tag    # Invalid image tag
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
EOF

# Troubleshooting commands
kubectl get pod troubleshoot-pod
kubectl describe pod troubleshoot-pod
kubectl logs troubleshoot-pod
kubectl get events --sort-by=.metadata.creationTimestamp
```

#### 9.2 Common Pod Issues and Solutions

```bash
# 1. Image Pull Issues
kubectl get pod troubleshoot-pod -o yaml | grep -A 5 status:
kubectl describe pod troubleshoot-pod | grep "Events:" -A 10

# 2. Resource Constraints
kubectl top pod troubleshoot-pod
kubectl describe node | grep -A 5 "Allocated resources"

# 3. Liveness/Readiness Probe Failures
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: probe-test
spec:
  containers:
  - name: nginx
    image: nginx
    livenessProbe:
      httpGet:
        path: /nonexistent
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 3
EOF

kubectl describe pod probe-test
```

### Part 2: Service and Networking Troubleshooting

#### 9.3 Service Connectivity Issues

```bash
# Create test deployment and service
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web-wrong  # Intentionally wrong selector
  ports:
  - port: 80
    targetPort: 80
EOF

# Troubleshooting steps
kubectl get endpoints web-service
kubectl describe service web-service
kubectl get pods -l app=web
kubectl get pods -l app=web-wrong
```

#### 9.4 Network Policy Troubleshooting

```bash
# Create test pods and network policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: TCP
      port: 5432
EOF

# Test connectivity
kubectl run test-pod --image=busybox -- sleep 3600
kubectl exec test-pod -- wget -O- --timeout=2 http://web-service
```

### Part 3: Storage Troubleshooting

#### 9.5 PV/PVC Issues

```bash
# Create PV and PVC with mismatched specifications
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteMany  # Mismatched access mode
  resources:
    requests:
      storage: 2Gi   # Larger than PV
EOF

# Troubleshooting commands
kubectl get pv,pvc
kubectl describe pv test-pv
kubectl describe pvc test-pvc
```

### Part 4: Control Plane Troubleshooting

#### 9.6 API Server Issues

```bash
# Check API server status
kubectl get componentstatuses
kubectl get pods -n kube-system
kubectl logs -n kube-system kube-apiserver-$(hostname)

# Test API server connectivity
curl -k https://localhost:6443/healthz
kubectl get --raw /healthz
kubectl get --raw /healthz/etcd
```

#### 9.7 Controller Manager and Scheduler

```bash
# Check controller manager status
kubectl get pods -n kube-system | grep controller-manager
kubectl describe pods -n kube-system kube-controller-manager-$(hostname)

# Check scheduler status
kubectl get pods -n kube-system | grep scheduler
kubectl logs -n kube-system kube-scheduler-$(hostname)
```

### Part 5: Node Troubleshooting

#### 9.8 Node Issues

```bash
# Check node status
kubectl get nodes
kubectl describe node <node-name>
kubectl top node

# Check kubelet status
systemctl status kubelet
journalctl -u kubelet

# Check node capacity and allocatable resources
kubectl describe node | grep -A 5 "Capacity"
kubectl describe node | grep -A 5 "Allocatable"
```

### Troubleshooting Cheatsheet

1. Pod Issues:
```bash
kubectl get pod <pod-name> -o yaml
kubectl describe pod <pod-name>
kubectl logs <pod-name> [-c <container-name>]
kubectl exec -it <pod-name> -- /bin/bash
```

2. Service Issues:
```bash
kubectl get endpoints <service-name>
kubectl get pods -l <selector-label>
kubectl run test-pod --image=busybox -- sleep 3600
kubectl exec test-pod -- wget -O- <service-name>
```

3. Storage Issues:
```bash
kubectl get pv,pvc
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>
```

4. Node Issues:
```bash
kubectl describe node <node-name>
kubectl top node
kubectl get events --field-selector involvedObject.kind=Node
```

### Verification Tasks

1. Pod Troubleshooting
- [ ] Identify and fix image pull issues
- [ ] Resolve resource constraint problems
- [ ] Fix probe failures

2. Service Troubleshooting
- [ ] Fix service selector issues
- [ ] Verify endpoint creation
- [ ] Test service connectivity

3. Storage Troubleshooting
- [ ] Resolve PV/PVC binding issues
- [ ] Fix storage capacity problems
- [ ] Verify storage access modes

4. Node Troubleshooting
- [ ] Check node conditions
- [ ] Verify kubelet status
- [ ] Monitor resource usage