# Chapter 11: Advanced Kubernetes Concepts

## 1. Custom Resource Definitions (CRDs)

### 1.1 Overview
```ascii
┌─────────────Custom Resources Architecture──────────────┐
│                                                       │
│  ┌─CRD Definition─┐    ┌─Custom Controller─┐         │
│  │               │     │                   │         │
│  │• Schema       │────►│• Reconciliation   │         │
│  │• Validation   │     │• Business Logic   │         │
│  │• Versioning   │     │• Status Updates   │         │
│  └───────────────┘     └───────────────────┘         │
│           ▲                      ▲                    │
│           │                      │                    │
│           ▼                      ▼                    │
│  ┌─Custom Objects─┐    ┌─Kubernetes API─┐            │
│  │               │◄───►│                │            │
│  └───────────────┘     └────────────────┘            │
└───────────────────────────────────────────────────────┘
```

### 1.2 CRD Definition
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.stable.example.com
spec:
  group: stable.example.com
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
                frequency:
                  type: string
                destination:
                  type: string
              required: ["frequency", "destination"]
  scope: Namespaced
  names:
    plural: backups
    singular: backup
    kind: Backup
    shortNames:
    - bk
```

## 2. Advanced Scheduling

### 2.1 Pod Topology Spread Constraints
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
  containers:
  - name: nginx
    image: nginx
```

### 2.2 Node Affinity Rules
```yaml
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
          - key: gpu-type
            operator: In
            values:
            - nvidia-tesla-p100
```

## 3. Advanced Networking

### 3.1 Service Mesh Integration
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
```

### 3.2 Multi-cluster Networking
```yaml
apiVersion: submariner.io/v1alpha1
kind: Submariner
metadata:
  name: submariner
spec:
  broker: k8s
  brokerK8sApiServer: "https://broker-api.example.com:6443"
  brokerK8sApiServerToken: "<token>"
  brokerK8sCA: "<ca-bundle>"
  clusterCIDR: "10.42.0.0/16"
  serviceCIDR: "10.43.0.0/16"
```

## 4. Advanced Security

### 4.1 Pod Security Standards
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 4.2 Advanced RBAC
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
  resourceNames: ["frontend-*"]
```

## 5. Advanced Storage

### 5.1 Storage Capacity Tracking
```yaml
apiVersion: storage.k8s.io/v1
kind: CSIStorageCapacity
metadata:
  name: capacity-info
storageClassName: standard
capacity: 1Ti
maximumVolumeSize: 5Gi
nodeTopology:
  matchLabels:
    topology.kubernetes.io/zone: us-east-1a
```

### 5.2 Volume Snapshots
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: data-snapshot
spec:
  volumeSnapshotClassName: csi-hostpath-snapclass
  source:
    persistentVolumeClaimName: data-pvc
```

## 6. Advanced Workload Management

### 6.1 Pod Disruption Budgets
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: critical-service
```

### 6.2 Vertical Pod Autoscaling
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: app
  updatePolicy:
    updateMode: "Auto"
```

## 7. Advanced Monitoring

### 7.1 Custom Metrics Pipeline
```yaml
apiVersion: custom.metrics.k8s.io/v1beta1
kind: MetricDefinition
metadata:
  name: queue_length
spec:
  query: |
    sum(rabbitmq_queue_messages) by (queue)
```

### 7.2 Advanced Prometheus Rules
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: advanced-alerts
spec:
  groups:
  - name: advanced.rules
    rules:
    - record: job:http_requests:rate5m
      expr: sum(rate(http_requests_total[5m])) by (job)
```

## Best Practices

### 1. Resource Management
```markdown
- Implement proper resource quotas
- Use limit ranges effectively
- Monitor resource usage
- Plan for scaling
- Optimize resource requests
```

### 2. High Availability
```markdown
- Implement proper redundancy
- Use pod anti-affinity
- Configure proper PDBs
- Monitor cluster health
- Plan for disasters
```

### 3. Security
```markdown
- Follow principle of least privilege
- Implement network policies
- Use pod security standards
- Regular security audits
- Monitor security events
```

## Common Pitfalls

### 1. Resource Configuration
```markdown
- Improper resource limits
- Missing quotas
- Poor scaling configuration
- Inadequate monitoring
- Insufficient testing
```

### 2. Security Issues
```markdown
- Overly permissive RBAC
- Missing network policies
- Weak security contexts
- Poor secret management
- Inadequate auditing
```

[Continue with more sections if needed...]
