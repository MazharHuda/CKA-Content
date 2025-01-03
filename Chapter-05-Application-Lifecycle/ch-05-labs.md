# Chapter 5: Application Lifecycle Management - Hands-on Labs

## Lab 1: Implementing Advanced Deployment Strategies

### Objective
Learn to implement different deployment strategies including rolling updates, blue-green, and canary deployments.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Basic understanding of Kubernetes deployments

### Steps

#### 1.1 Rolling Update Implementation
![Rolling Update Implementation](/Images/chapter05/ch05_lab01_rolling_update.png)
```bash
# Create initial deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
EOF

# Monitor rollout
kubectl rollout status deployment/web-app

# Perform update
kubectl set image deployment/web-app nginx=nginx:1.20

# Check rollout history
kubectl rollout history deployment/web-app

# Rollback if needed
kubectl rollout undo deployment/web-app
```

#### 1.2 Blue-Green Deployment
![Blue-Green Deployment](/Images/chapter05/ch05_lab01_blue_green.png)
```bash
# Create blue deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-blue
  labels:
    app: web
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: blue
  template:
    metadata:
      labels:
        app: web
        version: blue
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
EOF

# Create service pointing to blue
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
    version: blue
  ports:
  - port: 80
    targetPort: 80
EOF

# Create green deployment and switch service
# (Update service selector to version: green)
```![Canary Deployment](/Images/chapter05/ch05_lab01_blue_green.png)

## Lab 2: Configuration Management

### Objective
Implement various configuration management techniques using ConfigMaps and Secrets.

### Steps

#### 2.1 ConfigMap Management
![ConfigMap Management](/Images/chapter05/ch05_lab02_configmap.png)

```bash
# Create ConfigMap from literals
kubectl create configmap app-config \
  --from-literal=APP_ENV=production \
  --from-literal=APP_DEBUG=false

# Create ConfigMap from file
cat <<EOF > config.properties
database.url=jdbc:mysql://db:3306/myapp
database.user=app_user
log.level=INFO
EOF

kubectl create configmap app-config-file --from-file=config.properties

# Create pod using ConfigMap
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: config-test-pod
spec:
  containers:
  - name: test-container
    image: busybox
    command: [ "/bin/sh", "-c", "env" ]
    envFrom:
    - configMapRef:
        name: app-config
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config-file
EOF
```

#### 2.2 Secret Management
![Secret Management](/Images/chapter05/ch05_lab02_secrets.png)
```bash
# Create secret
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password=supersecret

# Create pod using secret
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
  - name: test-container
    image: busybox
    command: [ "/bin/sh", "-c", "env" ]
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: username
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: password
EOF
```
![Update Workflow](/Images/chapter05/ch05_lab02_update_flow.png)

## Lab 3: Application Scaling

### Objective
Implement and test different scaling strategies including manual and automatic scaling.

### Steps

#### 3.1 Manual Scaling
![Manual Scaling](/Images/chapter05/ch05_lab03_manual_scaling.png)

```bash
# Create deployment
kubectl create deployment scaling-demo --image=nginx:1.19

# Scale manually
kubectl scale deployment scaling-demo --replicas=5

# Monitor scaling
kubectl get pods -w
```

#### 3.2 Horizontal Pod Autoscaling
![Horizontal Pod Autoscaling](/Images/chapter05/ch05_lab03_hpa.png)
```bash
# Create deployment with resource requests
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: k8s.gcr.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 200m
          limits:
            cpu: 500m
EOF

# Create HPA
kubectl autoscale deployment php-apache \
  --cpu-percent=50 \
  --min=1 \
  --max=10

# Generate load
kubectl run -i --tty load-generator \
  --rm --image=busybox \
  --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"

# Monitor scaling
kubectl get hpa -w
```
![Load Test](/Images/chapter05/ch05_lab03_load_test.png)
## Lab 4: Health Checks and Probes

### Objective
Implement and test different types of health checks and probes.

### Steps

#### 4.1 Implementing Health Checks
![Health Checks and Probes](/Images/chapter05/ch05_lab04_health_checks.png)

![Probe flow](/Images/chapter05/ch05_lab04_probe_flow.png)
![Probe flow Timing](/Images/chapter05/ch05_lab04_probe_timing.png)
```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: probe-demo
spec:
  containers:
  - name: nginx
    image: nginx
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
EOF

# Monitor probe status
kubectl describe pod probe-demo
```

