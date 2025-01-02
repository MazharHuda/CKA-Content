# Chapter 8: Security - Real-world Scenarios

## Scenario 1: Implementing Multi-tenant Security

### Context
A company needs to set up a secure multi-tenant environment in their Kubernetes cluster where different teams can run their applications in isolation.

### Requirements
- Namespace isolation
- Resource quotas
- Network isolation
- RBAC configuration
- Audit logging

### Solution

#### 1. Namespace and RBAC Setup
```yaml
# Create namespace with security restrictions
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  labels:
    pod-security.kubernetes.io/enforce: restricted
---
# Create team role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: team-a
  name: team-access
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
---
# Create RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-access-binding
  namespace: team-a
subjects:
- kind: Group
  name: team-a
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: team-access
  apiGroup: rbac.authorization.k8s.io
```

#### 2. Network Policy Implementation
```yaml
# Default deny policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: team-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
# Allow internal communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internal
  namespace: team-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: team-a
```

### Implementation Steps

1. Set up Authentication
```bash
# Generate client certificate
openssl genrsa -out team-a.key 2048
openssl req -new -key team-a.key -out team-a.csr -subj "/CN=team-a/O=team-a"
```

2. Configure Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

## Scenario 2: Securing API Server Access

### Context
A financial services company needs to implement secure access to their Kubernetes API server with audit logging and monitoring.

### Requirements
- TLS authentication
- RBAC policies
- Audit logging
- Access monitoring
- Certificate management

### Solution

#### 1. API Server Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
    - --authorization-mode=Node,RBAC
    - --enable-admission-plugins=NodeRestriction
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
```

#### 2. Audit Policy Configuration
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: audit-policy
rules:
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods"]
  verbs: ["create", "delete"]
```

### Implementation Steps

1. Certificate Management
```bash
# Create CA
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -days 365 -out ca.crt

# Create server certificate
openssl genrsa -out apiserver.key 2048
openssl req -new -key apiserver.key -out apiserver.csr
```

2. Configure Monitoring
```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-server
  namespace: monitoring
spec:
  endpoints:
  - interval: 30s
    port: https
    scheme: https
    tlsConfig:
      caFile: /etc/prometheus/secrets/ca.crt
```

## Scenario 3: Container Security Implementation

### Context
A company needs to implement secure container configurations for their applications running in Kubernetes.

### Requirements
- Non-root containers
- Limited capabilities
- Read-only root filesystem
- Resource limitations
- Security context enforcement

### Solution

#### 1. Secure Pod Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: app
    image: secure-app:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
    resources:
      limits:
        cpu: "1"
        memory: "512Mi"
      requests:
        cpu: "500m"
        memory: "256Mi"
```

#### 2. Pod Security Standards
```yaml
# Namespace configuration
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Best Practices

1. Authentication and Authorization
```markdown
- Use X.509 certificates for authentication
- Implement RBAC with least privilege
- Regular access review and audit
- Automated certificate rotation
- Strong password policies
```

2. Network Security
```markdown
- Default deny network policies
- Encrypt all traffic with TLS
- Segment network access
- Regular security scanning
- Monitor network traffic
```

3. Container Security
```markdown
- Use minimal base images
- Regular security updates
- Scan for vulnerabilities
- Implement pod security standards
- Resource isolation
```

### Common Pitfalls

1. Security Configuration
```markdown
- Overly permissive RBAC
- Missing network policies
- Insecure pod configurations
- Weak secret management
- Insufficient logging
```

2. Operational Issues
```markdown
- Certificate expiration
- Token management
- Access control drift
- Audit log management
- Security update delays
```

## Scenario 4: Implementing Zero-Trust Security Model

### Context
An organization needs to implement a zero-trust security model in their Kubernetes cluster to meet compliance requirements.

### Requirements
- Default deny all traffic
- Pod-to-pod authentication
- Service mesh integration
- Encrypted communication
- Comprehensive auditing

### Solution

#### 1. Default Network Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

#### 2. Service Mesh Configuration (using Istio)
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: default
  namespace: default
spec:
  host: "*.default.svc.cluster.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
```

#### 3. Pod Security Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
  annotations:
    sidecar.istio.io/inject: "true"
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: secure-app:1.0
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
```

## Scenario 5: Implementing Security for CI/CD Pipeline

### Context
A DevOps team needs to implement secure CI/CD pipelines in Kubernetes with automated security scanning and enforcement.

### Requirements
- Secure image scanning
- Admission control
- Policy enforcement
- Automated compliance checks
- Secure secrets management

### Solution

#### 1. Image Scanning Policy
```yaml
apiVersion: imagepolicy.k8s.io/v1alpha1
kind: ImageReview
metadata:
  name: image-review
spec:
  containers:
  - image: myapp:latest
  annotations:
    scanner.security.io/status: "Approved"
```

#### 2. Admission Webhook Configuration
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: security-validation
webhooks:
- name: security.validator.io
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    operations: ["CREATE", "UPDATE"]
    resources: ["pods"]
  clientConfig:
    service:
      namespace: security
      name: validator-service
      path: "/validate"
    caBundle: <ca-bundle>
```

#### 3. Policy Enforcement
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: deployment-must-have-security-label
spec:
  match:
    kinds:
    - apiGroups: ["apps"]
      kinds: ["Deployment"]
  parameters:
    labels: ["security-level"]
```

## Scenario 6: Implementing Security for Edge Computing

### Context
A company needs to secure Kubernetes workloads running on edge locations with limited connectivity and physical security.

### Requirements
- Secure boot process
- Node attestation
- Encrypted storage
- Limited connectivity
- Automated recovery

### Solution

#### 1. Node Security Configuration
```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: secure-runtime
handler: kata-containers
---
apiVersion: v1
kind: Pod
metadata:
  name: edge-workload
spec:
  runtimeClassName: secure-runtime
  containers:
  - name: app
    image: edge-app:1.0
    securityContext:
      readOnlyRootFilesystem: true
```

#### 2. Edge Network Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: edge-policy
spec:
  podSelector:
    matchLabels:
      app: edge-workload
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/8
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/8
    ports:
    - protocol: TCP
      port: 443
```

#### 3. Secure Storage Configuration
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: edge-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  encryption:
    secretRef:
      name: storage-key
  local:
    path: /mnt/secure-data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - edge-node-1
```

### Implementation Guidelines

1. Edge Security Checklist
```markdown
- Implement secure boot with TPM verification
- Configure node attestation
- Set up encrypted storage
- Implement network isolation
- Configure automated recovery
```

2. Security Monitoring
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: edge-security-monitor
spec:
  selector:
    matchLabels:
      app: edge-workload
  endpoints:
  - port: metrics
    interval: 30s
    scheme: https
    tlsConfig:
      caFile: /etc/prometheus/secrets/ca
```

3. Recovery Procedures
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: security-check
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: security-check
            image: security-tools:1.0
            command:
            - /scripts/verify-security.sh
```

### Best Practices for Edge Security

1. Physical Security
```markdown
- Implement tamper detection
- Secure hardware storage
- Regular physical audits
- Access control systems
- Environmental monitoring
```

2. Network Security
```markdown
- Implement VPN connectivity
- Use mutual TLS
- Regular security scanning
- Traffic monitoring
- Intrusion detection
```

3. Data Security
```markdown
- Encrypt data at rest
- Secure key management
- Regular backups
- Data access auditing
- Compliance monitoring
```

[Continue with more scenarios if needed...]
