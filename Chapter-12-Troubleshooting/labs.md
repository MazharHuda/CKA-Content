# Chapter 12: Troubleshooting - Practice Labs

## Prerequisites
- Running Kubernetes cluster (v1.27+)
- kubectl CLI tool configured
- Access to cluster nodes
- Basic understanding of Kubernetes components

## Lab 1: Cluster-level Troubleshooting

### Objective
Learn to diagnose and resolve control plane component issues.

### Tasks

1. API Server Troubleshooting:
```bash
# Check API server status and logs
kubectl get componentstatuses
sudo systemctl status kube-apiserver
sudo journalctl -u kube-apiserver -n 100

# Verify API server certificates
sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
```

2. ETCD Health Check:
```bash
# Check ETCD health and member list
ETCDCTL_API=3 etcdctl endpoint health \
--endpoints=https://127.0.0.1:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key

# Check ETCD metrics
ETCDCTL_API=3 etcdctl endpoint status --write-out=table
```

## Lab 2: Node Troubleshooting

### Objective
Identify and resolve common node issues.

### Tasks

1. Node Health Analysis:
```bash
# Check node status and details
kubectl get nodes
kubectl describe node <node-name>

# Verify kubelet status
sudo systemctl status kubelet
sudo journalctl -u kubelet -n 100

# Check system resources
df -h
free -m
top
```

2. Node Connectivity:
```bash
# Test network connectivity
ping <node-ip>
telnet <node-ip> 6443
nc -zv <node-ip> 10250

# Check node DNS resolution
nslookup kubernetes.default
```

## Lab 3: Pod Troubleshooting

### Objective
Debug pod deployment and runtime issues.

### Tasks

1. Pod Lifecycle Issues:
```bash
# Check pod status and details
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Analyze pod logs
kubectl logs <pod-name> [-c container-name]
kubectl logs <pod-name> --previous

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp
```

2. Create Debug Pod:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
spec:
  containers:
  - name: debug
    image: busybox:1.28
    command: ['sleep', '3600']
    securityContext:
      privileged: true
```

## Lab 4: Network Troubleshooting

### Objective
Diagnose and resolve networking issues.

### Tasks

1. Service Connectivity:
```bash
# Test service DNS resolution
kubectl run test-dns --image=busybox:1.28 -- nslookup kubernetes.default

# Check service endpoints
kubectl get endpoints <service-name>
kubectl describe service <service-name>

# Test service connectivity
kubectl run test-curl --image=curlimages/curl --rm -it -- curl <service-name>.<namespace>
```

2. Network Policy Testing:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector:
    matchLabels:
      app: test
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            role: frontend
```

[Content continues in next part due to length...]

## Lab 5: Storage Troubleshooting

### Objective
Learn to diagnose and resolve storage-related issues in Kubernetes.

### Tasks

1. PV/PVC Analysis:
```bash
# Check storage status
kubectl get pv,pvc
kubectl describe pv <pv-name>
kubectl describe pvc <pvc-name>

# Verify storage class
kubectl get sc
kubectl describe sc <storage-class-name>
```

2. Volume Mount Debugging:
```bash
# Check volume mounts
kubectl describe pod <pod-name> | grep -A 10 Volumes

# Debug volume permissions
kubectl exec -it <pod-name> -- ls -la /mount/path
```

## Lab 6: Application Debugging

### Objective
Debug application deployment and runtime issues.

### Tasks

1. Application Logs Analysis:
```bash
# Get application logs
kubectl logs <pod-name> -f
kubectl logs -l app=myapp --all-containers=true

# Export logs to file
kubectl logs <pod-name> > app.log
```

## Lab 7: Resource Troubleshooting

### Objective
Learn to diagnose and resolve resource-related issues.

### Tasks

1. Resource Constraints:
```bash
# Check resource usage
kubectl top nodes
kubectl top pods --containers

# Identify resource pressure
kubectl describe node <node-name> | grep Pressure

# View resource quotas
kubectl get resourcequota
kubectl describe resourcequota
```

2. Pod Resource Issues:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-debug
spec:
  containers:
  - name: debug
    image: busybox:1.28
    command: ['sh', '-c', 'while true; do echo "Testing resources"; sleep 2; done']
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

[Content continues in final part...]

## Lab 8: Best Practices and Tips

### Objective
Learn and apply best practices for troubleshooting in Kubernetes environments.

### Tasks

1. Documentation:
```bash
# Create troubleshooting runbook
kubectl get events --sort-by=.metadata.creationTimestamp > incident_timeline.txt
kubectl describe pod <pod-name> > pod_details.txt

# Collect cluster state
kubectl get all --all-namespaces -o yaml > cluster_state.yaml
```

2. Monitoring Setup:
```bash
# Deploy monitoring tools
kubectl apply -f prometheus-operator.yaml
kubectl apply -f grafana-deployment.yaml

# Verify monitoring
kubectl get pods -n monitoring
```

## Exam Tips

1. Troubleshooting Methodology:
- Start with high-level components
- Use systematic approach
- Check logs and events
- Verify configurations
- Test connectivity

2. Common Issues:
- Certificate expiration
- Resource constraints
- Network policies
- Storage problems
- RBAC misconfiguration

3. Time Management:
- Prioritize critical issues
- Use efficient commands
- Document findings
- Know when to escalate

## Cleanup
```bash
# Remove test resources
kubectl delete pod debug-pod
kubectl delete networkpolicy test-network-policy
kubectl delete pvc test-pvc
```