### Verification Tasks

1. Deployment Verification
```bash
kubectl rollout status deployment/web-app
kubectl get pods -l app=web
kubectl describe deployment web-app
```

2. Configuration Verification
```bash
kubectl exec config-test-pod -- env | grep APP_
kubectl exec config-test-pod -- cat /etc/config/config.properties
```

3. Scaling Verification
```bash
kubectl get hpa
kubectl top pods
kubectl describe deployment php-apache
```

### Troubleshooting Guide

1. Deployment Issues
```bash
kubectl describe deployment <deployment-name>
kubectl get events --field-selector involvedObject.kind=Deployment
kubectl logs <pod-name>
```

2. Configuration Issues
```bash
kubectl describe configmap <configmap-name>
kubectl describe secret <secret-name>
kubectl exec <pod-name> -- env
```

3. Scaling Issues
```bash
kubectl describe hpa <hpa-name>
kubectl top nodes
kubectl get events --field-selector involvedObject.kind=HorizontalPodAutoscaler
```

Canary & A/B Testing Labs

## Lab 5: Advanced Deployment Patterns

### Objective
Implement Canary and A/B testing deployment patterns using different approaches.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Istio installed (for advanced traffic management)

### 5.1 Canary Deployment Using Native Kubernetes
![Canary Deployment Using Native Kubernetes](/Images/chapter05/ch05_lab05_shadow.png)

#### Step 1: Create Base Deployment
```bash
# Create production deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-production
  labels:
    app: myapp
    version: v1
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
EOF

# Create service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
EOF
```

#### Step 2: Deploy Canary Version
```bash
# Create canary deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
  labels:
    app: myapp
    version: v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      version: v2
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
EOF
```

#### Step 3: Test and Monitor
```bash
# Monitor pod distribution
kubectl get pods -l app=myapp -L version

# Test service distribution
kubectl run -i --tty load-test --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.1; do wget -q -O- http://myapp-service; done"

# Monitor metrics
kubectl top pods -l app=myapp
```

### 5.2 A/B Testing Using Istio
![ A/B Testing Using Istio](/Images/chapter05/ch05_lab05_ab_testing.png)

#### Step 1: Create Two Versions of the Application
```bash
# Version A
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-version-a
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
      version: a
  template:
    metadata:
      labels:
        app: myapp
        version: a
    spec:
      containers:
      - name: app
        image: myapp:v1
        ports:
        - containerPort: 8080
---
# Version B
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-version-b
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
      version: b
  template:
    metadata:
      labels:
        app: myapp
        version: b
    spec:
      containers:
      - name: app
        image: myapp:v2
        ports:
        - containerPort: 8080
EOF
```

#### Step 2: Configure Istio Traffic Routing
```bash
# Create Virtual Service and Destination Rules
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp-vsvc
spec:
  hosts:
  - myapp.example.com
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Chrome.*"
    route:
    - destination:
        host: myapp-service
        subset: version-a
  - route:
    - destination:
        host: myapp-service
        subset: version-b
---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: myapp-destrule
spec:
  host: myapp-service
  subsets:
  - name: version-a
    labels:
      version: a
  - name: version-b
    labels:
      version: b
EOF
```

### 5.3 Progressive Delivery Using Flagger
![ Progressive Delivery Using Flagger](/Images/chapter05/ch05_lab05_feature_toggle.png)
#### Step 1: Install Flagger
```bash
# Add Flagger Helm repository
helm repo add flagger https://flagger.app

# Install Flagger
helm upgrade -i flagger flagger/flagger \
  --namespace istio-system \
  --set crd.create=true \
  --set meshProvider=istio \
  --set metricsServer=http://prometheus:9090
```

#### Step 2: Create Canary Custom Resource
```bash
cat <<EOF | kubectl apply -f -
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp-canary
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 80
    targetPort: 8080
  analysis:
    interval: 30s
    threshold: 10
    maxWeight: 50
    stepWeight: 5
    metrics:
    - name: request-success-rate
      threshold: 99
      interval: 1m
    - name: request-duration
      threshold: 500
      interval: 1m
EOF
```

### Verification and Testing

