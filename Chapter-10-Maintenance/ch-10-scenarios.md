# Chapter 10: Maintenance - Real-world Scenarios

## Scenario 1: Cluster Upgrade in Production Environment

### Context
A company needs to upgrade their production Kubernetes cluster from version 1.23 to 1.24 with minimal downtime.

### Requirements
- Zero downtime for critical applications
- Proper backup procedures
- Rollback capability
- Minimal impact on workloads
- Compliance with maintenance windows

### Solution

#### 1. Pre-upgrade Planning
```yaml
# Resource Assessment
apiVersion: v1
kind: ResourceQuota
metadata:
  name: upgrade-quota
spec:
  hard:
    cpu: "16"
    memory: "32Gi"
    pods: "20"
```

#### 2. Backup Configuration
```yaml
# Backup Job
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
          ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-$(date +%Y%m%d).db \
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

### Implementation Steps

1. Pre-upgrade Checks:
```bash
# Version verification
kubeadm version
kubectl version --short

# Component health check
kubectl get componentstatuses
kubectl get nodes
kubectl get pods --all-namespaces
```

2. Node Upgrade Process:
```bash
# For each control plane node
kubectl drain <node-name> --ignore-daemonsets
apt-get update && apt-get install -y kubeadm=1.24.x-00
kubeadm upgrade plan
kubeadm upgrade apply v1.24.x
apt-get install -y kubelet=1.24.x-00 kubectl=1.24.x-00
systemctl restart kubelet
kubectl uncordon <node-name>
```

## Scenario 2: Disaster Recovery Implementation

### Context
An organization needs to implement comprehensive disaster recovery procedures for their Kubernetes cluster.

### Requirements
- Regular automated backups
- Quick recovery capability
- Data integrity verification
- Cross-region recovery
- Documented procedures

### Solution

#### 1. Automated Backup System
```yaml
# Backup CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cluster-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:v1
            command:
            - /backup-script.sh
            env:
            - name: BACKUP_LOCATION
              value: "s3://cluster-backups"
            - name: RETENTION_DAYS
              value: "30"
```

#### 2. Recovery Procedure
```yaml
# Recovery Job
apiVersion: batch/v1
kind: Job
metadata:
  name: cluster-restore
spec:
  template:
    spec:
      containers:
      - name: restore
        image: restore-tool:v1
        command:
        - /restore-script.sh
        env:
        - name: BACKUP_FILE
          value: "backup-20231201.tar.gz"
```

## Scenario 3: High Availability Maintenance

### Context
A financial services company needs to perform maintenance on their HA Kubernetes cluster while maintaining service availability.

### Requirements
- No service interruption
- Load balancer reconfiguration
- Certificate rotation
- Component updates
- Performance monitoring

### Solution

#### 1. Load Balancer Configuration
```yaml
# HAProxy Configuration
global
    log /dev/log local0
    stats socket /var/run/haproxy.sock mode 600 level admin

frontend kubernetes
    bind *:6443
    mode tcp
    option tcplog
    default_backend kubernetes-masters

backend kubernetes-masters
    mode tcp
    balance roundrobin
    option tcp-check
    server master1 192.168.1.10:6443 check fall 3 rise 2
    server master2 192.168.1.11:6443 check fall 3 rise 2
    server master3 192.168.1.12:6443 check fall 3 rise 2
```

#### 2. Certificate Rotation
```yaml
# Certificate Renewal Job
apiVersion: batch/v1
kind: Job
metadata:
  name: cert-renewal
spec:
  template:
    spec:
      containers:
      - name: cert-renewer
        image: cert-tool:v1
        command:
        - /bin/sh
        - -c
        - |
          kubeadm certs check-expiration
          kubeadm certs renew all
```

## Scenario 4: Node Maintenance Strategy

### Context
A company needs to implement a systematic approach for node maintenance across their large Kubernetes cluster.

### Requirements
- Automated node draining
- Workload migration
- OS updates
- Health verification
- Minimal disruption

### Solution

#### 1. Node Maintenance Controller
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-maintainer
spec:
  template:
    spec:
      containers:
      - name: maintainer
        image: node-maintainer:v1
        env:
        - name: MAX_UNAVAILABLE
          value: "20%"
        - name: MAINTENANCE_WINDOW
          value: "0 2 * * SAT"
```

