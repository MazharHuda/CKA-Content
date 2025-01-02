# Chapter 2: Kubernetes Architecture and Core Concepts

## 1. Understanding Kubernetes Architecture

### 1.1 Overview of Kubernetes
Kubernetes (K8s) is a production-grade container orchestration system that provides a platform for automating deployment, scaling, and operations of application containers across clusters of hosts.

#### 1.1.1 Evolution and History
- Developed by Google based on Borg experience
- Open-sourced in 2014
- Now maintained by CNCF
- Industry standard for container orchestration

#### 1.1.2 Key Features and Benefits
1. **Container Orchestration**
   - Automated container deployment and scheduling
   - Container lifecycle management
   - Dynamic scaling based on demand
   - Load balancing across containers
   - Self-healing mechanisms
   - Zero-downtime deployments

2. **Infrastructure Abstraction**
   - Hardware-level abstraction
   - Platform independence
   - Cloud provider agnostic
   - Consistent environments

3. **Declarative Configuration**
   - Infrastructure as Code (IaC)
   - Desired state management
   - Version-controlled configurations
   - Reproducible deployments

### 1.2 Architectural Overview

#### 1.2.1 High-Level Architecture
```ascii
┌──────────────────────────────────────────┐
│            Kubernetes Cluster            │
│                                         │
│  ┌─────────────┐      ┌─────────────┐   │
│  │Control Plane│      │Worker Nodes │   │
│  │(Master)     │      │            │   │
│  │             │      │            │   │
│  │• API Server │      │• Kubelet   │   │
│  │• Scheduler  │◄────►│• Kube-proxy│   │
│  │• Controller │      │• Containers│   │
│  │• etcd       │      │            │   │
│  └─────────────┘      └─────────────┘   │
│                                         │
└──────────────────────────────────────────┘
```

### 1.3 Control Plane Components (Master Node)

#### 1.3.1 API Server (kube-apiserver)
The API server is the front-end for the Kubernetes control plane, handling all API requests.

**Key Functions:**
- Authentication and Authorization
- API Object validation and configuration
- REST API endpoint for all operations
- Resource quota management
- Horizontal scaling capability

**Configuration Example:**
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
    - --advertise-address=192.168.1.10
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-servers=https://127.0.0.1:2379
```

**Best Practices:**
1. Enable RBAC authorization
2. Configure appropriate admission controllers
3. Implement API request rate limiting
4. Use secure communication (TLS)
5. Regular security audits

**Common Pitfalls:**
- Insufficient resource allocation
- Improper security configuration
- Missing admission controllers
- Inadequate monitoring

#### 1.3.2 etcd
Distributed key-value store that serves as Kubernetes' backing store for all cluster data.

**Key Characteristics:**
- Consistent and highly-available
- Source of truth for cluster state
- Supports watch operations
- Versioned key-value store

**Configuration Example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.1.10:2379
    - --data-dir=/var/lib/etcd
    - --initial-cluster-state=new
    - --initial-cluster-token=etcd-cluster
```

**Best Practices:**
1. Regular backups
2. High availability configuration
3. Resource monitoring
4. Performance tuning
5. Security hardening

**Common Pitfalls:**
- No backup strategy
- Insufficient resources
- Poor performance configuration
- Insecure setup

[Continue with more components...]

### 1.4 Worker Node Components

#### 1.4.1 Kubelet
The primary node agent that runs on each node.

**Key Responsibilities:**
- Pod lifecycle management
- Container health checks
- Node status reporting
- Volume management

**Configuration Example:**
```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
address: "192.168.1.10"
port: 10250
serializeImagePulls: true
evictionHard:
  memory.available: "100Mi"
  nodefs.available: "10%"
```

[Continue with detailed sections for each component...]

### 1.5 Real-world Considerations

#### 1.5.1 Production Deployment Considerations
1. **High Availability**
   - Multiple master nodes
   - Distributed etcd cluster
   - Load balancer configuration

2. **Security**
   - Network policies
   - RBAC configuration
   - Secret management
   - Certificate rotation

3. **Monitoring and Logging**
   - Metrics collection
   - Log aggregation
   - Alerting setup
   - Performance monitoring

4. **Disaster Recovery**
   - Backup procedures
   - Recovery testing
   - Failure scenarios
   - Data protection

[Continue with more sections...]

## 2. Kubernetes Objects and Workloads

### 2.1 Pods: The Basic Building Block

#### 2.1.1 Pod Concepts
Pods are the smallest deployable units in Kubernetes that can be created, scheduled, and managed.

```ascii
┌──────────────Pod───────────────┐
│ ┌────────────┐  ┌────────────┐ │
│ │Container 1 │  │Container 2 │ │
│ │            │  │            │ │
│ │ • App      │  │ • Sidecar  │ │
│ │ • Storage  │  │ • Logging  │ │
│ └────────────┘  └────────────┘ │
│     Shared Network & IPC        │
│     Shared Storage Volumes      │
└────────────────────────────────┘
```