#### 1. Test Canary Deployment
```bash
# Monitor pod distribution
watch kubectl get pods -l app=myapp -L version

# Check service endpoints
kubectl get endpoints myapp-service

# Test with curl
for i in $(seq 1 100); do
  curl -s http://myapp-service
done | sort | uniq -c
```

#### 2. Test A/B Deployment
```bash
# Test with different user agents
curl -H "User-Agent: Chrome" http://myapp.example.com
curl -H "User-Agent: Firefox" http://myapp.example.com

# Monitor traffic distribution
kubectl -n istio-system logs -l app=istio-ingressgateway -c istio-proxy
```

#### 3. Monitor Metrics
```bash
# Get Prometheus metrics
kubectl -n istio-system port-forward svc/prometheus 9090:9090

# Get Grafana dashboards
kubectl -n istio-system port-forward svc/grafana 3000:3000
```

### Cleanup
```bash
# Remove deployments
kubectl delete deployment app-production app-canary
kubectl delete deployment app-version-a app-version-b

# Remove services
kubectl delete service myapp-service

# Remove Istio configs
kubectl delete virtualservice myapp-vsvc
kubectl delete destinationrule myapp-destrule

# Remove Flagger resources
kubectl delete canary myapp-canary
```

### Troubleshooting Guide

1. Deployment Issues
```bash
# Check deployment status
kubectl describe deployment <deployment-name>

# Check pod logs
kubectl logs <pod-name> -c <container-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

2. Traffic Routing Issues
```bash
# Check Istio configuration
istioctl analyze

# Check proxy configuration
istioctl proxy-config routes <pod-name>

# Check Envoy stats
kubectl exec <pod-name> -c istio-proxy -- pilot-agent request GET stats
```

3. Metrics Issues
```bash
# Check Prometheus targets
kubectl -n istio-system port-forward svc/prometheus 9090:9090
# Access localhost:9090/targets

# Check Flagger logs
kubectl -n istio-system logs deployment/flagger
```

Multi-cluster deployment labs

## Lab 6: Multi-cluster Deployment Patterns

### Objective
Implement and manage applications across multiple Kubernetes clusters with different deployment patterns.

### Prerequisites
- Access to two or more Kubernetes clusters
- kubectl configured with multiple contexts
- kubemci (Multi-cluster Ingress) installed
- Istio installed (optional, for advanced traffic management)

### 6.1 Setting Up Multi-cluster Environment
![ Setting Up Multi-cluster Environment](/Images/chapter05/ch05_lab06_multicluster.png)
#### Step 1: Configure kubectl Contexts
```bash
# List current contexts
kubectl config get-contexts

# Create aliases for easier management
alias kc1='kubectl --context=cluster1'
alias kc2='kubectl --context=cluster2'

# Verify access to both clusters
kc1 get nodes
kc2 get nodes

# Create test namespace in both clusters
for ctx in cluster1 cluster2; do
  kubectl --context=$ctx create namespace multi-cluster-demo
done
```

#### Step 2: Create Cluster Registry
```bash
# Create cluster registry
cat <<EOF | kubectl apply -f -
apiVersion: clusterregistry.k8s.io/v1alpha1
kind: Cluster
metadata:
  name: cluster1
  namespace: multi-cluster-demo
spec:
  kubernetesApiEndpoints:
    serverEndpoints:
      - clientCIDR: "0.0.0.0/0"
        serverAddress: "https://cluster1-api:6443"
---
apiVersion: clusterregistry.k8s.io/v1alpha1
kind: Cluster
metadata:
  name: cluster2
  namespace: multi-cluster-demo
spec:
  kubernetesApiEndpoints:
    serverEndpoints:
      - clientCIDR: "0.0.0.0/0"
        serverAddress: "https://cluster2-api:6443"
EOF
```

### 6.2 Implementing Active-Active Deployment
![ Implementing Active-Active Deployment](/Images/chapter05/ch05_lab06_active_active.png)
#### Step 1: Deploy Application to Both Clusters
```bash
# Create deployment template
cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-cluster-app
  namespace: multi-cluster-demo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: multi-cluster-app
  template:
    metadata:
      labels:
        app: multi-cluster-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
        env:
        - name: CLUSTER_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
EOF

# Deploy to both clusters
for ctx in cluster1 cluster2; do
  kubectl --context=$ctx apply -f deployment.yaml
