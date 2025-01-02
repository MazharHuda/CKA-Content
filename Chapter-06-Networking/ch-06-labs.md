# Chapter 6: Kubernetes Networking - Hands-on Labs

## Lab 1: Understanding Pod Networking

### Objective
Understand and implement pod-to-pod communication, network namespaces, and basic networking concepts.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Access to create network policies

### Steps

#### 1.1 Create Test Pods for Networking
```bash
# Create test pods in different namespaces
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: network-test
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-a
  namespace: network-test
  labels:
    app: network-test
spec:
  containers:
  - name: netshoot
    image: nicolaka/netshoot
    command: ['sh', '-c', 'sleep infinity']
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-b
  namespace: network-test
  labels:
    app: network-test
spec:
  containers:
  - name: nginx
    image: nginx
EOF

# Verify pods are running
kubectl get pods -n network-test
```

#### 1.2 Test Pod Network Connectivity
```bash
# Test connectivity between pods
kubectl exec -n network-test pod-a -- ping -c 4 pod-b
kubectl exec -n network-test pod-a -- curl pod-b

# Examine network interfaces
kubectl exec -n network-test pod-a -- ip addr
kubectl exec -n network-test pod-a -- ip route

# Test DNS resolution
kubectl exec -n network-test pod-a -- nslookup kubernetes.default
```

## Lab 2: Implementing Services

### Objective
Create and test different types of Kubernetes services.

### Steps

#### 2.1 Create ClusterIP Service
```yaml
# Create deployment and service
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: network-test
spec:
  replicas: 3
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
        image: nginx
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: network-test
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
EOF

# Test service
kubectl run -n network-test test-pod --image=busybox -i --rm --restart=Never -- wget -qO- web-service
```

#### 2.2 Create NodePort Service
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: web-nodeport
  namespace: network-test
spec:
  type: NodePort
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
EOF

# Get node IP and test NodePort
NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
curl http://$NODE_IP:30080
```

## Lab 3: Network Policies

### Objective
Implement and test network policies for pod isolation.

### Steps

#### 3.1 Create Default Deny Policy
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: network-test
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF
```

#### 3.2 Create Allowed Communication Policy
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-web
  namespace: network-test
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 80
EOF

# Test policy
kubectl run -n network-test frontend --labels=role=frontend --image=busybox -i --rm --restart=Never -- wget -qO- web-service
kubectl run -n network-test backend --labels=role=backend --image=busybox -i --rm --restart=Never -- wget -qO- web-service
```

## Lab 4: DNS and Service Discovery

### Objective
Understand and implement Kubernetes DNS and service discovery.

### Steps

#### 4.1 Create Service Discovery Test
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: dns-test
  namespace: network-test
spec:
  containers:
  - name: dns-test
    image: busybox
    command:
    - sleep
    - "3600"
EOF

# Test DNS resolution
kubectl exec -n network-test dns-test -- nslookup web-service
kubectl exec -n network-test dns-test -- nslookup web-service.network-test.svc.cluster.local
```

#### 4.2 Custom DNS Configuration
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: custom-dns
  namespace: network-test
spec:
  containers:
  - name: dns-test
    image: busybox
    command:
    - sleep
    - "3600"
  dnsConfig:
    nameservers:
    - 8.8.8.8
    searches:
    - ns1.svc.cluster.local
    - my.dns.search.suffix
    options:
    - name: ndots
      value: "2"
EOF
```

[Continue with more labs...]

## Lab 5: Ingress Controllers and Load Balancing

### Objective
Set up and configure Ingress Controllers, implement various load balancing strategies, and manage external access to services.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Helm installed (for NGINX Ingress Controller installation)
- Domain name for testing (can use nip.io)

### Steps

#### 5.1 Install NGINX Ingress Controller
```bash
# Add the NGINX Ingress repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Install NGINX Ingress Controller
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set controller.admissionWebhooks.enabled=true \
  --set controller.metrics.enabled=true

