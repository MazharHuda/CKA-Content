# Chapter 4: Pod Orchestration and Scheduling - Hands-on Labs

## Lab 1: Advanced Pod Configuration and Management

### Objective
Learn to create and manage pods with various configurations including multi-container pods, resource constraints, and health checks.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Basic understanding of YAML

### Steps

#### 1.1 Create a Multi-Container Pod
```yaml
# multi-container-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
    
  - name: content-sync
    image: busybox
    command: ['sh', '-c', 'while true; do echo "Hello from syncer $(date)" > /data/index.html; sleep 10; done']
    volumeMounts:
    - name: shared-data
      mountPath: /data
  
  volumes:
  - name: shared-data
    emptyDir: {}
```

```bash
# Apply and verify
kubectl apply -f multi-container-pod.yaml
kubectl get pod web-app
kubectl describe pod web-app

# Test the containers
kubectl exec -it web-app -c nginx -- curl localhost
kubectl logs web-app -c content-sync
```

#### 1.2 Implement Health Checks
```yaml
# health-checks-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-check-demo
spec:
  containers:
  - name: app
    image: nginx:1.21
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 3
      periodSeconds: 3
    readinessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
```

```bash
# Apply and monitor health checks
kubectl apply -f health-checks-pod.yaml
kubectl describe pod health-check-demo
kubectl get events --field-selector involvedObject.name=health-check-demo
```

## Lab 2: Pod Scheduling and Placement

### Objective
Understand and implement various pod scheduling strategies including node selection, affinity, and taints/tolerations.

### Steps

#### 2.1 Node Selection and Labels
```bash
# Label nodes
kubectl label nodes worker1 disk=ssd
kubectl label nodes worker2 disk=hdd

# Create pod with node selector
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: nginx-ssd
spec:
  nodeSelector:
    disk: ssd
  containers:
  - name: nginx
    image: nginx
EOF

# Verify placement
kubectl get pod nginx-ssd -o wide
```

#### 2.2 Implement Node Affinity
```yaml
# node-affinity-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disk
            operator: In
            values:
            - ssd
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: performance
            operator: In
            values:
            - high
  containers:
  - name: nginx
    image: nginx
```

#### 2.3 Configure Taints and Tolerations
```bash
# Add taint to node
kubectl taint nodes worker1 app=critical:NoSchedule

# Create pod with toleration
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: critical-app
spec:
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "critical"
    effect: "NoSchedule"
  containers:
  - name: nginx
    image: nginx
EOF
```

## Lab 3: Resource Management and QoS

### Objective
Learn to manage pod resources and implement different Quality of Service (QoS) classes.

### Steps

#### 3.1 Create Pods with Resource Requests and Limits
```yaml
# resource-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-demo
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

```bash
# Create and monitor resource usage
kubectl apply -f resource-pod.yaml
kubectl describe pod resource-demo
kubectl top pod resource-demo
```

#### 3.2 Implement Different QoS Classes
```yaml
# guaranteed-qos.yaml
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed-pod
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        memory: "128Mi"
        cpu: "500m"
      limits:
        memory: "128Mi"
        cpu: "500m"
---
# burstable-qos.yaml
apiVersion: v1
kind: Pod
metadata:
  name: burstable-pod
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

## Lab 4: Advanced Pod Patterns

### Objective
Implement various pod patterns including init containers, sidecars, and pod disruption budgets.

### Steps

#### 4.1 Create Pod with Init Container
```yaml
# init-container-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  initContainers:
  - name: init-service
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  containers:
  - name: app
    image: nginx
```

#### 4.2 Implement Sidecar Pattern
```yaml
# sidecar-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: sidecar-demo
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  - name: log-shipper
    image: busybox
    command: ['sh', '-c', 'tail -f /var/log/nginx/access.log']
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  volumes:
  - name: logs
    emptyDir: {}
```

### Verification Tasks

1. Pod Status Verification
```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name> [-c <container-name>]
```

2. Resource Usage Monitoring
```bash
kubectl top pods
kubectl describe node | grep -A 5 "Allocated resources"
```

3. Scheduling Verification
```bash
kubectl get pods -o wide
kubectl describe pod <pod-name> | grep Node:
```

### Troubleshooting Guide

1. Pod Creation Issues
```bash
kubectl describe pod <pod-name>
kubectl get events --field-selector involvedObject.name=<pod-name>
```

2. Container Issues
```bash
kubectl logs <pod-name> [-c <container-name>]
kubectl exec -it <pod-name> [-c <container-name>] -- /bin/sh
```

3. Resource Issues
```bash
kubectl describe pod <pod-name> | grep -A 3 Events
kubectl top pod <pod-name>
```