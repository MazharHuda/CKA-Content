# Chapter 11: Advanced Concepts - Real-world Scenarios

## Scenario 1: Custom Resource Implementation

### Context
A company needs to implement a custom backup solution for their applications running in Kubernetes.

### Requirements
- Automated backup scheduling
- Multiple backup targets
- Backup verification
- Retention management
- Status reporting

### Solution

#### 1. Custom Resource Definition
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.ops.example.com
spec:
  group: ops.example.com
  names:
    kind: Backup
    plural: backups
    singular: backup
    shortNames:
    - bk
  scope: Namespaced
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
            required: ["schedule", "target"]
            properties:
              schedule:
                type: string
                pattern: '^(\d+|\*)(/\d+)?(\s+(\d+|\*)(/\d+)?){4}$'
              target:
                type: string
              retention:
                type: integer
                minimum: 1
          status:
            type: object
            properties:
              lastBackup:
                type: string
              status:
                type: string
                enum: ["Pending", "InProgress", "Completed", "Failed"]
```

#### 2. Custom Controller Implementation
```go
// Backup Controller Structure
type BackupController struct {
    kubeclientset    kubernetes.Interface
    backupclientset  clientset.Interface
    backupLister     listers.BackupLister
    backupSynced     cache.InformerSynced
    workqueue        workqueue.RateLimitingInterface
}

// Reconciliation Loop
func (c *BackupController) syncHandler(key string) error {
    namespace, name, err := cache.SplitMetaNamespaceKey(key)
    backup, err := c.backupLister.Backups(namespace).Get(name)
    
    // Implement backup logic
    if err := c.processBackup(backup); err != nil {
        return err
    }
    
    return nil
}
```

## Scenario 2: Advanced Scheduling Implementation

### Context
A machine learning platform needs to implement complex scheduling requirements for GPU workloads.

### Requirements
- GPU resource management
- Node affinity rules
- Pod topology spread
- Priority-based scheduling
- Resource quotas

### Solution

#### 1. Custom Scheduler Configuration
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
metadata:
  name: gpu-scheduler
profiles:
- schedulerName: gpu-scheduler
  plugins:
    score:
      disabled:
      - name: NodeResourcesBalancedAllocation
      enabled:
      - name: GPUAllocation
        weight: 5
```

#### 2. Pod Configuration with Advanced Scheduling
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-training
spec:
  schedulerName: gpu-scheduler
  priorityClassName: high-priority
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: ml-training
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: nvidia.com/gpu
            operator: Exists
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: ml-training
          topologyKey: kubernetes.io/hostname
  containers:
  - name: training
    image: ml-training:v1
    resources:
      limits:
        nvidia.com/gpu: 1
```

## Scenario 3: Advanced Service Mesh Integration

### Context
An organization needs to implement advanced traffic management and security features using service mesh.

### Requirements
- Traffic routing
- Circuit breaking
- Mutual TLS
- Request tracing
- Service-to-service authentication

### Solution

#### 1. Service Mesh Configuration
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: service-routes
spec:
  hosts:
  - service-a
  http:
  - match:
    - headers:
        end-user:
          exact: beta-tester
    route:
    - destination:
        host: service-a
        subset: v2
  - route:
    - destination:
        host: service-a
        subset: v1
```

#### 2. Security Policy
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
  portLevelMtls:
    8080:
      mode: PERMISSIVE
```

## Scenario 4: Multi-cluster Workload Management

### Context
A global company needs to manage workloads across multiple Kubernetes clusters in different regions.

### Requirements
- Centralized management
- Workload distribution
- Cross-cluster networking
- Unified monitoring
- Disaster recovery

### Solution

#### 1. Cluster Federation Configuration
```yaml
apiVersion: core.kubefed.io/v1beta1
kind: KubeFedConfig
metadata:
  name: kubefed
  namespace: kube-federation-system
spec:
  scope: Namespaced
  controllerDuration:
    availableDelay: 20s
    unavailableDelay: 60s
  leaderElect:
    resourceLock: configmaps
    leaseDuration: 15s
    renewDeadline: 10s
    retryPeriod: 5s
```

#### 2. Federated Deployment
```yaml
apiVersion: types.kubefed.io/v1beta1
kind: FederatedDeployment
metadata:
  name: global-app
  namespace: global