# Verify installation
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx
```

#### 5.2 Deploy Test Applications
```yaml
# Create test applications
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1
  namespace: network-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
      initContainers:
      - name: init-html
        image: busybox
        command: ["/bin/sh", "-c"]
        args:
          - echo "<h1>App 1</h1>" > /html/index.html
        volumeMounts:
        - name: html
          mountPath: /html
      volumes:
      - name: html
        emptyDir: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2
  namespace: network-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app2
  template:
    metadata:
      labels:
        app: app2
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
      initContainers:
      - name: init-html
        image: busybox
        command: ["/bin/sh", "-c"]
        args:
          - echo "<h1>App 2</h1>" > /html/index.html
        volumeMounts:
        - name: html
          mountPath: /html
      volumes:
      - name: html
        emptyDir: {}
EOF

# Create services for applications
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: app1-service
  namespace: network-test
spec:
  selector:
    app: app1
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app2-service
  namespace: network-test
spec:
  selector:
    app: app2
  ports:
  - port: 80
    targetPort: 80
EOF
```

#### 5.3 Configure Path-based Routing
```yaml
# Create Ingress resource for path-based routing
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: path-based-ingress
  namespace: network-test
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: apps.example.com  # Replace with your domain
    http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
      - path: /app2
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
EOF
```

#### 5.4 Configure SSL/TLS
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=apps.example.com"

# Create TLS secret
kubectl create secret tls apps-tls \
  --key tls.key \
  --cert tls.crt \
  -n network-test

# Update Ingress with TLS
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  namespace: network-test
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - apps.example.com
    secretName: apps-tls
  rules:
  - host: apps.example.com
    http:
      paths:
      - path: /app1
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
      - path: /app2
        pathType: Prefix
        backend:
          service:
            name: app2-service
            port:
              number: 80
EOF
```

#### 5.5 Configure Load Balancing Strategies
```yaml
# Create Ingress with custom load balancing
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: lb-ingress
  namespace: network-test
  annotations:
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
    nginx.ingress.kubernetes.io/session-cookie-name: "route"
    nginx.ingress.kubernetes.io/session-cookie-expires: "172800"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
spec:
  ingressClassName: nginx
  rules:
  - host: apps.example.com
    http:
      paths:
      - path: /app
        pathType: Prefix
        backend:
          service:
            name: app1-service
            port:
              number: 80
EOF
```

### Verification Steps

1. Test Path-based Routing
```bash
# Get Ingress IP
INGRESS_IP=$(kubectl get svc -n ingress-nginx nginx-ingress-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Test routing
curl -H "Host: apps.example.com" http://$INGRESS_IP/app1
curl -H "Host: apps.example.com" http://$INGRESS_IP/app2
```

2. Test SSL/TLS
```bash
# Test HTTPS
curl -k -H "Host: apps.example.com" https://$INGRESS_IP/app1
curl -k -H "Host: apps.example.com" https://$INGRESS_IP/app2
```

3. Test Load Balancing
```bash
# Test multiple requests
for i in {1..10}; do
  curl -H "Host: apps.example.com" http://$INGRESS_IP/app
done
```

### Cleanup
```bash
# Remove resources
kubectl delete ingress -n network-test --all
kubectl delete service -n network-test app1-service app2-service
kubectl delete deployment -n network-test app1 app2
kubectl delete secret -n network-test apps-tls
helm uninstall nginx-ingress -n ingress-nginx
```

## Lab 6: Network Troubleshooting

### Objective
Learn to diagnose and resolve common Kubernetes networking issues using various troubleshooting tools and techniques.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- netshoot container image
- Access to cluster nodes

### 6.1 Network Debugging Tools Setup

#### Create Debugging Pod
```yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: netshoot
  namespace: network-test
spec:
  containers:
  - name: netshoot
    image: nicolaka/netshoot
    command:
      - sleep
      - "3600"
    securityContext:
      capabilities:
        add: ["NET_ADMIN", "NET_RAW"]
EOF

# Verify pod creation
kubectl get pod netshoot -n network-test
```

### 6.2 DNS Troubleshooting

