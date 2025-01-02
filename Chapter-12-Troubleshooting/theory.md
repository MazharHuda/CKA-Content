# Chapter 12: Kubernetes Troubleshooting

## 1. Cluster-level Troubleshooting

### 1.1 Control Plane Components
```ascii
┌─────────────Control Plane Troubleshooting──────────────┐
│                                                        │
│  ┌─API Server─┐   ┌─Controller Manager─┐   ┌─etcd─┐   │
│  │• Logs     │   │• Component Status  │   │• Data │   │
│  │• Events   │   │• Pod Status       │   │• Backup│   │
│  │• Certs    │   │• Configurations   │   │• Sync  │   │
│  └───────────┘   └──────────────────┘   └───────┘   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 1.2 Common Commands
```bash
# Check component status
kubectl get componentstatuses

# View API server logs
kubectl logs -n kube-system kube-apiserver-master

# Check etcd health
ETCDCTL_API=3 etcdctl endpoint health \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

## 2. Node Troubleshooting

### 2.1 Node Health Checks
```yaml
# Node Status Check
apiVersion: v1
kind: Node
metadata:
  name: worker-1
status:
  conditions:
  - type: Ready
    status: "True"
  - type: DiskPressure
    status: "False"
  - type: MemoryPressure
    status: "False"
  - type: PIDPressure
    status: "False"
  - type: NetworkUnavailable
    status: "False"
```

### 2.2 Kubelet Issues
```bash
# Check kubelet status
systemctl status kubelet

# View kubelet logs
journalctl -u kubelet

# Check kubelet configuration
ps aux | grep kubelet
```

## 3. Pod Troubleshooting

### 3.1 Pod Lifecycle Issues
```yaml
# Pod Status Analysis
apiVersion: v1
kind: Pod
metadata:
  name: troubleshoot-pod
spec:
  containers:
  - name: app
    image: nginx
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 3
```

### 3.2 Common Pod Problems
1. Image Pull Issues
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check image pull secrets
kubectl get secrets | grep docker
```

2. Resource Constraints
```bash
# Check resource usage
kubectl top pod <pod-name>

# View resource limits
kubectl describe pod <pod-name> | grep -A 3 Limits
```

## 4. Network Troubleshooting

### 4.1 Service Connectivity
```yaml
# Service Debug Pod
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  containers:
  - name: debug
    image: nicolaka/netshoot
    command: ['sh', '-c', 'sleep 3600']
```

### 4.2 DNS Issues
```bash
# Check DNS configuration
kubectl exec -it debug-pod -- cat /etc/resolv.conf

# Test DNS resolution
kubectl exec -it debug-pod -- nslookup kubernetes.default
```

## 5. Storage Troubleshooting

### 5.1 Volume Issues
```yaml
# PV/PVC Status Check
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
```

### 5.2 Storage Class Problems
```bash
# Check storage class
kubectl get sc

# View PVC events
kubectl describe pvc <pvc-name>
```

## 6. Application Debugging

### 6.1 Container Logs
```bash
# View container logs
kubectl logs <pod-name> -c <container-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# View previous container logs
kubectl logs --previous <pod-name>
```

### 6.2 Exec into Containers
```bash
# Interactive shell
kubectl exec -it <pod-name> -- /bin/sh

# Run specific command
kubectl exec <pod-name> -- ps aux
```

## 7. Performance Analysis

### 7.1 Resource Monitoring
```bash
# Node resource usage
kubectl top nodes

# Pod resource usage
kubectl top pods --containers

# Detailed node description
kubectl describe node <node-name>
```

### 7.2 Event Analysis
```bash
# View cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# Watch events in real-time
kubectl get events -w
```

## Best Practices

### 1. Systematic Approach
```markdown
1. Identify the problem scope
2. Gather relevant information
3. Analyze logs and events
4. Test hypotheses
5. Implement solution
6. Verify fix
```

### 2. Preventive Measures
```markdown
1. Regular health checks
2. Resource monitoring
3. Log analysis
4. Backup procedures
5. Documentation
```

### 3. Documentation
```markdown
1. Keep troubleshooting logs
2. Document solutions
3. Update runbooks
4. Share knowledge
5. Review incidents
```

## Common Pitfalls

### 1. Troubleshooting Issues
```markdown
1. Incomplete information gathering
2. Wrong problem scope
3. Missing root cause analysis
4. Temporary fixes
5. Poor documentation
```

### 2. System Issues
```markdown
1. Resource exhaustion
2. Network misconfiguration
3. Certificate expiration
4. Storage problems
5. Security misconfigurations
```

[Continue with more sections...] 