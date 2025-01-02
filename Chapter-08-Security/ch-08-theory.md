# Chapter 8: Kubernetes Security

## 1. Authentication and Authorization

### 1.1 Overview
```ascii
┌─────────────────Kubernetes Security────────────────┐
│                                                   │
│  ┌─Authentication─┐     ┌──Authorization──┐       │
│  │ Who are you?   │ ──► │  What can you   │       │
│  │                │     │     do?         │       │
│  └────────────────┘     └────────────────┘       │
│           │                     │                 │
│  ┌────────▼─────┐     ┌────────▼─────┐          │
│  │  Certificates│     │     RBAC     │          │
│  │  Tokens      │     │   Policies   │          │
│  └──────────────┘     └──────────────┘          │
└───────────────────────────────────────────────────┘
```

### 1.2 Authentication Methods
1. X.509 Certificates
```yaml
# Certificate Signing Request (CSR)
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john
spec:
  request: <base64-encoded-csr>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

2. Service Account Tokens
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: default
automountServiceAccountToken: false
```

3. OpenID Connect (OIDC)
```yaml
# API Server Configuration
--oidc-issuer-url=https://accounts.google.com
--oidc-client-id=kubernetes
--oidc-username-claim=email
--oidc-groups-claim=groups
```

### 1.3 Role-Based Access Control (RBAC)

#### 1.3.1 Roles and ClusterRoles
```yaml
# Role Example
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

# ClusterRole Example
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

#### 1.3.2 RoleBindings and ClusterRoleBindings
```yaml
# RoleBinding Example
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## 2. Pod Security

### 2.1 Security Contexts
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
```

### 2.2 Pod Security Standards
```ascii
┌─────────────Security Levels──────────────┐
│                                         │
│  ┌─Privileged─┐  ┌─Baseline─┐  ┌─Restricted─┐ │
│  │ No         │  │ Limited  │  │ Enhanced  │ │
│  │ Restrictions│  │ Security │  │ Security  │ │
│  └────────────┘  └──────────┘  └───────────┘ │
└─────────────────────────────────────────────┘
```

### 2.3 Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## 3. Cluster Security

### 3.1 Control Plane Security
1. API Server Security
```yaml
# API Server Configuration
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --enable-admission-plugins=NodeRestriction
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
```

2. etcd Security
```yaml
# etcd Configuration
apiVersion: v1
kind: Pod
metadata:
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --key-file=/etc/kubernetes/pki/etcd/server.key
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --client-cert-auth=true
```

### 3.2 Node Security
```yaml
# Node Authorization Configuration
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

## 4. Secret Management

### 4.1 Kubernetes Secrets
```yaml
# Create Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  username: admin
  password: t0p-Secret

# Use Secret in Pod
apiVersion: v1
kind: Pod
metadata:
  name: secret-test
spec:
  containers:
  - name: test
    image: busybox
    env:
    - name: USERNAME
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: username
```

### 4.2 External Secret Management
```yaml
# Vault Integration Example
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-database
spec:
  provider: vault
  parameters:
    vaultAddress: "http://vault.default:8200"
    roleName: "database-role"
    objects: |
      - objectName: "db-password"
        secretPath: "secret/data/database"
        secretKey: "password"
```

## 5. Audit Logging

### 5.1 Audit Policy Configuration
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

### 5.2 Audit Log Configuration
```yaml
# API Server Audit Configuration
--audit-log-path=/var/log/kubernetes/audit.log
--audit-log-maxage=30
--audit-log-maxbackup=10
--audit-log-maxsize=100
--audit-policy-file=/etc/kubernetes/audit-policy.yaml
```

## Best Practices

### 1. Authentication and Authorization
```markdown
- Use strong authentication methods
- Implement least privilege principle
- Regular access review
- Proper service account management
- Certificate rotation
```

### 2. Pod Security
```markdown
- Use security contexts
- Implement network policies
- Enable pod security standards
- Regular security scanning
- Container image security
```

### 3. Secret Management
```markdown
- Encrypt secrets at rest
- Use external secret stores
- Regular secret rotation
- Audit secret access
- Implement proper RBAC
```

### 4. Network Security
```markdown
- Implement network policies
- Secure cluster communications
- Use TLS everywhere
- Regular network audits
- Monitor network traffic
```

## Common Pitfalls

### 1. Security Configuration
```markdown
- Overly permissive RBAC
- Missing network policies
- Insecure pod configurations
- Weak secret management
- Insufficient logging
```

### 2. Operational Issues
```markdown
- Certificate expiration
- Token management
- Access control drift
- Audit log management
- Security update delays
```

[Continue with more sections...]