#### 2. Update Strategy
```yaml
# Node Update DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-updater
spec:
  template:
    spec:
      containers:
      - name: updater
        image: system-updater:v1
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

## Scenario 5: ETCD Cluster Maintenance and Management

### Context
A company needs to implement comprehensive etcd maintenance procedures for their production Kubernetes cluster to ensure data consistency and high availability.

### Requirements
- Regular backups
- Performance optimization
- High availability
- Data consistency
- Disaster recovery

### Solution

#### 1. ETCD Backup Configuration
```yaml
# Automated Backup CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etcd-backup
  namespace: kube-system
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
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
              ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot-$(date +%Y%m%d-%H%M%S).db \
                --endpoints=https://127.0.0.1:2379 \
                --cacert=/etc/kubernetes/pki/etcd/ca.crt \
                --cert=/etc/kubernetes/pki/etcd/server.crt \
                --key=/etc/kubernetes/pki/etcd/server.key
            volumeMounts:
            - name: etcd-certs
              mountPath: /etc/kubernetes/pki/etcd
              readOnly: true
            - name: backup
              mountPath: /backup
          volumes:
          - name: etcd-certs
            hostPath:
              path: /etc/kubernetes/pki/etcd
              type: Directory
          - name: backup
            persistentVolumeClaim:
              claimName: etcd-backup-pvc
```

#### 2. ETCD Performance Monitoring
```yaml
# Prometheus ServiceMonitor for etcd
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: etcd-monitor
  namespace: monitoring
spec:
  endpoints:
  - interval: 30s
    port: metrics
    scheme: https
    tlsConfig:
      caFile: /etc/prometheus/secrets/etcd-client-cert/ca.crt
      certFile: /etc/prometheus/secrets/etcd-client-cert/tls.crt
      keyFile: /etc/prometheus/secrets/etcd-client-cert/tls.key
      serverName: localhost
  selector:
    matchLabels:
      k8s-app: etcd
```

#### 3. ETCD Defragmentation Job
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etcd-defrag
  namespace: kube-system
spec:
  schedule: "0 0 * * 6"  # Weekly on Saturday
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: etcd-defrag
            image: k8s.gcr.io/etcd:3.5.1
            command:
            - /bin/sh
            - -c
            - |
              ETCDCTL_API=3 etcdctl defrag \
                --endpoints=https://127.0.0.1:2379 \
                --cacert=/etc/kubernetes/pki/etcd/ca.crt \
                --cert=/etc/kubernetes/pki/etcd/server.crt \
                --key=/etc/kubernetes/pki/etcd/server.key
            volumeMounts:
            - name: etcd-certs
              mountPath: /etc/kubernetes/pki/etcd
              readOnly: true
          volumes:
          - name: etcd-certs
            hostPath:
              path: /etc/kubernetes/pki/etcd
              type: Directory
```

### Implementation Steps

1. Backup Verification Process:
```bash
# Verify backup integrity
ETCDCTL_API=3 etcdctl snapshot status snapshot.db --write-out=table

# Test restore process
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir /var/lib/etcd-backup-test

# Validate restored data
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 get / --prefix --keys-only
```

2. Performance Monitoring:
```yaml
# Alert Rules for etcd
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: etcd-alerts
spec:
  groups:
  - name: etcd.rules
    rules:
    - alert: EtcdHighCommitDurations
      expr: histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m])) > 0.1
      for: 10m
      labels:
        severity: warning
      annotations:
        description: "Etcd commit durations are high"
    - alert: EtcdHighFsyncDurations
      expr: histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m])) > 0.1
      for: 10m
      labels:
        severity: warning
      annotations:
        description: "Etcd WAL fsync durations are high"
```

3. Member Management:
```bash
# Health check script
#!/bin/bash
ENDPOINTS="https://10.0.0.1:2379,https://10.0.0.2:2379,https://10.0.0.3:2379"
ETCDCTL_API=3 etcdctl \
  --endpoints=$ENDPOINTS \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint health --cluster

# Member list check
ETCDCTL_API=3 etcdctl \
  --endpoints=$ENDPOINTS \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  member list -w table
```

### Best Practices

1. Backup Strategy
```markdown
- Regular automated backups
- Multiple backup locations
- Backup verification
- Restore testing
- Retention management
```

2. Performance Optimization
```markdown
- Regular defragmentation
- Monitor WAL size
- Track DB size
- Optimize snapshot frequency
- Monitor latency metrics
```

3. High Availability
```markdown
- Distribute members across zones
- Use proper quorum size
- Monitor member health
- Implement failover testing
- Document recovery procedures
```

### Common Pitfalls

1. Operational Issues
```markdown
- Insufficient monitoring
- Missing backups
- Poor performance tuning
- Inadequate security
- Improper maintenance windows
```

2. Configuration Problems
```markdown
- Incorrect TLS setup
- Insufficient resources
- Poor network configuration
- Missing alerts
- Inadequate logging
```

[Continue with more scenarios if needed...]