**Key Characteristics:**
- Shared network namespace
- Shared storage volumes
- Shared IPC namespace
- Co-located and co-scheduled

**Pod Manifest Example:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: web
spec:
  containers:
  - name: web
    image: nginx:1.14
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
  
  - name: content-sync
    image: debian
    volumeMounts:
    - name: shared-data
      mountPath: /content
    command: ["/bin/sh"]
    args: ["-c", "while true; do date >> /content/index.html; sleep 10; done"]
  
  volumes:
  - name: shared-data
    emptyDir: {}
```

**Best Practices:**
1. Keep pods focused and minimal
2. Use appropriate health checks
3. Set resource requests and limits
4. Implement proper labels and annotations
5. Use init containers when needed

**Common Pitfalls:**
- Too many containers in a pod
- Missing resource specifications
- Improper health checks
- Poor security context configuration

### 2.2 ReplicaSets: Ensuring Pod Availability

#### 2.2.1 ReplicaSet Concepts
ReplicaSets maintain a stable set of replica Pods running at any given time.

```ascii
┌─────────────ReplicaSet──────────────┐
│                                     │
│  ┌─────Pod─────┐   ┌─────Pod─────┐  │
│  │ Container   │   │ Container   │  │
│  └─────────────┘   └─────────────┘  │
│                                     │
│  ┌─────Pod─────┐   ┌─────Pod─────┐  │
│  │ Container   │   │ Container   │  │
│  └─────────────┘   └─────────────┘  │
└─────────────────────────────────────┘
```

**ReplicaSet Manifest Example:**
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: frontend
    tier: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        ports:
        - containerPort: 80
```

**Best Practices:**
1. Use Deployments instead of direct ReplicaSet management
2. Implement proper label selectors
3. Set appropriate replica counts
4. Configure update strategies
5. Use pod disruption budgets

**Common Pitfalls:**
- Direct manipulation of ReplicaSets
- Incorrect selector configuration
- Missing pod template labels
- Improper scaling configurations

### 2.3 Deployments: Managing Application Updates

#### 2.3.1 Deployment Concepts
Deployments provide declarative updates for Pods and ReplicaSets.

```ascii
┌─────────────Deployment──────────────┐
│                                     │
│  ┌────ReplicaSet (v1)────┐         │
│  │ ┌─Pod─┐ ┌─Pod─┐ ┌─Pod─┐│        │
│  │ │     │ │     │ │     ││        │
│  │ └─────┘ └─────┘ └─────┘│        │
│  └────────────────────────┘        │
│                                     │
│  ┌────ReplicaSet (v2)────┐         │
│  │ ┌─Pod─┐ ┌─Pod─┐ ┌─Pod─┐│        │
│  │ │     │ │     │ │     ││        │
│  │ └─────┘ └─────┘ └─────┘│        │
│  └────────────────────────┘        │
└─────────────────────────────────────┘
```

**Deployment Manifest Example:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
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
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
```

[Continue with more sections...]

### 2.4 Services: Networking and Service Discovery

#### 2.4.1 Service Concepts
Services provide a stable networking endpoint for Pods and enable load balancing.

```ascii
┌─────────────Service──────────────┐
│           ClusterIP              │
│         (10.96.x.x)             │
│               │                  │
│               ▼                  │
│    ┌──────────────────────┐     │
│    │    Load Balancer     │     │
│    └──────────────────────┘     │
│               │                  │
│               ▼                  │
│    ┌─Pod──┐ ┌─Pod──┐ ┌─Pod──┐   │
│    │      │ │      │ │      │   │
│    └──────┘ └──────┘ └──────┘   │
└──────────────────────────────────┘
```

**Service Types:**
1. **ClusterIP (default)**
   - Internal cluster access only
   - Stable internal IP address
   - Load balancing within cluster

2. **NodePort**
   - Exposes service on each node's IP
   - Port range: 30000-32767
   - Includes ClusterIP functionality

3. **LoadBalancer**
   - External load balancer
   - Cloud provider integration
   - Automatic public IP assignment

4. **ExternalName**
   - DNS CNAME record
   - No proxying
   - Service discovery for external services

**Service Manifest Example:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

**Best Practices:**
1. Use meaningful service names
2. Implement proper selectors
3. Configure appropriate health checks
4. Set session affinity when needed
5. Use appropriate service type

**Common Pitfalls:**
- Incorrect selector configuration
- Missing port mappings
- Improper security group settings
- Inadequate health checks

### 2.5 Storage Architecture

#### 2.5.1 Persistent Volumes and Claims
```ascii
┌─────────────Storage Architecture──────────────┐
│                                              │
│  ┌─────────────┐      ┌─────────────┐       │
│  │StorageClass │      │PersistentVol│       │
│  │             │──┬──►│             │       │
│  └─────────────┘  │   └─────────────┘       │
│                   │          ▲              │
│  ┌─────────────┐  │          │              │
│  │PVC          │──┘          │              │
│  │             │─────────────┘              │
│  └─────────────┘                            │
│         ▲                                   │
│         │                                   │
│    ┌────Pod────┐                           │
│    │           │                           │
│    └───────────┘                           │
└──────────────────────────────────────────────┘
```

**PersistentVolume Example:**
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  nfs:
    path: /mnt/data
    server: nfs-server.example.com
```

