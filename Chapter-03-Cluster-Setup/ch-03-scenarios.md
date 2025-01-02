# Chapter 3: Cluster Setup and Configuration - Real-world Scenarios

## Scenario 1: Enterprise Multi-Region Cluster Deployment

### Context
A global e-commerce company needs to deploy a highly available Kubernetes cluster across multiple regions to serve customers worldwide.

### Requirements
- High availability across regions
- Disaster recovery capabilities
- Consistent performance
- Security compliance
- Automated scaling

### Solution

#### 1. Architecture Design
```ascii
┌─────────────Region A─────────────┐  ┌─────────────Region B─────────────┐
│                                  │  │                                   │
│    ┌─────────┐    ┌─────────┐   │  │    ┌─────────┐    ┌─────────┐    │
│    │Control  │    │Control  │   │  │    │Control  │    │Control  │    │
│    │Plane 1  │    │Plane 2  │   │  │    │Plane 1  │    │Plane 2  │    │
│    └────┬────┘    └────┬────┘   │  │    └────┬────┘    └────┬────┘    │
│         │              │        │  │         │              │         │
│    ┌────┴────┐    ┌────┴────┐   │  │    ┌────┴────┐    ┌────┴────┐    │
│    │ Worker  │    │ Worker  │   │  │    │ Worker  │    │ Worker  │    │
│    │Node 1   │    │Node 2   │   │  │    │Node 1   │    │Node 2   │    │
│    └─────────┘    └─────────┘   │  │    └─────────┘    └─────────┘    │
│                                  │  │                                   │
└──────────────────────────────────┘  └───────────────────────────────────┘
                   │                                    │
                   └────────────────┬─────────────────┘
                                   │
                            ┌──────┴──────┐
                            │Global Load  │
                            │Balancer    │
                            └─────────────┘
```

#### 2. Implementation Steps

##### 2.1 Control Plane Setup
```yaml
# Regional Load Balancer Configuration
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
spec:
  type: LoadBalancer
  ports:
  - port: 6443
    targetPort: 6443
  selector:
    component: kube-apiserver
```

##### 2.2 etcd Configuration
```yaml
# etcd Cluster Configuration
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
    - --initial-cluster=etcd0=https://192.168.1.10:2380,etcd1=https://192.168.1.11:2380
    - --initial-cluster-state=new
    - --initial-cluster-token=etcd-cluster-1
    image: k8s.gcr.io/etcd:3.5.1
```

## Scenario 2: Financial Services Security Compliance

### Context
A banking institution needs to implement a Kubernetes cluster that meets strict security and compliance requirements.

### Requirements
- End-to-end encryption
- Audit logging
- Access control
- Network segmentation
- Compliance monitoring

### Solution

#### 1. Security Implementation

##### 1.1 Network Policy Configuration
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pci-compliance
spec:
  podSelector:
    matchLabels:
      compliance: pci
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
      port: 443
  egress:
  - to:
    - podSelector:
        matchLabels:
          role: database
    ports:
    - protocol: TCP
      port: 5432
```

##### 1.2 Audit Policy Configuration
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: compliance-audit-policy
rules:
- level: RequestResponse
  resources:
  - group: ""
    resources: ["secrets", "configmaps"]
- level: Metadata
  resources:
  - group: ""
    resources: ["pods", "services"]
```

## Scenario 3: Large-Scale Data Processing Cluster

### Context
A data analytics company needs to process large amounts of data using Kubernetes.

### Requirements
- High performance storage
- Efficient scheduling
- Resource optimization
- Scalable architecture
- Monitoring and analytics

### Solution

#### 1. Storage Configuration
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: high-performance
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iopsPerGB: "50"
  encrypted: "true"
volumeBindingMode: WaitForFirstConsumer
```

#### 2. Resource Management
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    requests.cpu: "30"
    requests.memory: 100Gi
    limits.cpu: "40"
    limits.memory: 200Gi
    requests.nvidia.com/gpu: 4
```

## Scenario 4: Automated Disaster Recovery

### Context
A healthcare provider needs to implement automated disaster recovery for their Kubernetes cluster.

### Requirements
- Zero data loss
- Minimal downtime
- Automated failover
- Data compliance
- Regular testing

### Solution

#### 1. Backup Configuration
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
spec:
  schedule: "0 0 * * *"
  template:
    includedNamespaces:
    - default
    - kube-system
    includedResources:
    - deployments
    - statefulsets
    - configmaps
    - secrets
    storageLocation: aws-backup
    volumeSnapshotLocations:
    - aws-snapshot
```

#### 2. Failover Automation
```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: health-check
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: health-check
            image: health-check:v1
            command:
            - /scripts/check-cluster-health.sh
```

### Best Practices and Lessons Learned

1. Deployment Strategy
   - Use Infrastructure as Code
   - Implement gradual rollouts
   - Maintain configuration version control
   - Regular disaster recovery testing

2. Monitoring and Alerting
   - Implement comprehensive monitoring
   - Set up alerting thresholds
   - Regular metric review
   - Automated response procedures

3. Security Considerations
   - Regular security audits
   - Certificate rotation
   - Access review
   - Compliance checking

4. Performance Optimization
   - Resource usage monitoring
   - Scaling thresholds review
   - Storage optimization
   - Network performance tuning