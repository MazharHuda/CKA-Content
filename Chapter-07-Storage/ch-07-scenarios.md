# Chapter 7: Storage - Real-world Scenarios

## Scenario 1: Database Migration with Zero Downtime

### Context
A company needs to migrate their production database from local storage to a cloud-managed storage solution while ensuring zero downtime and data consistency.

### Requirements
- Zero data loss
- Minimal downtime
- Data consistency
- Rollback capability
- Performance monitoring

### Solution

#### 1. Storage Configuration
```yaml
# Source PV (Local Storage)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: source-pv
spec:
  capacity:
    storage: 100Gi
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
          - node1

# Destination PV (Cloud Storage)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: dest-pv
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: cloud-premium
  csi:
    driver: cloud.provider/csi
    volumeHandle: vol-xyz
    fsType: ext4
```

#### 2. Migration Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: db-migration
spec:
  containers:
  - name: migration-tool
    image: migration-tool:v1
    volumeMounts:
    - name: source-data
      mountPath: /source
    - name: dest-data
      mountPath: /dest
    command:
    - "/bin/sh"
    - "-c"
    - |
      rsync -av --progress /source/ /dest/
      echo "Migration completed at $(date)" >> /dest/migration.log
  volumes:
  - name: source-data
    persistentVolumeClaim:
      claimName: source-pvc
  - name: dest-data
    persistentVolumeClaim:
      claimName: dest-pvc
```

### Implementation Steps

1. Prepare Storage
```bash
# Create PVCs
kubectl apply -f source-pvc.yaml
kubectl apply -f dest-pvc.yaml

# Verify PVC binding
kubectl get pvc
kubectl get pv
```

2. Data Migration
```bash
# Start migration pod
kubectl apply -f migration-pod.yaml

# Monitor progress
kubectl logs -f db-migration
```

## Scenario 2: High-Performance Storage for ML Workloads

### Context
A data science team needs to set up storage for their machine learning workloads requiring high IOPS and low latency.

### Requirements
- High IOPS
- Low latency
- Scalable storage
- Data persistence
- Cost optimization

### Solution

#### 1. Storage Class Configuration
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ml-storage
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iopsPerGB: "50"
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

#### 2. StatefulSet for ML Workload
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ml-training
spec:
  serviceName: ml-training
  replicas: 3
  selector:
    matchLabels:
      app: ml-training
  template:
    metadata:
      labels:
        app: ml-training
    spec:
      containers:
      - name: training
        image: ml-training:v1
        resources:
          requests:
            memory: "64Gi"
            cpu: "8"
          limits:
            memory: "128Gi"
            cpu: "16"
        volumeMounts:
        - name: training-data
          mountPath: /data
        - name: model-output
          mountPath: /models
  volumeClaimTemplates:
  - metadata:
      name: training-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: ml-storage
      resources:
        requests:
          storage: 500Gi
  - metadata:
      name: model-output
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: ml-storage
      resources:
        requests:
          storage: 100Gi
```

## Scenario 3: Multi-tenant Storage Management

### Context
A SaaS provider needs to implement storage isolation and resource management for multiple tenants on a shared Kubernetes cluster.

### Requirements
- Storage isolation
- Resource quotas
- Performance guarantees
- Cost tracking
- Security compliance

### Solution

#### 1. Namespace and Quota Setup
```yaml
# Tenant Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-a
  labels:
    tenant: a

# Storage Resource Quota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-a-quota
  namespace: tenant-a
spec:
  hard:
    requests.storage: 500Gi
    persistentvolumeclaims: "10"
```

#### 2. Tenant Storage Class
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: tenant-a-storage
parameters:
  type: gp3
  encrypted: "true"
  kmsKeyId: arn:aws:kms:region:account:key/key-id
provisioner: kubernetes.io/aws-ebs
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

#### 3. Storage Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: storage-policy
  namespace: tenant-a
spec:
  podSelector:
    matchLabels:
      tenant: a
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: a
```

### Implementation Steps

1. Create Tenant Environment
```bash
# Create namespace and quotas
kubectl apply -f tenant-namespace.yaml
kubectl apply -f storage-quota.yaml

# Create storage class
kubectl apply -f tenant-storage-class.yaml
```

2. Monitor Usage
```bash
# Check quota usage
kubectl describe quota -n tenant-a

# Monitor PVC status
kubectl get pvc -n tenant-a
```

## Best Practices

1. Storage Management
```markdown
- Implement proper backup strategies
- Monitor storage usage
- Set up alerts for capacity thresholds
- Regular performance testing
- Document storage policies
```

2. Security
```markdown
- Encrypt data at rest
- Implement access controls
- Regular security audits
- Monitor access patterns
- Maintain compliance requirements
```

3. Performance
```markdown
- Choose appropriate storage class
- Monitor IOPS and latency
- Set resource limits
- Regular performance testing
- Optimize storage configuration
```

## Common Pitfalls

1. Storage Issues
```markdown
- Insufficient capacity planning
- Poor performance configuration
- Missing backup strategies
- Inadequate monitoring
- Improper access controls
```

2. Operational Challenges
```markdown
- Complex migration procedures
- Backup/restore failures
- Performance bottlenecks
- Cost management
- Security vulnerabilities
```

## Monitoring and Alerts

1. Storage Metrics
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: storage-alerts
spec:
  groups:
  - name: storage
    rules:
    - alert: HighStorageUsage
      expr: kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes > 0.85
      for: 5m
      labels:
        severity: warning
      annotations:
        message: Storage usage is above 85% for volume {{ $labels.persistentvolumeclaim }}
```

2. Performance Monitoring
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
```