#### 6.2.1 DNS Resolution Issues
```bash
# Create test pods with different DNS configurations
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: dns-test-1
  namespace: network-test
spec:
  containers:
  - name: dns-test
    image: busybox
    command:
      - sleep
      - "3600"
  dnsPolicy: ClusterFirst
---
apiVersion: v1
kind: Pod
metadata:
  name: dns-test-2
  namespace: network-test
spec:
  containers:
  - name: dns-test
    image: busybox
    command:
      - sleep
      - "3600"
  dnsPolicy: None
  dnsConfig:
    nameservers:
      - "8.8.8.8"
    searches:
      - "default.svc.cluster.local"
      - "svc.cluster.local"
      - "cluster.local"
EOF

# DNS Troubleshooting Commands
kubectl exec -n network-test dns-test-1 -- cat /etc/resolv.conf
kubectl exec -n network-test dns-test-1 -- nslookup kubernetes.default
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### 6.3 Network Connectivity Testing

#### 6.3.1 Pod-to-Pod Connectivity
```bash
# Create test pods in different namespaces
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: test-ns-1
---
apiVersion: v1
kind: Namespace
metadata:
  name: test-ns-2
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
  namespace: test-ns-1
  labels:
    app: connectivity-test
spec:
  containers:
  - name: nginx
    image: nginx
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-2
  namespace: test-ns-2
  labels:
    app: connectivity-test
spec:
  containers:
  - name: nginx
    image: nginx
EOF

# Test connectivity
kubectl exec -n network-test netshoot -- ping -c 4 pod-1.test-ns-1
kubectl exec -n network-test netshoot -- traceroute pod-2.test-ns-2
kubectl exec -n network-test netshoot -- tcpdump -i any -n port 80
```

### 6.4 Service Connectivity Troubleshooting

#### 6.4.1 Service Endpoint Verification
```bash
# Create test service and deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-test
  namespace: network-test
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-test
  template:
    metadata:
      labels:
        app: web-test
    spec:
      containers:
      - name: nginx
        image: nginx
---
apiVersion: v1
kind: Service
metadata:
  name: web-test-svc
  namespace: network-test
spec:
  selector:
    app: web-test
  ports:
  - port: 80
    targetPort: 80
EOF

# Service Troubleshooting Commands
kubectl get endpoints web-test-svc -n network-test
kubectl describe service web-test-svc -n network-test
kubectl get pods -n network-test -l app=web-test -o wide
```

### 6.5 Network Policy Troubleshooting

#### 6.5.1 Policy Testing
```bash
# Create test network policy
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: network-test
spec:
  podSelector:
    matchLabels:
      app: web-test
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
      port: 80
EOF

# Test network policy
kubectl run frontend --namespace=network-test --labels=role=frontend --image=busybox -i --rm -- wget -qO- web-test-svc
kubectl run backend --namespace=network-test --labels=role=backend --image=busybox -i --rm -- wget -qO- web-test-svc
```

### 6.6 Advanced Network Diagnostics

#### 6.6.1 Network Packet Analysis
```bash
# Start packet capture
kubectl exec -n network-test netshoot -- tcpdump -i any -w /tmp/capture.pcap port 80

# Generate traffic
kubectl run test-client --namespace=network-test --image=busybox -i --rm -- wget -qO- web-test-svc

# Copy capture file
kubectl cp network-test/netshoot:/tmp/capture.pcap ./capture.pcap

# Analyze with Wireshark or tcpdump
tcpdump -r capture.pcap -n
```

#### 6.6.2 MTU and Network Interface Troubleshooting
```bash
# Check MTU settings
kubectl exec -n network-test netshoot -- ip link show

# Test MTU issues
kubectl exec -n network-test netshoot -- ping -c 4 -M do -s 1500 web-test-svc

# Check interface statistics
kubectl exec -n network-test netshoot -- netstat -i
```

### 6.7 Common Issues and Solutions

#### 6.7.1 kube-proxy Verification
```bash
# Check kube-proxy status
kubectl get pods -n kube-system -l k8s-app=kube-proxy
kubectl logs -n kube-system -l k8s-app=kube-proxy

# Verify iptables rules
kubectl exec -n network-test netshoot -- iptables-save | grep web-test-svc
```

#### 6.7.2 CNI Plugin Troubleshooting
```bash
# Check CNI configuration
kubectl exec -n network-test netshoot -- ls -l /etc/cni/net.d/
kubectl exec -n network-test netshoot -- cat /etc/cni/net.d/10-calico.conflist