done
```

#### Step 2: Configure Global Load Balancing
```bash
# Create multi-cluster service
cat <<EOF > multi-cluster-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-cluster-app
  namespace: multi-cluster-demo
  annotations:
    multicluster.kubernetes.io/service-type: LoadBalancer
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: multi-cluster-app
EOF

# Apply service to both clusters
for ctx in cluster1 cluster2; do
  kubectl --context=$ctx apply -f multi-cluster-service.yaml
done
```

### 6.3 Implementing Active-Passive Deployment

![Implementing Active-Passive Deployment](/Images/chapter05/ch05_lab06_dr.png)
#### Step 1: Deploy Primary Cluster
```bash
# Create deployment with primary label
cat <<EOF | kc1 apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: active-app
  namespace: multi-cluster-demo
  labels:
    role: primary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: active-app
  template:
    metadata:
      labels:
        app: active-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
EOF
```

#### Step 2: Deploy Standby Cluster
```bash
# Create deployment with standby label
cat <<EOF | kc2 apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: standby-app
  namespace: multi-cluster-demo
  labels:
    role: standby
spec:
  replicas: 3
  selector:
    matchLabels:
      app: active-app
  template:
    metadata:
      labels:
        app: active-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
EOF
```

### 6.4 Implementing Data Replication

#### Step 1: Configure Storage Replication
```bash
# Create PV and PVC in both clusters
cat <<EOF > storage.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: replicated-data
  namespace: multi-cluster-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: replicated-data
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data
EOF

# Apply to both clusters
for ctx in cluster1 cluster2; do
  kubectl --context=$ctx apply -f storage.yaml
done
```

#### Step 2: Configure Data Sync
```bash
# Deploy sync daemon
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: data-sync
  namespace: multi-cluster-demo
spec:
  selector:
    matchLabels:
      name: data-sync
  template:
    metadata:
      labels:
        name: data-sync
    spec:
      containers:
      - name: syncer
        image: rclone/rclone
        args:
        - sync
        - /source
        - /destination
        volumeMounts:
        - name: source-data
          mountPath: /source
        - name: dest-data
          mountPath: /destination
      volumes:
      - name: source-data
        persistentVolumeClaim:
          claimName: replicated-data
      - name: dest-data
        persistentVolumeClaim:
          claimName: replicated-data
EOF
```

### 6.5 Monitoring and Verification

#### Step 1: Check Deployment Status
```bash
# Check deployments across clusters
for ctx in cluster1 cluster2; do
  echo "Checking cluster: $ctx"
  kubectl --context=$ctx get deployments -n multi-cluster-demo
  kubectl --context=$ctx get pods -n multi-cluster-demo
done
```

#### Step 2: Test Load Balancing
```bash
# Create test pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: test-client
spec:
  containers:
  - name: curl
    image: curlimages/curl
    command: ["/bin/sh", "-c", "while true; do curl -s http://multi-cluster-app; sleep 1; done"]
EOF

# Monitor logs to verify distribution
kubectl logs -f test-client
```

### Cleanup
```bash
# Remove resources from both clusters
for ctx in cluster1 cluster2; do
  kubectl --context=$ctx delete namespace multi-cluster-demo
  kubectl --context=$ctx delete -f deployment.yaml
  kubectl --context=$ctx delete -f multi-cluster-service.yaml
  kubectl --context=$ctx delete -f storage.yaml
done
```

### Troubleshooting Guide

1. Cluster Connectivity Issues
```bash
# Check cluster status
kubectl config get-contexts

# Verify API server access
kubectl --context=cluster1 cluster-info
kubectl --context=cluster2 cluster-info
```

2. Load Balancing Issues
```bash
# Check service status
kubectl --context=cluster1 get svc -n multi-cluster-demo
kubectl --context=cluster2 get svc -n multi-cluster-demo

# Check endpoints
kubectl --context=cluster1 get endpoints -n multi-cluster-demo
kubectl --context=cluster2 get endpoints -n multi-cluster-demo
```

3. Data Replication Issues
```bash
# Check PV/PVC status
kubectl --context=cluster1 get pv,pvc -n multi-cluster-demo
kubectl --context=cluster2 get pv,pvc -n multi-cluster-demo

# Check sync daemon logs
kubectl --context=cluster1 logs -l name=data-sync -n multi-cluster-demo
```

