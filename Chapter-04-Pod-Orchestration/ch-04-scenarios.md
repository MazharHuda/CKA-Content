# Chapter 4: Pod Orchestration and Scheduling - Real-world Scenarios

## Scenario 1: High-Performance Microservices Deployment

### Context
A financial services company needs to deploy a high-performance trading application consisting of multiple microservices with specific resource and placement requirements.

### Requirements
- Guaranteed resource allocation
- Co-location of related services
- High availability
- Performance monitoring
- Low latency communication

### Solution

#### 1. Pod Configuration with Resource Guarantees
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: trading-service
  labels:
    app: trading
    type: high-priority
spec:
  containers:
  - name: trading-app
    image: trading:v1
    resources:
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 5
```

#### 2. Co-location Strategy
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: market-data-processor
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - trading
        topologyKey: "kubernetes.io/hostname"
  containers:
  - name: processor
    image: market-processor:v1
```

### Implementation Steps
1. Deploy core services with resource guarantees
2. Implement affinity rules
3. Configure monitoring
4. Set up alerts
5. Test performance

## Scenario 2: Multi-tenant Application Platform

### Context
A SaaS provider needs to host multiple customer applications on the same cluster while ensuring isolation and resource fairness.

### Requirements
- Resource isolation
- Network segregation
- Fair resource allocation
- Performance monitoring
- Cost tracking

### Solution

#### 1. Namespace and Resource Quota Setup
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: customer-a
  labels:
    customer: a
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: customer-quota
  namespace: customer-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
```

#### 2. Pod Security and Isolation
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: customer-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          customer: a
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          customer: a
```

## Scenario 3: Edge Computing Deployment

### Context
An IoT company needs to deploy applications across multiple edge locations with limited resources and varying hardware capabilities.

### Requirements
- Resource efficiency
- Hardware awareness
- Automatic recovery
- Local storage handling
- Remote management

### Solution

#### 1. Resource-Aware Pod Scheduling
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: edge-processor
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: edge-capability
            operator: In
            values:
            - "gpu"
            - "high-compute"
  containers:
  - name: processor
    image: edge-app:v1
    resources:
      requests:
        cpu: "500m"
        memory: "512Mi"
      limits:
        cpu: "1"
        memory: "1Gi"
```

#### 2. Local Storage Configuration
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
  local:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - edge-node-1
```

## Scenario 4: Machine Learning Pipeline

### Context
A data science team needs to deploy machine learning training and inference pipelines with specific hardware requirements and data access patterns.

### Requirements
- GPU resource management
- Data pipeline orchestration
- Model serving
- Scalable training
- Resource optimization

### Solution

#### 1. GPU-enabled Training Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-training
spec:
  containers:
  - name: trainer
    image: ml-trainer:v1
    resources:
      limits:
        nvidia.com/gpu: 2
    volumeMounts:
    - name: training-data
      mountPath: /data
    - name: model-output
      mountPath: /output
  volumes:
  - name: training-data
    persistentVolumeClaim:
      claimName: training-data-pvc
  - name: model-output
    persistentVolumeClaim:
      claimName: model-output-pvc
```

#### 2. Inference Service Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: model-server
spec:
  containers:
  - name: inference
    image: model-server:v1
    ports:
    - containerPort: 8080
    resources:
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
    volumeMounts:
    - name: model-store
      mountPath: /models
  volumes:
  - name: model-store
    persistentVolumeClaim:
      claimName: model-store-pvc
```

### Best Practices and Lessons Learned

1. Resource Management
   - Implement proper resource requests and limits
   - Use appropriate QoS classes
   - Monitor resource usage
   - Set up autoscaling

2. High Availability
   - Use pod anti-affinity for redundancy
   - Implement proper health checks
   - Configure pod disruption budgets
   - Plan for node failures

3. Security
   - Implement network policies
   - Use security contexts
   - Configure RBAC properly
   - Regular security audits

4. Monitoring and Maintenance
   - Set up comprehensive monitoring
   - Implement proper logging
   - Regular performance reviews
   - Automated recovery procedures