# Verify CNI pods
kubectl get pods -n kube-system -l k8s-app=calico-node
```

### Verification Checklist

1. DNS Resolution
```bash
# Verify CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

2. Network Connectivity
```bash
# Basic connectivity tests
kubectl exec -n network-test netshoot -- ping -c 4 8.8.8.8
kubectl exec -n network-test netshoot -- curl -v telnet://web-test-svc:80
```

3. Service Discovery
```bash
# Test service resolution
kubectl exec -n network-test netshoot -- nslookup web-test-svc.network-test.svc.cluster.local
```

### Cleanup
```bash
# Remove test resources
kubectl delete namespace test-ns-1 test-ns-2
kubectl delete -f network-policy.yaml
kubectl delete deployment web-test -n network-test
kubectl delete service web-test-svc -n network-test
kubectl delete pod netshoot -n network-test
```

## Lab 7: Advanced Service Configurations

### Objective
Implement and understand advanced service configurations including session affinity, ExternalName services, headless services, and multi-port services.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Access to create services and deployments

### 7.1 Session Affinity and Load Balancing

#### 7.1.1 Session Affinity Configuration
```yaml
# Create deployment with multiple replicas
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: session-app
  namespace: network-test
spec:
  replicas: 3
  selector:
    matchLabels:
      app: session-app
  template:
    metadata:
      labels:
        app: session-app
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: script
          mountPath: /usr/share/nginx/html
      initContainers:
      - name: init-html
        image: busybox
        command: ['/bin/sh', '-c']
        args:
          - |
            echo "Server: $HOSTNAME" > /html/index.html
        volumeMounts:
        - name: script
          mountPath: /html
      volumes:
      - name: script
        emptyDir: {}
---
# Service with session affinity
apiVersion: v1
kind: Service
metadata:
  name: session-service
  namespace: network-test
spec:
  selector:
    app: session-app
  ports:
  - port: 80
    targetPort: 80
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
EOF

# Test session affinity
for i in {1..10}; do
  kubectl run -n network-test test-${i} --rm -i --image=busybox --restart=Never -- wget -qO- session-service
done
```

### 7.2 Multi-Port Services

#### 7.2.1 Configure Multi-Port Service
```yaml
# Create deployment with multiple ports
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-port-app
  namespace: network-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: multi-port
  template:
    metadata:
      labels:
        app: multi-port
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
          name: http
        - containerPort: 443
          name: https
      - name: metrics
        image: prom/prometheus
        ports:
        - containerPort: 9090
          name: metrics
---
# Multi-port service
apiVersion: v1
kind: Service
metadata:
  name: multi-port-service
  namespace: network-test
spec:
  selector:
    app: multi-port
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: https
    port: 443
    targetPort: https
  - name: metrics
    port: 9090
    targetPort: metrics
EOF

# Test different ports
kubectl run -n network-test port-test --rm -i --image=busybox --restart=Never -- wget -qO- multi-port-service:80
kubectl run -n network-test port-test --rm -i --image=busybox --restart=Never -- wget -qO- multi-port-service:9090
```

### 7.3 Headless Services

#### 7.3.1 Implement Headless Service
```yaml
# Create StatefulSet with headless service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: headless-service
  namespace: network-test
spec:
  clusterIP: None
  selector:
    app: stateful-app
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: stateful-app
  namespace: network-test
spec:
  serviceName: headless-service
  replicas: 3
  selector:
    matchLabels:
      app: stateful-app
  template:
    metadata:
      labels:
        app: stateful-app
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

# Test DNS resolution for individual pods
kubectl run -n network-test dns-test --rm -i --image=busybox --restart=Never -- nslookup stateful-app-0.headless-service
```

### 7.4 ExternalName Services

#### 7.4.1 Configure ExternalName Service
```yaml
# Create ExternalName service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: external-service
  namespace: network-test
spec:
  type: ExternalName
  externalName: api.example.com
EOF

# Test external name resolution
kubectl run -n network-test external-test --rm -i --image=busybox --restart=Never -- nslookup external-service
```

### 7.5 Service Topology

