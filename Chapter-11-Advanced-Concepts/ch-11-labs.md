# Chapter 11: Advanced Concepts - Practice Labs

## Prerequisites
- Running Kubernetes cluster
- kubectl CLI tool configured
- Helm installed
- Basic understanding of advanced Kubernetes concepts

## Lab 1: source Definitions (CRDs)Custom 
![source Definitions (CRDs)Custom ](/Images/chapter11/ch11_lab01_crd_creation.png)
![source Definitions (CRDs)Custom Controller](/Images/chapter11/ch11_lab01_controller.png)
![source Definitions (CRDs)Custom Interaction](/Images/chapter11/ch11_lab01_interaction.png)
### Objective
Create and manage custom resources in Kubernetes.

### Tasks

1. Create a Custom Resource Definition:
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
                retention:
                  type: integer
              required: ["frequency", "destination"]
  scope: Namespaced
  names:
    plural: backups
    singular: backup
    kind: Backup
    shortNames:
    - bk
```

2. Create Custom Resource:
```yaml
apiVersion: stable.example.com/v1
kind: Backup
metadata:
  name: daily-backup
spec:
  frequency: "0 0 * * *"
  destination: "s3://my-bucket/backups"
  retention: 7
```

## Lab 2: Advanced Scheduling
![Advanced Scheduling](/Images/chapter11/ch11_lab02_topology_spread.png)
![Node Affinity](/Images/chapter11/ch11_lab02_node_affinity.png)
![Strategy](/Images/chapter11/ch11_lab02_strategy.png)


### Objective
Implement complex scheduling scenarios using pod topology spread constraints and affinity rules.

### Tasks

1. Create Pod with Topology Spread Constraints:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
  labels:
    app: web
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

2. Implement Node Affinity:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gpu-app
  template:
    metadata:
      labels:
        app: gpu-app
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
      containers:
      - name: gpu-container
        image: gpu-app:1.0
```

## Lab 3: Advanced Networking
![Advanced Networking](/Images/chapter11/ch11_lab03_network_policy.png)
![Advanced Networking Service Mesh](/Images/chapter11/ch11_lab03_service_mesh.png)
![Advanced Config](/Images/chapter11/ch11_lab03_advanced_config.png)
### Objective
Configure advanced networking features including network policies and service mesh integration.

### Tasks

1. Implement Network Policies:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

2. Configure Service Mesh (Istio):
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

## Lab 4: Advanced Storage Configuration
![Advanced Storage Configuration](/Images/chapter11/ch11_lab04_storage_class.png)
![Advanced Storage Snapshot](/Images/chapter11/ch11_lab04_snapshots.png)
![Advanced ](/Images/chapter11/ch11_lab04_advanced.png)
![Advanced Workload Management Strategy](/Images/chapter11/ch11_lab05_strategy.png)
### Objective
Implement advanced storage features including storage classes and volume snapshots.

### Tasks

1. Create Custom Storage Class:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-ssd
  fstype: ext4
  replication-type: none
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

2. Configure Volume Snapshots:
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

## Lab 5: Advanced Workload Management
![Advanced Workload Management](/Images/chapter11/ch11_lab05_pdb.png)
![Advanced Workload Management VPA](/Images/chapter11/ch11_lab05_vpa.png)


### Objective
Implement advanced workload features including pod disruption budgets and vertical pod autoscaling.

### Tasks

1. Create Pod Disruption Budget:
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

2. Configure Vertical Pod Autoscaling:
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

## Verification Tasks

1. Verify CRD Implementation:
```bash
# Check CRD registration
kubectl get crd
kubectl describe crd backups.stable.example.com

# Verify custom resource
kubectl get backups
kubectl describe backup daily-backup
```

2. Test Advanced Scheduling:
```bash
# Verify pod placement
kubectl get pods -o wide
kubectl describe pod web-server

# Check node affinity
kubectl get nodes --show-labels
```

3. Verify Network Policies:
```bash
# Test network connectivity
kubectl exec -it frontend-pod -- curl api-service:8080
kubectl exec -it test-pod -- curl api-service:8080
```

## Best Practices

1. Resource Management
```markdown
- Use proper resource requests and limits
- Implement pod disruption budgets
- Configure appropriate scheduling constraints
- Monitor resource usage
- Plan for scaling
```

2. Security
```markdown
- Implement network policies
- Use pod security standards
- Configure service accounts properly
- Regular security audits
- Monitor security events
```

## Cleanup

```bash
# Remove CRD resources
kubectl delete crd backups.stable.example.com
kubectl delete -f network-policy.yaml
kubectl delete -f storage-class.yaml
```

## Tips for CKA Exam

1. Understand CRD concepts and implementation
2. Master advanced scheduling configurations
3. Know how to troubleshoot network policies
4. Be familiar with storage class configuration
5. Practice workload management scenarios
