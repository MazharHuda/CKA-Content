# Chapter 8: Security - Practice Labs

## Prerequisites
- Running Kubernetes cluster
- kubectl CLI tool configured
- OpenSSL installed for certificate generation
- Basic understanding of Kubernetes security concepts

## Lab 1: Certificate Management and TLS
![ Certificate Management and TLS](/Images/chapter08/ch08_lab01_certificates.png)
### Objective
Learn to create and manage certificates for secure communication in Kubernetes.

### Tasks

1. Create a Certificate Signing Request (CSR):
```bash
# Generate private key
openssl genrsa -out john.key 2048

# Create CSR
openssl req -new -key john.key \
  -out john.csr \
  -subj "/CN=john/O=developers"

# Base64 encode the CSR
cat john.csr | base64 | tr -d '\n'
```

2. Submit CSR to Kubernetes:
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: <base64-encoded-csr>
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # 24 hours
  usages:
  - client auth
```

3. Approve CSR:
```bash
# Apply CSR
kubectl apply -f john-csr.yaml

# View CSR
kubectl get csr

# Approve CSR
kubectl certificate approve john-developer

# Get the signed certificate
kubectl get csr john-developer -o jsonpath='{.status.certificate}' | base64 -d > john.crt
```

## Lab 2: RBAC Configuration
![ RBAC Configuration](/Images/chapter08/ch08_lab02_rbac.png)
### Objective
Implement Role-Based Access Control (RBAC) for different user types.

### Tasks

1. Create Role for Pod Management:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: pod-manager
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

2. Create RoleBinding:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-manager-binding
  namespace: development
subjects:
- kind: User
  name: john
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-manager
  apiGroup: rbac.authorization.k8s.io
```

3. Test Access:
```bash
# Test with kubectl
kubectl auth can-i create pods --namespace=development --as=john
kubectl auth can-i delete pods --namespace=development --as=john
kubectl auth can-i create deployments --namespace=development --as=john
```

## Lab 3: Pod Security Contexts
![Pod Security Contexts](/Images/chapter08/ch08_lab03_security_context.png)
### Objective
Configure and test pod security contexts and policies.

### Tasks

1. Create Pod with Security Context:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: sec-ctx-demo
    image: busybox
    command: ["sh", "-c", "sleep 1h"]
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: sec-storage
      mountPath: /data
  volumes:
  - name: sec-storage
    emptyDir: {}
```

2. Verify Security Context:
```bash
# Create pod
kubectl apply -f security-context-pod.yaml

# Verify user and group settings
kubectl exec security-context-demo -- id

# Check file permissions
kubectl exec security-context-demo -- ls -l /data
```

## Lab 4: Network Policies
![Network Policies](/Images/chapter08/ch08_lab04_network_policies.png)
### Objective
Implement and test network policies for pod isolation.

### Tasks

1. Create Test Pods:
```yaml
# Create namespaces
kubectl create namespace policy-demo

# Create pods in the namespace
kubectl run backend --image=nginx --labels=app=backend -n policy-demo
kubectl run frontend --image=nginx --labels=app=frontend -n policy-demo
kubectl run test-pod --image=nginx --labels=app=test -n policy-demo
```

2. Create Network Policy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
  namespace: policy-demo
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
```

3. Test Network Policy:
```bash
# Test access from frontend pod
kubectl exec frontend -n policy-demo -- curl backend

# Test access from test pod (should fail)
kubectl exec test-pod -n policy-demo -- curl backend
```

## Lab 5: Secret Management
![Secret Management](/Images/chapter08/ch08_lab05_secrets.png)
### Objective
Create and manage Kubernetes secrets securely.

### Tasks

1. Create Secrets:
```bash
# Create secret from literal values
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password=S3cur3P@ss

# Create secret from files
echo -n 'admin' > ./username.txt
echo -n 'S3cur3P@ss' > ./password.txt
kubectl create secret generic db-creds-file \
  --from-file=username=./username.txt \
  --from-file=password=./password.txt
```

2. Use Secrets in Pod:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
  - name: test-container
    image: nginx
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: password
    volumeMounts:
    - name: secret-volume
      mountPath: "/etc/secrets"
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-creds-file
```

## Lab 6: Audit Logging
![Audit Logging](/Images/chapter08/ch08_lab06_audit.png)
### Objective
Configure and analyze Kubernetes audit logging.

### Tasks

1. Create Audit Policy:
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: audit-policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods"]
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
```

2. Configure API Server:
```bash
# Add these flags to kube-apiserver.yaml
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
--audit-log-path=/var/log/kubernetes/audit.log
--audit-log-maxage=30
--audit-log-maxbackup=10
--audit-log-maxsize=100
```

3. Analyze Audit Logs:
```bash
# View audit logs
tail -f /var/log/kubernetes/audit.log

# Search for specific events
grep "secret" /var/log/kubernetes/audit.log
```

## Verification Tasks

1. Certificate Management
```bash
# Verify certificate
openssl x509 -in john.crt -text -noout
```

2. RBAC Verification
```bash
# Test permissions
kubectl auth can-i --list --as=john --namespace=development
```

3. Network Policy Testing
```bash
# Test connectivity
kubectl exec -n policy-demo frontend -- curl -s backend
kubectl exec -n policy-demo test-pod -- curl -s backend
```

## Cleanup

```bash
# Remove test resources
kubectl delete namespace policy-demo
kubectl delete csr john-developer
kubectl delete secret db-creds db-creds-file
kubectl delete pod security-context-demo secret-test-pod
```

## Tips for CKA Exam

1. Master certificate generation and CSR approval process
2. Understand RBAC components and their relationships
3. Know how to troubleshoot network policies
4. Practice creating and managing secrets
5. Be familiar with security context configurations