#### 7.5.1 Configure Topology-Aware Service
```yaml
# Create service with topology awareness
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: topology-service
  namespace: network-test
  annotations:
    service.kubernetes.io/topology-aware-hints: "auto"
spec:
  selector:
    app: topology-app
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: topology-app
  namespace: network-test
spec:
  replicas: 6
  selector:
    matchLabels:
      app: topology-app
  template:
    metadata:
      labels:
        app: topology-app
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: topology-app
      containers:
      - name: nginx
        image: nginx
EOF
```

### 7.6 Service Health Checks

#### 7.6.1 Configure Service with Health Checks
```yaml
# Create service with health checks
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: health-service
  namespace: network-test
  annotations:
    service.kubernetes.io/healthcheck-nodeport: "32000"
spec:
  selector:
    app: health-app
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-app
  namespace: network-test
spec:
  replicas: 3
  selector:
    matchLabels:
      app: health-app
  template:
    metadata:
      labels:
        app: health-app
    spec:
      containers:
      - name: nginx
        image: nginx
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 3
          periodSeconds: 3
EOF
```

### Verification Steps

1. Test Session Affinity
```bash
# Run multiple requests from same client
for i in {1..10}; do
  kubectl run -n network-test affinity-test-${i} \
    --rm -i --image=busybox --restart=Never \
    -- wget -qO- session-service
done
```

2. Verify Multi-Port Service
```bash
# Test each port
for port in 80 443 9090; do
  kubectl run -n network-test port-test \
    --rm -i --image=busybox --restart=Never \
    -- wget -qO- multi-port-service:${port}
done
```

3. Check Headless Service DNS
```bash
# Verify DNS entries for each pod
for i in {0..2}; do
  kubectl run -n network-test dns-test \
    --rm -i --image=busybox --restart=Never \
    -- nslookup stateful-app-${i}.headless-service
done
```

### Cleanup
```bash
# Remove all test resources
kubectl delete deployment -n network-test session-app multi-port-app topology-app health-app
kubectl delete service -n network-test session-service multi-port-service headless-service external-service topology-service health-service
kubectl delete statefulset -n network-test stateful-app
```

## Lab 8: CNI Plugin Configuration and Management

### Objective
Learn to install, configure, and troubleshoot different CNI plugins, understand their networking models, and implement advanced networking features.

### Prerequisites
- Running Kubernetes cluster
- kubectl configured
- Root/sudo access to worker nodes
- Access to CNI configuration directory

### 8.1 Calico CNI Installation and Configuration

#### 8.1.1 Install Calico CNI
```bash
# Download Calico manifest
curl https://docs.projectcalico.org/manifests/calico.yaml -O

# Customize Calico configuration
cat <<EOF > custom-calico-config.yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  # Configure IPv4 pool
  calicoNetwork:
    ipPools:
    - blockSize: 26
      cidr: 192.168.0.0/16
      encapsulation: VXLANCrossSubnet
      natOutgoing: true
      nodeSelector: all()
    nodeAddressAutodetectionV4:
      interface: eth.*
  # Configure MTU
  mtu: 1440
EOF

# Apply Calico configuration
kubectl apply -f custom-calico-config.yaml
kubectl apply -f calico.yaml

# Verify installation
kubectl get pods -n calico-system
```

#### 8.1.2 Configure Calico Network Policies
```yaml
# Create advanced Calico network policy
cat <<EOF | kubectl apply -f -
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: advanced-policy
spec:
  selector: all()
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
    protocol: TCP
    source:
      selector: role == 'frontend'
    destination:
      ports:
      - 80
      - 443
  egress:
  - action: Allow
    protocol: TCP
    destination:
      selector: role == 'database'
      ports:
      - 5432
EOF
```

### 8.2 Weave Net CNI Configuration

#### 8.2.1 Install and Configure Weave Net
```bash
# Create custom Weave Net configuration
cat <<EOF > weave-net-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: weave-net-config
  namespace: kube-system
data:
  network: |
    {
      "Network": "10.32.0.0/12",
      "IPAllocRange": "10.32.0.0/12",
      "IPAllocRangeMask": "255.240.0.0",
      "EnableEncryption": true,
      "Password": "your-secure-password"
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: weave-net
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: weave-net
  template:
    metadata:
      labels:
        name: weave-net
    spec:
      containers:
        - name: weave
          image: weaveworks/weave-kube:latest
          env:
            - name: IPALLOC_RANGE
              value: 10.32.0.0/12
            - name: WEAVE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: weave-net-password
                  key: password
EOF

# Apply Weave Net configuration
kubectl apply -f weave-net-config.yaml
```