spec:
  template:
    metadata:
      labels:
        app: global-app
    spec:
      replicas: 3
      template:
        spec:
          containers:
          - name: app
            image: global-app:v1
  placement:
    clusters:
    - name: cluster1
    - name: cluster2
  overrides:
  - clusterName: cluster1
    clusterOverrides:
    - path: "/spec/replicas"
      value: 5
```

## Scenario 7: Advanced Storage Orchestration

### Context
A large enterprise needs to implement a sophisticated storage management system for their microservices architecture with varying storage requirements.

### Requirements
- Dynamic storage provisioning
- Storage tiering
- Data replication
- Volume snapshots
- Automated backup/restore

### Solution

#### 1. Multi-tier Storage Classes
```yaml
# High-Performance SSD Storage Class
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: premium-ssd
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  replication-type: regional-pd
  zones: us-central1-a,us-central1-b
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
---
# Standard Storage Class
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  fstype: ext4
reclaimPolicy: Delete
allowVolumeExpansion: true
```

#### 2. Volume Snapshot Configuration
```yaml
# Volume Snapshot Class
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-hostpath-snapclass
driver: hostpath.csi.k8s.io
deletionPolicy: Delete
parameters:
  # snapshot specific parameters

---
# Automated Snapshot Schedule
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: data-snapshot
spec:
  volumeSnapshotClassName: csi-hostpath-snapclass
  source:
    persistentVolumeClaimName: data-pvc
```

#### 3. Automated Backup System
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: volume-backup
spec:
  schedule: "0 1 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:v1
            volumeMounts:
            - name: data-volume
              mountPath: /data
            - name: backup-target
              mountPath: /backup
            env:
            - name: BACKUP_RETENTION
              value: "7"
          volumes:
          - name: data-volume
            persistentVolumeClaim:
              claimName: data-pvc
          - name: backup-target
            persistentVolumeClaim:
              claimName: backup-pvc
```

#### 4. Storage Monitoring and Alerts
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: storage-alerts
spec:
  groups:
  - name: storage.rules
    rules:
    - alert: VolumeUsageHigh
      expr: |
        kubelet_volume_stats_used_bytes /
        kubelet_volume_stats_capacity_bytes > 0.85
      for: 5m
      labels:
        severity: warning
      annotations:
        description: "Volume usage is above 85%"
    - alert: VolumeFullIn24Hours
      expr: |
        predict_linear(kubelet_volume_stats_used_bytes[6h], 24 * 3600) >
        kubelet_volume_stats_capacity_bytes
      for: 5m
      labels:
        severity: critical
```

### Implementation Steps

1. Storage Class Setup:
```bash
# Create storage classes
kubectl apply -f storage-classes.yaml

# Verify creation
kubectl get storageclass
kubectl describe storageclass premium-ssd
```

2. Volume Snapshot Configuration:
```bash
# Enable snapshot feature gates
kubectl apply -f snapshot-controller.yaml
kubectl apply -f snapshot-crd.yaml

# Create snapshot class
kubectl apply -f snapshot-class.yaml
```

3. Backup System Implementation:
```yaml
# Backup PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: backup-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard-storage
  resources:
    requests:
      storage: 500Gi
```

### Best Practices

1. Storage Management
```markdown
- Implement proper storage classes
- Use volume snapshots for backups
- Monitor storage usage
- Plan for capacity
- Regular backup testing
```

2. Performance Optimization
```markdown
- Use appropriate storage types
- Implement caching where needed
- Monitor I/O patterns
- Optimize storage requests
- Regular performance testing
```

3. Data Protection
```markdown
- Regular snapshots
- Automated backups
- Data encryption
- Access controls
- Disaster recovery testing
```

### Common Challenges

1. Storage Issues
```markdown
- Capacity management
- Performance bottlenecks
- Backup consistency
- Recovery procedures
- Cost optimization
```

2. Operational Concerns
```markdown
- Backup window management
- Snapshot retention
- Storage migration
- Version compatibility
- Resource constraints
```

### Monitoring Configuration

1. Storage Metrics
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: storage-monitor
spec:
  selector:
    matchLabels:
      app: storage-metrics
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

2. Performance Dashboards
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: storage-dashboard
data:
  dashboard.json: |
    {
      "panels": [
        {
          "title": "Volume Usage",
          "type": "graph",
          "datasource": "Prometheus",
          "targets": [
            {
              "expr": "kubelet_volume_stats_used_bytes",
              "legendFormat": "{{persistentvolumeclaim}}"
            }
          ]
        }
      ]
    }
```

[Continue with more scenarios if needed...]
