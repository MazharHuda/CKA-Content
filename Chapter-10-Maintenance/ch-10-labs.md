# Chapter 10: Maintenance - Practice Labs

## Prerequisites
- Running Kubernetes cluster
- kubectl CLI tool configured
- Access to cluster nodes
- Basic understanding of Kubernetes maintenance concepts

## Lab 1: Cluster Upgrade Process
![Cluster Upgrade Process](/Images/chapter10/ch10_lab01_upgrade_process.png)
### Objective
Perform a Kubernetes cluster upgrade following the proper procedures and best practices.

### Tasks

1. Pre-upgrade Checks:
```bash
# Check current versions
kubectl version
kubectl get nodes

# Check cluster health
kubectl get pods --all-namespaces
kubectl get componentstatuses

# Backup etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

2. Control Plane Upgrade:
```bash
# Drain control plane node
kubectl drain <control-plane-node> --ignore-daemonsets

# Upgrade kubeadm
apt-mark unhold kubeadm
apt-get update && apt-get install -y kubeadm=1.xx.x-00
apt-mark hold kubeadm

# Plan and apply upgrade
kubeadm upgrade plan
kubeadm upgrade apply v1.xx.x

# Upgrade kubelet and kubectl
apt-mark unhold kubelet kubectl
apt-get update && apt-get install -y kubelet=1.xx.x-00 kubectl=1.xx.x-00
apt-mark hold kubelet kubectl

# Restart kubelet
systemctl daemon-reload
systemctl restart kubelet

# Uncordon node
kubectl uncordon <control-plane-node>
```

## Lab 2: Node Maintenance
![Node Maintenances](/Images/chapter10/ch10_lab02_node_maintenance.png)

### Objective
Perform maintenance tasks on cluster nodes while ensuring workload availability.

### Tasks

1. Prepare Node for Maintenance:
```bash
# Check pods running on node
kubectl get pods -o wide | grep <node-name>

# Drain node
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Verify pods are rescheduled
kubectl get pods -o wide
```

2. Perform Maintenance:
```bash
# Stop kubelet
systemctl stop kubelet

# Perform system updates
apt-get update && apt-get upgrade -y

# Restart kubelet
systemctl start kubelet
```

3. Return Node to Service:
```bash
# Uncordon node
kubectl uncordon <node-name>

# Verify node status
kubectl get nodes
kubectl describe node <node-name>
```

## Lab 3: Backup and Restore
![Backup and Restore](/Images/chapter10/ch10_lab03_backup.png)

### Objective
Implement and test backup and restore procedures for cluster data.

### Tasks

1. Backup etcd:
```yaml
# Create backup job
apiVersion: batch/v1
kind: Job
metadata:
  name: etcd-backup
spec:
  template:
    spec:
      containers:
      - name: etcd-backup
        image: k8s.gcr.io/etcd:3.5.1
        command:
        - /bin/sh
        - -c
        - |
          ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot-$(date +%Y%m%d).db \
          --endpoints=https://127.0.0.1:2379 \
          --cacert=/etc/kubernetes/pki/etcd/ca.crt \
          --cert=/etc/kubernetes/pki/etcd/server.crt \
          --key=/etc/kubernetes/pki/etcd/server.key
        volumeMounts:
        - name: etcd-certs
          mountPath: /etc/kubernetes/pki/etcd
        - name: backup
          mountPath: /backup
      volumes:
      - name: etcd-certs
        hostPath:
          path: /etc/kubernetes/pki/etcd
      - name: backup
        hostPath:
          path: /var/lib/etcd-backup
```

2. Restore from Backup:
![Backup and Restore](/Images/chapter10/ch10_lab03_restore.png)
```bash
# Stop kube-apiserver
systemctl stop kube-apiserver

# Restore etcd data
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir /var/lib/etcd-restore

# Update etcd configuration
sed -i 's/\/var\/lib\/etcd/\/var\/lib\/etcd-restore/g' \
  /etc/kubernetes/manifests/etcd.yaml

# Restart services
systemctl restart kubelet
systemctl start kube-apiserver
```

## Lab 4: Certificate Management
![Certificate Management](/Images/chapter10/ch10_lab04_cert_management.png)
![Certificate CsrFlow](/Images/chapter10/ch10_lab04_csr_flow.png)
![Certificate Cert rotation](/Images/chapter10/ch10_lab04_cert_rotation.png)

### Objective
Manage and rotate cluster certificates.

### Tasks

1. Check Certificate Expiration:
```bash
# Check certificate expiration
kubeadm certs check-expiration

# List all certificates
ls -l /etc/kubernetes/pki/
```

2. Renew Certificates:
```bash
# Renew all certificates
kubeadm certs renew all

# Verify renewal
kubeadm certs check-expiration
```

3. Create New Certificate:
```yaml
# Create Certificate Signing Request
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: new-admin
spec:
  request: <base64-encoded-csr>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

## Lab 5: Troubleshooting Scenarios
![Troubleshooting Scenarios](/Images/chapter10/ch10_lab05_recovery.png)
![Node Troubleshooting Scenarios](/Images/chapter10/ch10_lab05_node_troubleshooting.png)
![Control_Plane](/Images/chapter10/ch10_lab05_control_plane.png)
### Scenario 1: Node Problems

1. Investigate Node Issues:
```bash
# Check node status
kubectl describe node <node-name>

# Check kubelet status
systemctl status kubelet
journalctl -u kubelet

# Check system resources
top
df -h
```

### Scenario 2: Control Plane Recovery

1. Recover Failed Control Plane:
```bash
# Check control plane pods
kubectl get pods -n kube-system

# Check pod logs
kubectl logs -n kube-system kube-apiserver-<node-name>

# Check static pod manifests
ls -l /etc/kubernetes/manifests/
```

## Verification Tasks

1. Upgrade Verification:
```bash
# Verify component versions
kubectl version
kubectl get nodes
kubectl get pods -n kube-system
```

2. Backup Verification:
```bash
# Test backup integrity
ETCDCTL_API=3 etcdctl snapshot status snapshot.db

# Verify backup contents
ETCDCTL_API=3 etcdctl --write-out=table snapshot status snapshot.db
```

## Best Practices

1. Maintenance Planning
```markdown
- Schedule maintenance during off-peak hours
- Communicate maintenance windows
- Have rollback plans ready
- Test procedures in staging
- Monitor system during maintenance
```

2. Backup Strategy
```markdown
- Regular etcd backups
- Resource backups
- Configuration backups
- Test restore procedures
- Document backup locations
```

## Cleanup

```bash
# Remove test resources
kubectl delete job etcd-backup
kubectl delete csr new-admin
```

## Tips for CKA Exam

1. Master the upgrade process steps
2. Know how to backup and restore etcd
3. Understand certificate management
4. Practice troubleshooting scenarios
5. Be familiar with node maintenance procedures
