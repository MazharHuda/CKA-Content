# Chapter 10: Kubernetes Cluster Maintenance

## 1. Cluster Upgrade Process

### 1.1 Upgrade Planning
```ascii
┌─────────────Kubernetes Version Skew Policy──────────────┐
│                                                        │
│  ┌─Control Plane─┐   ┌─kubelet─┐   ┌─kubectl─┐        │
│  │ Can be ahead  │   │ Can be  │   │ Can be  │        │
│  │ of kubelet by │   │ behind  │   │ +/-1    │        │
│  │ up to 2 minor │   │ control │   │ minor   │        │
│  │ versions      │   │ plane   │   │ version │        │
│  └──────────────┘   └─────────┘   └─────────┘        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 1.2 Upgrade Steps
1. Control Plane Components
```bash
# Check current versions
kubectl version
kubectl get nodes

# Drain control plane node
kubectl drain <node-name> --ignore-daemonsets

# Upgrade kubeadm
apt-get update && \
apt-get install -y kubeadm=1.xx.x-00

# Plan the upgrade
kubeadm upgrade plan

# Apply the upgrade
kubeadm upgrade apply v1.xx.x
```

2. Worker Node Components
```bash
# Drain worker node
kubectl drain <node-name> --ignore-daemonsets

# Upgrade kubelet and kubectl
apt-get update && \
apt-get install -y kubelet=1.xx.x-00 kubectl=1.xx.x-00
systemctl daemon-reload
systemctl restart kubelet

# Uncordon node
kubectl uncordon <node-name>
```

## 2. Backup and Restore

### 2.1 etcd Backup
```yaml
# Backup Configuration
apiVersion: v1
kind: Pod
metadata:
  name: etcd-backup
spec:
  containers:
  - name: backup
    image: k8s.gcr.io/etcd:3.5.1
    command:
    - /bin/sh
    - -c
    - |
      ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db \
      --endpoints=https://127.0.0.1:2379 \
      --cacert=/etc/kubernetes/pki/etcd/ca.crt \
      --cert=/etc/kubernetes/pki/etcd/server.crt \
      --key=/etc/kubernetes/pki/etcd/server.key
```

### 2.2 Resource Backup
```bash
# Backup all resources
kubectl get all --all-namespaces -o yaml > all-resources.yaml

# Backup specific resources
kubectl get deployments,services,configmaps,secrets \
  -n production -o yaml > production-backup.yaml
```

## 3. Node Maintenance

### 3.1 Node Operations
```ascii
┌─────────────Node Maintenance Process──────────────┐
│                                                  │
│  1. Drain Node    2. Perform     3. Uncordon     │
│     ┌─────┐         Maintenance    ┌─────┐       │
│     │Drain│         ┌─────┐        │Ready│       │
│     └──┬──┘         │Work │        └──┬──┘       │
│        │            └─────┘           │          │
│        ▼                              ▼          │
│  Pods Evicted                   Node Available   │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 3.2 Node Management Commands
```bash
# Cordon node (mark as unschedulable)
kubectl cordon node-1

# Drain node
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data

# Uncordon node
kubectl uncordon node-1
```

## 4. System Upgrades

### 4.1 Operating System Updates
```yaml
# Node Update Strategy
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-updater
spec:
  template:
    spec:
      containers:
      - name: updater
        image: system-updater:1.0
        securityContext:
          privileged: true
        volumeMounts:
        - name: host-root
          mountPath: /host
      volumes:
      - name: host-root
        hostPath:
          path: /
```

### 4.2 Container Runtime Updates
```bash
# Container Runtime Update Steps
systemctl stop kubelet
systemctl stop containerd

# Update containerd
apt-get update && apt-get install -y containerd.io

# Restart services
systemctl start containerd
systemctl start kubelet
```

## 5. Certificate Management

### 5.1 Certificate Renewal
```yaml
# Certificate Check
kubeadm certs check-expiration

# Certificate Renewal
kubeadm certs renew all
```

### 5.2 Certificate Configuration
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: new-cert
spec:
  request: <base64-encoded-csr>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

## 6. High Availability Maintenance

### 6.1 Control Plane HA
```ascii
┌─────────────HA Control Plane──────────────┐
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │Master-1 │  │Master-2 │  │Master-3 │   │
│  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │           │            │         │
│  ┌────▼───────────▼────────────▼────┐    │
│  │         Load Balancer           │    │
│  └─────────────────────────────────┘    │
│                                          │
└──────────────────────────────────────────┘
```

### 6.2 etcd Cluster Maintenance
```bash
# Check etcd cluster health
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key

# Remove etcd member
ETCDCTL_API=3 etcdctl member remove <member-id>
```

## 7. Troubleshooting During Maintenance

### 7.1 Common Issues
1. Node Problems
```bash
# Check node conditions
kubectl describe node <node-name>

# Check system logs
journalctl -u kubelet

# Check pod status
kubectl get pods --all-namespaces -o wide
```

2. Control Plane Issues
```bash
# Check control plane pods
kubectl get pods -n kube-system

# Check API server logs
kubectl logs -n kube-system kube-apiserver-<node-name>
```

### 7.2 Recovery Procedures
```bash
# Restore etcd from backup
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir /var/lib/etcd-restore

# Reset kubeadm
kubeadm reset

# Reinitialize cluster
kubeadm init --config=config.yaml
```

## Best Practices

### 1. Maintenance Planning
```markdown
- Schedule maintenance during off-peak hours
- Communicate maintenance windows
- Have rollback plans ready
- Test procedures in staging
- Monitor system during maintenance
```

### 2. Backup Strategy
```markdown
- Regular etcd backups
- Resource backups
- Configuration backups
- Test restore procedures
- Document backup locations
```

### 3. High Availability
```markdown
- Maintain multiple control plane nodes
- Use load balancers
- Implement proper monitoring
- Regular failover testing
- Document recovery procedures
```

## Common Pitfalls

### 1. Upgrade Issues
```markdown
- Skipping version compatibility checks
- Not backing up before upgrades
- Insufficient resource planning
- Missing dependency updates
- Incomplete rollback plans
```

### 2. Maintenance Problems
```markdown
- Inadequate testing
- Poor communication
- Missing documentation
- Incomplete backups
- Resource exhaustion
```

[Continue with more sections if needed...]