**PersistentVolumeClaim Example:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### 2.6 Configuration and Secrets

#### 2.6.1 ConfigMaps
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    environment=production
    log_level=INFO
    max_users=100
  feature.json: |
    {
      "feature1": true,
      "feature2": false
    }
```

#### 2.6.2 Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  db-password: base64encodedpassword
  api-key: base64encodedkey
```

**Best Practices for Configuration:**
1. Version control configurations
2. Use environment-specific configs
3. Implement secret rotation
4. Use proper access controls
5. Monitor configuration usage

[Continue with Security Model and Resource Management sections...]

### 2.7 Security Model

#### 2.7.1 Authentication and Authorization
```ascii
┌─────────────Security Architecture──────────────┐
│                                               │
│  ┌─────────────┐      ┌─────────────┐        │
│  │Authentication│─────►│Authorization │        │
│  │  (Who?)     │      │  (What?)    │        │
│  └─────────────┘      └─────────────┘        │
│         │                    │               │
│         ▼                    ▼               │
│  ┌─────────────┐      ┌─────────────┐        │
│  │ Certificates│      │    RBAC     │        │
│  │   Tokens    │      │   Policies  │        │
│  └─────────────┘      └─────────────┘        │
└───────────────────────────────────────────────┘
```

**RBAC Configuration Example:**
```yaml
# Role Definition
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

---
# RoleBinding
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

**Best Practices:**
1. Follow principle of least privilege
2. Use service accounts for pods
3. Implement network policies
4. Regular security audits
5. Certificate rotation

### 2.8 Resource Management

#### 2.8.1 Resource Quotas and Limits
```ascii
┌─────────────Resource Management──────────────┐
│                                             │
│  ┌─────────────┐      ┌─────────────┐      │
│  │ResourceQuota│      │LimitRange   │      │
│  │(Namespace)  │      │(Per Pod)    │      │
│  └─────────────┘      └─────────────┘      │
│         │                    │             │
│         ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      │
│  │CPU/Memory   │      │Default      │      │
│  │Constraints  │      │Constraints  │      │
│  └─────────────┘      └─────────────┘      │
└─────────────────────────────────────────────┘
```

**ResourceQuota Example:**
```yaml
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
    pods: "10"
```

**LimitRange Example:**
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 512Mi
      cpu: 500m
    defaultRequest:
      memory: 256Mi
      cpu: 200m
    type: Container
```

### 2.9 Advanced Concepts

#### 2.9.1 Custom Resources and Operators
```ascii
┌─────────────Custom Resource Architecture─────────┐
│                                                 │
│  ┌─────────────┐      ┌─────────────┐          │
│  │    CRD      │─────►│  Custom     │          │
│  │Definition   │      │  Resource   │          │
│  └─────────────┘      └─────────────┘          │
│         │                    ▲                 │
│         │                    │                 │
│         ▼                    │                 │
│  ┌─────────────┐      ┌─────────────┐          │
│  │  Operator   │─────►│  Controller │          │
│  │             │      │             │          │
│  └─────────────┘      └─────────────┘          │
└─────────────────────────────────────────────────┘
```

**Custom Resource Definition Example:**
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                size:
                  type: string
                version:
                  type: string
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
    shortNames:
    - db
```

### 2.10 Real-world Implementation Guidelines

#### 2.10.1 Production Readiness Checklist

1. **High Availability Configuration**
   - Multiple master nodes
   - Distributed etcd cluster
   - Node anti-affinity rules
   ```yaml
   affinity:
     podAntiAffinity:
       requiredDuringSchedulingIgnoredDuringExecution:
         - labelSelector:
             matchExpressions:
               - key: app
                 operator: In
                 values:
                 - web-server
           topologyKey: "kubernetes.io/hostname"
   ```

2. **Monitoring and Logging Setup**
   - Prometheus for metrics
   - ELK/EFK stack for logging
   - Custom metrics pipeline
   - Alerting configuration

3. **Backup and Disaster Recovery**
   - Regular etcd backups
   - State backup procedures
   - Recovery testing schedule
   - Disaster recovery documentation

4. **Security Hardening**
   - Network policies
   - Pod security policies
   - RBAC configuration
   - Secret management
   - Regular security audits

5. **Performance Optimization**
   - Resource limits and requests
   - HPA configuration
   - Node pool optimization
   - Storage configuration
   ```yaml
   apiVersion: autoscaling/v2beta2
   kind: HorizontalPodAutoscaler
   metadata:
     name: web-app
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: web-app
     minReplicas: 3
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

[Continue with more implementation guidelines...]

