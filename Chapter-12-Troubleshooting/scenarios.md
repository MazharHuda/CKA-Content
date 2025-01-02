# Chapter 12: Troubleshooting - Real-world Scenarios

## Scenario 1: Unresponsive Application

### Situation
A critical microservice-based application is reported as unresponsive. The application consists of a frontend service, backend API, and a database. Users report timeouts when accessing the application.

### Initial Investigation
1. Check pod status:
```bash
kubectl get pods -n production
kubectl get pods -n production -o wide
```

2. Check service endpoints:
```bash
kubectl get endpoints frontend-svc backend-svc db-svc -n production
```

3. Review recent events:
```bash
kubectl get events -n production --sort-by=.metadata.creationTimestamp
```

### Common Findings and Solutions
1. **Pod Health Issues**
   ```bash
   # Check pod logs
   kubectl logs -n production <pod-name> --previous
   kubectl describe pod -n production <pod-name>
   ```

2. **Resource Constraints**
   ```bash
   # Check resource usage
   kubectl top pods -n production
   kubectl top nodes
   ```

3. **Network Issues**
   ```bash
   # Test connectivity
   kubectl run test-net --image=busybox -it --rm -- wget -O- http://backend-svc:8080
   ```

## Scenario 2: Control Plane Failure

### Situation
Multiple users report that they cannot create or modify resources in the cluster. The kubectl commands are timing out or returning errors.

### Investigation Steps
1. Check control plane components:
```bash
kubectl get pods -n kube-system
systemctl status kubelet
```

2. Verify API server health:
```bash
curl -k https://localhost:6443/healthz
journalctl -u kube-apiserver
```

3. Check ETCD status:
```bash
ETCDCTL_API=3 etcdctl endpoint health \
--endpoints=https://127.0.0.1:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key
```

### Common Solutions
1. **API Server Issues**
   ```bash
   # Check certificates
   openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
   
   # Restart API server
   cd /etc/kubernetes/manifests
   mv kube-apiserver.yaml ../
   sleep 5
   mv ../kube-apiserver.yaml .
   ```

2. **ETCD Problems**
   ```bash
   # Backup ETCD
   ETCDCTL_API=3 etcdctl snapshot save snapshot.db
   
   # Check disk space
   df -h /var/lib/etcd
   ```

## Scenario 3: Node Failure

### Situation
Several pods are being evicted from a node, and new pods are not being scheduled on it.

### Investigation
1. Check node status:
```bash
kubectl describe node <node-name>
kubectl get node <node-name> -o yaml
```

2. Verify system resources:
```bash
ssh <node-name>
df -h
free -m
top
```

3. Check kubelet logs:
```bash
journalctl -u kubelet -f
systemctl status kubelet
```

### Resolution Steps
1. **Resource Pressure**
   ```bash
   # Clean up unused resources
   docker system prune
   kubectl drain <node-name> --ignore-daemonsets
   ```

2. **Kubelet Issues**
   ```bash
   # Restart kubelet
   systemctl restart kubelet
   
   # Check certificates
   openssl x509 -in /var/lib/kubelet/pki/kubelet.crt -text -noout
   ```

## Scenario 4: Storage Problems

### Situation
Pods with persistent volumes are stuck in Pending state or failing to start.

### Investigation Steps
1. Check PVC status:
```bash
kubectl get pvc -A
kubectl describe pvc <pvc-name>
```

2. Verify storage provider:
```bash
kubectl get sc
kubectl describe sc <storage-class-name>
```

3. Check pod events:
```bash
kubectl describe pod <pod-name> | grep Events: -A 10
```

### Common Solutions
1. **PV Binding Issues**
   ```bash
   # Check available PVs
   kubectl get pv
   
   # Verify storage class
   kubectl get sc <storage-class-name> -o yaml
   ```

2. **Storage Provider Problems**
   ```bash
   # Check storage provider pods
   kubectl get pods -n kube-system | grep csi
   kubectl logs -n kube-system <csi-pod-name>
   ```

## Scenario 5: Network Connectivity Issues

### Situation
Pods cannot communicate with each other or with external services. Services are not accessible.

### Investigation
1. Check CNI status:
```bash
kubectl get pods -n kube-system -l k8s-app=calico-node
ls -l /etc/cni/net.d/
```

2. Verify DNS:
```bash
kubectl run test-dns --image=busybox:1.28 -- nslookup kubernetes.default
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

3. Test connectivity:
```bash
# Create test pods
kubectl run test-pod1 --image=nginx
kubectl run test-pod2 --image=busybox -- sleep 3600

# Test connection
kubectl exec test-pod2 -- wget -O- http://test-pod1
```

### Resolution Steps
1. **CNI Issues**
   ```bash
   # Restart CNI pods
   kubectl delete pod -n kube-system -l k8s-app=calico-node
   
   # Check CNI logs
   kubectl logs -n kube-system <cni-pod-name>
   ```

2. **DNS Problems**
   ```bash
   # Check CoreDNS configuration
   kubectl get configmap coredns -n kube-system -o yaml
   
   # Restart CoreDNS
   kubectl rollout restart deployment coredns -n kube-system
   ```

## Best Practices

1. **Documentation**
   - Keep a troubleshooting runbook
   - Document all changes made during incident resolution
   - Maintain cluster configuration backups

2. **Monitoring**
   ```bash
   # Set up monitoring
   kubectl apply -f prometheus-operator.yaml
   kubectl apply -f node-exporter.yaml
   kubectl apply -f grafana.yaml
   ```

3. **Regular Health Checks**
   ```bash
   # Create health check script
   kubectl get nodes -o wide
   kubectl get pods --all-namespaces
   kubectl top nodes
   kubectl get events --sort-by=.metadata.creationTimestamp
   ```

4. **Backup Procedures**
   ```bash
   # ETCD backup
   ETCDCTL_API=3 etcdctl snapshot save backup.db
   
   # Resource backup
   kubectl get all --all-namespaces -o yaml > cluster-backup.yaml
   ```