### 8.3 Advanced CNI Features

#### 8.3.1 Configure Network Policies with Bandwidth Control
```yaml
# Create NetworkPolicy with bandwidth limits
cat <<EOF | kubectl apply -f -
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: bandwidth-limit
  namespace: network-test
spec:
  selector: app == 'bandwidth-test'
  ingress:
  - action: Allow
    metadata:
      annotations:
        kubernetes.io/ingress-bandwidth: "1M"
  egress:
  - action: Allow
    metadata:
      annotations:
        kubernetes.io/egress-bandwidth: "1M"
EOF

# Create test pod
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: bandwidth-test
  namespace: network-test
  labels:
    app: bandwidth-test
spec:
  containers:
  - name: iperf
    image: networkstatic/iperf3
    command: ["iperf3", "-s"]
EOF
```

### 8.4 CNI Troubleshooting Tools

#### 8.4.1 Setup Debugging Environment
```bash
# Create debugging pod with network tools
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: cni-debug
  namespace: network-test
spec:
  hostNetwork: true
  containers:
  - name: debug
    image: nicolaka/netshoot
    command: ["sleep", "infinity"]
    securityContext:
      privileged: true
    volumeMounts:
    - name: cni
      mountPath: /etc/cni/net.d
    - name: cnibins
      mountPath: /opt/cni/bin
  volumes:
  - name: cni
    hostPath:
      path: /etc/cni/net.d
  - name: cnibins
    hostPath:
      path: /opt/cni/bin
EOF
```

#### 8.4.2 CNI Debugging Commands
```bash
# Check CNI configuration
kubectl exec -n network-test cni-debug -- ls -l /etc/cni/net.d/
kubectl exec -n network-test cni-debug -- cat /etc/cni/net.d/10-calico.conflist

# Check CNI binaries
kubectl exec -n network-test cni-debug -- ls -l /opt/cni/bin/

# Test CNI network
kubectl exec -n network-test cni-debug -- ip addr
kubectl exec -n network-test cni-debug -- ip route
```

### 8.5 Multi-Network Support

#### 8.5.1 Configure Multiple Networks
```yaml
# Create Multus CNI configuration
cat <<EOF | kubectl apply -f -
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan-conf
spec:
  config: '{
    "cniVersion": "0.3.1",
    "type": "macvlan",
    "master": "eth0",
    "mode": "bridge",
    "ipam": {
      "type": "host-local",
      "subnet": "192.168.1.0/24",
      "rangeStart": "192.168.1.200",
      "rangeEnd": "192.168.1.216",
      "routes": [
        { "dst": "0.0.0.0/0" }
      ],
      "gateway": "192.168.1.1"
    }
  }'
---
# Create pod with multiple networks
apiVersion: v1
kind: Pod
metadata:
  name: multi-net-pod
  namespace: network-test
  annotations:
    k8s.v1.cni.cncf.io/networks: macvlan-conf
spec:
  containers:
  - name: multi-net
    image: nicolaka/netshoot
    command: ["sleep", "infinity"]
EOF
```

### Verification Steps

1. Check CNI Installation
```bash
# Verify CNI pods
kubectl get pods -n calico-system
kubectl get pods -n kube-system -l name=weave-net

# Check node status
kubectl get nodes -o wide
```

2. Test Network Connectivity
```bash
# Create test pods
kubectl run -n network-test test-pod-1 --image=busybox -- sleep infinity
kubectl run -n network-test test-pod-2 --image=busybox -- sleep infinity

# Test connectivity
kubectl exec -n network-test test-pod-1 -- ping -c 4 test-pod-2
```

3. Verify Network Policies
```bash
# Test policy enforcement
kubectl exec -n network-test test-pod-1 -- wget -qO- http://test-pod-2
```

### Cleanup
```bash
# Remove test resources
kubectl delete pod -n network-test cni-debug multi-net-pod test-pod-1 test-pod-2
kubectl delete networkattachmentdefinition macvlan-conf
kubectl delete -f custom-calico-config.yaml
```