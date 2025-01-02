# Chapter 6: Kubernetes Networking - Real-world Scenarios

## Scenario 1: E-commerce Platform Network Architecture

### Context
A large e-commerce company needs to migrate their monolithic application to a microservices architecture on Kubernetes, requiring secure and efficient network communication between services.

### Requirements
- Secure service-to-service communication
- External access through load balancers
- Network isolation between environments
- High availability
- Performance monitoring
- DDoS protection

### Solution

#### 1. Network Architecture
```ascii
┌─────────────────────E-commerce Platform────────────────────┐
│                                                           │
│  ┌─Public Zone─────┐    ┌─App Zone────┐    ┌─DB Zone──┐  │
│  │                 │    │             │    │          │  │
│  │ ┌─Ingress─┐    │    │ ┌─────┐     │    │ ┌────┐  │  │
│  │ │  NGINX  │    │    │ │Cart │     │    │ │Main│  │  │
│  │ └────┬────┘    │    │ └──┬──┘     │    │ │ DB │  │  │
│  │      │         │    │    │        │    │ └────┘  │  │
│  │ ┌────┴────┐    │    │ ┌──┴──┐     │    │ ┌────┐  │  │
│  │ │  WAF    │    │    │ │Order│     │    │ │User│  │  │
│  │ └─────────┘    │    │ └─────┘     │    │ │ DB │  │  │
│  └─────────────────┘    └─────────────┘    └──────┘  │  │
│                                                       │  │
└───────────────────────────────────────────────────────┘  │
```

#### 2. Network Policy Implementation
```yaml
# Frontend Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app: frontend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 0.0.0.0/0
        except:
        - 10.0.0.0/8
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: api
    ports:
    - protocol: TCP
      port: 8080

# Database Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: ecommerce
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api
    ports:
    - protocol: TCP
      port: 5432
```

#### 3. Service Configuration
```yaml
# Frontend Service
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: ecommerce
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: frontend

# API Service
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: ecommerce
spec:
  type: ClusterIP
  ports:
  - port: 8080
    targetPort: 8080
  selector:
    app: api
```

### Implementation Steps

1. Network Segmentation
```bash
# Create namespaces
kubectl create namespace ecommerce-prod
kubectl create namespace ecommerce-staging

# Label namespaces
kubectl label namespace ecommerce-prod environment=production
kubectl label namespace ecommerce-staging environment=staging
```

2. Security Implementation
```yaml
# TLS Secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
  namespace: ecommerce
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>

# Ingress Configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - shop.example.com
    secretName: tls-secret
  rules:
  - host: shop.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

3. Monitoring Setup
```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-monitor
spec:
  selector:
    matchLabels:
      app: ecommerce
  endpoints:
  - port: metrics
```

### Best Practices

1. Security
```markdown
- Implement network policies by default
- Use TLS for all services
- Regular security audits
- Monitor network traffic
- Implement rate limiting
```

2. Performance
```markdown
- Use appropriate service types
- Optimize network policies
- Monitor network metrics
- Configure proper health checks
- Implement caching
```

3. Maintenance
```markdown
- Regular certificate rotation
- Monitor network usage
- Update security policies
- Backup configurations
- Document network topology
```

### Common Pitfalls

1. Network Policy Issues
```markdown
- Over-restrictive policies
- Missing egress rules
- Incorrect selectors
- Policy conflicts
- Missing default policies
```

2. Service Problems
```markdown
- Incorrect service type selection
- Missing health checks
- Improper load balancing
- Certificate management
- DNS configuration
```

### Monitoring and Alerts

1. Network Metrics
```yaml
# Prometheus Alert Rules
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: network-alerts
spec:
  groups:
  - name: network
    rules:
    - alert: HighLatency
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
      for: 5m
      labels:
        severity: warning
```

2. Health Checks
```yaml
# Readiness Probe
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

[Continue with more scenarios...]

## Scenario 2: Multi-cluster Networking Implementation

### Context
A global financial services company needs to implement a multi-cluster Kubernetes architecture across different regions for high availability, disaster recovery, and regulatory compliance.

### Requirements
- Cross-cluster communication
- Regional data compliance
- Automatic failover
- Service discovery
- Traffic routing
- Security compliance
- Performance monitoring

### Solution

#### 1. Multi-cluster Architecture
```ascii
┌─────────────────Global Load Balancer──────────────────┐
│                                                       │
│           ┌─────────────┐    ┌─────────────┐         │
│           │ US Cluster  │    │ EU Cluster  │         │
│           └──────┬──────┘    └──────┬──────┘         │
│                  │                  │                 │
└──────────────────┼──────────────────┼─────────────────┘
                   │                  │
     ┌────────────▼──────┐  ┌────────▼──────────┐
     │   US Region       │  │    EU Region      │
     │                   │  │                    │
     │ ┌─Apps─┐ ┌─Data─┐│  │ ┌─Apps─┐ ┌─Data─┐ │
     │ │Pod A │ │Pod B ││  │ │Pod A │ │Pod B │ │
     │ └──────┘ └──────┘│  │ └──────┘ └──────┘ │
     └───────────────────┘  └────────────────────┘
```

#### 2. Cross-Cluster Service Discovery
```yaml
# Service Export Configuration (US Cluster)
apiVersion: multicluster.k8s.io/v1alpha1
kind: ServiceExport
metadata:
  name: financial-app
  namespace: prod
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
---
# Service Import Configuration (EU Cluster)
apiVersion: multicluster.k8s.io/v1alpha1
kind: ServiceImport
metadata:
  name: financial-app
  namespace: prod
spec:
  type: ClusterSetIP
  ports:
  - name: http
    port: 80
  ips:
  - 10.96.0.1
```

#### 3. Multi-cluster Network Policy
```yaml
# Global Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cross-cluster-policy
  namespace: prod
spec:
  podSelector:
    matchLabels:
      app: financial-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/14  # US Cluster CIDR
    - ipBlock:
        cidr: 10.4.0.0/14  # EU Cluster CIDR
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/14
    - ipBlock:
        cidr: 10.4.0.0/14
    ports:
    - protocol: TCP
      port: 8080
```

#### 4. Load Balancing Configuration
```yaml
# Global Load Balancer Configuration
apiVersion: v1
kind: Service
metadata:
  name: global-financial-app
  annotations:
    global.load.balancer/config: |
      {
        "clusters": ["us-east", "eu-west"],
        "strategy": "geo",
        "failover": {
          "default": "us-east",
          "regions": {
            "europe": "eu-west",
            "america": "us-east"
          }
        }
      }
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8080
  selector:
    app: financial-app
```

### Implementation Steps

1. Cluster Federation Setup
```bash
# Install Federation Control Plane
kubectl apply -f federation-namespace.yaml
kubectl apply -f federation-controller.yaml

# Join Clusters
kubefed join us-cluster \
  --cluster-context=us-cluster \
  --host-cluster-context=host-cluster \
  --v=2

kubefed join eu-cluster \
  --cluster-context=eu-cluster \
  --host-cluster-context=host-cluster \
  --v=2
```

2. Cross-Cluster Service Configuration
```yaml
# Service DNS Configuration
apiVersion: multicluster.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: financial-app
  namespace: prod
spec:
  endpoints:
  - dnsName: financial-app.global.example.com
    recordTTL: 180
    recordType: A
    targets:
    - 10.0.0.1  # US Cluster VIP
    - 10.4.0.1  # EU Cluster VIP
```

3. Data Replication Setup
```yaml
# Database StatefulSet with Replication
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: financial-db
spec:
  replicas: 3
  serviceName: financial-db
  template:
    spec:
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: financial
        - name: REPLICATION_MODE
          value: "master"
        - name: REPLICATION_USER
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: replication-user
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
```

### Monitoring and Observability

1. Cross-Cluster Metrics
```yaml
# Prometheus Federation Configuration
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: cross-cluster-monitor
spec:
  endpoints:
  - interval: 30s
    port: metrics
  selector:
    matchLabels:
      app: financial-app
  namespaceSelector:
    matchNames:
    - prod
```

2. Distributed Tracing
```yaml
# Jaeger Configuration
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: global-tracer
spec:
  strategy: production
  storage:
    type: elasticsearch
  ingress:
    enabled: true
```

### Best Practices

1. Network Design
```markdown
- Plan IP ranges carefully
- Implement proper segmentation
- Use consistent naming
- Document topology
- Regular failover testing
```

2. Security Implementation
```markdown
- Encrypt cross-cluster traffic
- Implement strict policies
- Regular security audits
- Certificate management
- Access control
```

3. Performance Optimization
```markdown
- Use regional endpoints
- Implement caching
- Monitor latency
- Optimize routing
- Regular testing
```

### Common Pitfalls

1. Network Issues
```markdown
- IP range conflicts
- DNS resolution problems
- Routing misconfiguration
- Certificate issues
- Policy conflicts
```

2. Operational Challenges
```markdown
- Complex troubleshooting
- Inconsistent configurations
- Data synchronization
- Monitoring complexity
- Failover issues
```

### Disaster Recovery Plan

1. Failover Procedure
```bash
# Check cluster health
kubectl get nodes --context=us-cluster
kubectl get nodes --context=eu-cluster

# Verify service status
kubectl get services --all-namespaces --context=us-cluster
kubectl get services --all-namespaces --context=eu-cluster

# Initiate failover
kubectl patch svc global-financial-app \
  -p '{"metadata":{"annotations":{"global.load.balancer/active":"eu-west"}}}'
```

2. Recovery Steps
```markdown
- Verify data consistency
- Check replication status
- Update DNS records
- Test applications
- Monitor performance
```

## Scenario 3: Service Mesh Implementation

### Context
A large technology company needs to implement a service mesh to manage microservices communication, security, and observability across their Kubernetes clusters.

### Requirements
- Service-to-service encryption
- Traffic management
- Observability
- Access control
- Load balancing
- Circuit breaking
- Fault injection
- API gateway integration

### Solution

#### 1. Service Mesh Architecture
```ascii
┌─────────────────Service Mesh Architecture──────────────────┐
│                                                           │
│  ┌─Control Plane──────────────────────┐                   │
│  │                                    │                   │
│  │  ┌─Istiod─┐    ┌─Cert Manager─┐   │                   │
│  │  │        │    │              │   │                   │
│  │  └────────┘    └──────────────┘   │                   │
│  │                                    │                   │
│  └────────────────────────────────────┘                   │
│                                                           │
│  ┌─Data Plane───────────────────────────────────────┐     │
│  │                                                  │     │
│  │  ┌─Pod──────────┐      ┌─Pod──────────┐         │     │
│  │  │ ┌─App──┐     │      │ ┌─App──┐     │         │     │
│  │  │ │      │     │      │ │      │     │         │     │
│  │  │ └──────┘     │      │ └──────┘     │         │     │
│  │  │ ┌─Envoy─┐    │      │ ┌─Envoy─┐    │         │     │
│  │  │ │Proxy  │    │      │ │Proxy  │    │         │     │
│  │  │ └───────┘    │      │ └───────┘    │         │     │
│  │  └──────────────┘      └──────────────┘         │     │
│  └──────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────┘
```

#### 2. Istio Installation and Configuration
```yaml
# IstioOperator Configuration
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-control-plane
spec:
  profile: default
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 2048Mi
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 1024Mi
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
      mtls:
        enabled: true
```

#### 3. Traffic Management Configuration
```yaml
# Virtual Service for Traffic Routing
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: microservice-routes
spec:
  hosts:
  - microservice.example.com
  gateways:
  - microservice-gateway
  http:
  - match:
    - headers:
        user-type:
          exact: premium
    route:
    - destination:
        host: premium-service
        subset: v2
      weight: 90
    - destination:
        host: premium-service
        subset: v1
      weight: 10
---
# Destination Rule for Load Balancing
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: microservice-destination
spec:
  host: microservice-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 1024
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```

#### 4. Security Configuration
```yaml
# Authentication Policy
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
---
# Authorization Policy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: microservice-auth
spec:
  selector:
    matchLabels:
      app: microservice
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/service-a"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/v1/*"]
```

#### 5. Observability Setup
```yaml
# Prometheus Configuration
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-monitor
  namespace: istio-system
spec:
  selector:
    matchLabels:
      istio: pilot
  endpoints:
  - port: http-monitoring
---
# Grafana Dashboard Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-grafana-dashboards
  namespace: istio-system
data:
  istio-mesh-dashboard.json: |
    {
      "dashboard": {
        "panels": [
          {
            "title": "Request Rate",
            "type": "graph"
          }
        ]
      }
    }
```

### Implementation Steps

1. Install Service Mesh
```bash
# Install Istio
istioctl install -f istio-operator.yaml

# Enable sidecar injection
kubectl label namespace default istio-injection=enabled

# Verify installation
istioctl verify-install
```

2. Configure Traffic Management
```bash
# Apply Virtual Service
kubectl apply -f virtual-service.yaml

# Apply Destination Rules
kubectl apply -f destination-rule.yaml

# Verify configuration
istioctl analyze
```

3. Setup Monitoring
```bash
# Install monitoring stack
kubectl apply -f istio-monitoring.yaml

# Verify monitoring setup
kubectl -n istio-system get svc prometheus
kubectl -n istio-system get svc grafana
```

### Best Practices

1. Security
```markdown
- Enable mTLS by default
- Implement least privilege
- Regular security audits
- Certificate rotation
- Monitor security events
```

2. Performance
```markdown
- Optimize proxy resources
- Configure circuit breakers
- Monitor latency
- Set appropriate timeouts
- Regular performance testing
```

3. Observability
```markdown
- Implement distributed tracing
- Set up metrics collection
- Configure proper logging
- Create dashboards
- Set up alerts
```

### Common Pitfalls

1. Implementation Issues
```markdown
- Resource constraints
- Complex configurations
- Version mismatches
- Proxy conflicts
- Performance impact
```

2. Operational Challenges
```markdown
- Debugging complexity
- Certificate management
- Configuration drift
- Monitoring overhead
- Update procedures
```

### Monitoring and Alerts

1. Service Mesh Metrics
```yaml
# Alert Rules
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-mesh-alerts
spec:
  groups:
  - name: istio.rules
    rules:
    - alert: HighLatency
      expr: istio_request_duration_milliseconds_sum{reporter="destination"} > 1000
      for: 5m
      labels:
        severity: warning
```

2. Health Checks
```yaml
# Liveness Probe
livenessProbe:
  httpGet:
    path: /health
    port: 15020
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Scenario 4: Edge Computing Network Setup

### Context
A manufacturing company needs to implement edge computing across multiple factory locations, processing IoT sensor data locally while maintaining connectivity with the central cloud infrastructure.

### Requirements
- Local data processing
- Low latency networking
- Offline operation capability
- Data synchronization
- Security compliance
- Resource optimization
- Remote management

### Solution

#### 1. Edge Computing Architecture
```ascii
┌─Cloud Data Center──────────────────────────────────────┐
│                                                       │
│  ┌─Central Control Plane─┐   ┌─Data Aggregation─┐     │
│  │                      │   │                   │     │
│  │  ┌─Management──┐     │   │  ┌─Analytics─┐    │     │
│  │  │            │     │   │  │          │    │     │
│  │  └────────────┘     │   │  └──────────┘    │     │
│  └──────────┬──────────┘   └────────┬─────────┘     │
│             │                       │                │
└─────────────┼───────────────────────┼────────────────┘
              │                       │
┌─────────────┼───────────────────────┼────────────────┐
│  ┌─Edge Location 1─┐   ┌─Edge Location 2─┐           │
│  │                 │   │                 │           │
│  │  ┌─K3s────┐     │   │  ┌─K3s────┐     │           │
│  │  │        │     │   │  │        │     │           │
│  │  └────────┘     │   │  └────────┘     │           │
│  │  ┌─IoT Data┐    │   │  ┌─IoT Data┐    │           │
│  │  │         │    │   │  │         │    │           │
│  │  └─────────┘    │   │  └─────────┘    │           │
│  └─────────────────┘   └─────────────────┘           │
└───────────────────────────────────────────────────────┘
```

#### 2. Edge Cluster Configuration
```yaml
# K3s Configuration
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: edge-cluster
  namespace: kube-system
spec:
  repo: https://k3s.io/k3s-charts
  chart: k3s
  version: v1.21
  set:
    global.clusterCIDR: "10.42.0.0/16"
    global.serviceCIDR: "10.43.0.0/16"
    global.clusterDNS: "10.43.0.10"
    k3s:
      args:
      - --disable=traefik
      - --disable=servicelb
      - --disable=metrics-server
      - --node-label=edge-location=factory-1
```

#### 3. Local Data Processing
```yaml
# Edge Data Processor
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edge-processor
  namespace: edge-processing
spec:
  replicas: 2
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: edge-location
                operator: Exists
      containers:
      - name: processor
        image: edge-processor:v1
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
        volumeMounts:
        - name: local-storage
          mountPath: /data
      volumes:
      - name: local-storage
        persistentVolumeClaim:
          claimName: local-pvc
```

#### 4. Data Synchronization
```yaml
# Data Sync Job
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: data-sync
spec:
  schedule: "*/15 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: sync
            image: data-sync:v1
            env:
            - name: CLOUD_ENDPOINT
              valueFrom:
                configMapKeyRef:
                  name: sync-config
                  key: cloud-endpoint
            - name: SYNC_TOKEN
              valueFrom:
                secretKeyRef:
                  name: sync-secrets
                  key: token
```

#### 5. Edge Network Security
```yaml
# Network Policy for Edge Services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: edge-network-policy
spec:
  podSelector:
    matchLabels:
      app: data-processor
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          type: sensor
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/8
        except:
        - 10.255.255.255/32
```

#### 6. Local Load Balancing
```yaml
# MetalLB Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.1.240-192.168.1.250
```

### Implementation Steps

1. Edge Node Setup
```bash
# Install K3s
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--node-label=edge-location=factory-1" sh -

# Verify installation
k3s kubectl get nodes
```

2. Configure Local Storage
```yaml
# Local Storage Class
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

3. Setup Monitoring
```yaml
# Prometheus Edge Configuration
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: edge-prometheus
spec:
  retention: 24h
  resources:
    requests:
      memory: 400Mi
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: local-storage
        resources:
          requests:
            storage: 40Gi
```

### Best Practices

1. Resource Management
```markdown
- Implement resource limits
- Use local storage efficiently
- Configure proper scheduling
- Monitor resource usage
- Implement cleanup policies
```

2. Network Optimization
```markdown
- Use appropriate CNI plugin
- Implement traffic prioritization
- Configure proper MTU
- Monitor bandwidth usage
- Optimize DNS caching
```

3. Security Implementation
```markdown
- Secure edge communication
- Implement access controls
- Regular security updates
- Monitor security events
- Encrypt sensitive data
```

### Common Pitfalls

1. Network Issues
```markdown
- Bandwidth limitations
- Latency problems
- DNS resolution issues
- Network partitioning
- Synchronization failures
```

2. Resource Constraints
```markdown
- Storage limitations
- CPU/Memory pressure
- Network bottlenecks
- Power constraints
- Temperature issues
```

### Monitoring and Alerts

1. Edge Metrics
```yaml
# Alert Rules
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: edge-alerts
spec:
  groups:
  - name: edge.rules
    rules:
    - alert: EdgeNodeDown
      expr: up{job="edge-node"} == 0
      for: 5m
      labels:
        severity: critical
```

2. Data Synchronization Monitoring
```yaml
# Sync Status Check
apiVersion: v1
kind: ConfigMap
metadata:
  name: sync-check
data:
  check.sh: |
    #!/bin/bash
    if [[ $(find /data -mmin +30 -type f) ]]; then
      echo "Data sync delayed"
      exit 1
    fi
```

## Scenario 5: Hybrid Cloud Networking Setup

### Context
A large enterprise needs to implement a hybrid cloud architecture connecting their on-premises data center with multiple cloud providers while maintaining security, performance, and compliance requirements.

### Requirements
- Secure cross-cloud connectivity
- Consistent networking policies
- Service discovery
- Load balancing
- Disaster recovery
- Compliance monitoring
- Traffic optimization

### Solution

#### 1. Hybrid Cloud Architecture
```ascii
┌─On-Premises DC──────────────────────────────────────┐
│                                                     │
│  ┌─K8s Cluster─┐    ┌─Legacy Apps─┐   ┌─Storage─┐  │
│  │             │    │             │   │        │  │
│  │ ┌─Apps─┐    │    │ ┌─Apps─┐    │   │ ┌─NFS─┐│  │
│  │ │      │    │    │ │      │    │   │ │    ││  │
│  │ └──────┘    │    │ └──────┘    │   │ └────┘│  │
│  └─────┬───────┘    └──────┬──────┘   └───────┘  │
│        │                   │                      │
│  ┌─────▼───────────────────▼──────┐              │
│  │     Express Route/Direct Connect│              │
│  └─────────────┬─────────────────┬┘              │
└────────────────┼─────────────────┼───────────────┘
                 │                 │
    ┌────────────▼───┐      ┌─────▼────────┐
    │   AWS Cloud    │      │  Azure Cloud  │
    │  ┌─K8s────┐   │      │  ┌─AKS────┐   │
    │  │        │   │      │  │        │   │
    │  └────────┘   │      │  └────────┘   │
    └───────────────┘      └──────────────┘
```

#### 2. Cross-Cloud Network Configuration
```yaml
# AWS Transit Gateway Configuration
apiVersion: eks.aws.k8s.io/v1alpha1
kind: TransitGatewayConfig
metadata:
  name: hybrid-transit
spec:
  region: us-west-2
  routes:
    - destinationCidrBlock: "10.0.0.0/8"
      transitGatewayId: tgw-xxxxx
  vpcs:
    - vpcId: vpc-xxxxx
      subnets:
        - subnet-xxxxx
        - subnet-yyyyy

# Azure Virtual Network Configuration
apiVersion: network.azure.com/v1alpha1
kind: VirtualNetwork
metadata:
  name: hybrid-vnet
spec:
  addressSpace:
    addressPrefixes:
    - "172.16.0.0/16"
  subnets:
  - name: aks-subnet
    properties:
      addressPrefix: "172.16.1.0/24"
```

#### 3. Service Discovery Setup
```yaml
# External DNS Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: external-dns-config
  namespace: kube-system
data:
  hybrid-dns.conf: |
    domain-name: "hybrid.example.com"
    zones:
      - name: "on-prem"
        domain: "onprem.hybrid.example.com"
        servers: ["10.0.0.53"]
      - name: "aws"
        domain: "aws.hybrid.example.com"
        servers: ["172.16.0.53"]
      - name: "azure"
        domain: "azure.hybrid.example.com"
        servers: ["192.168.0.53"]
```

#### 4. Cross-Cloud Network Policy
```yaml
# Network Policy for Cross-Cloud Communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cross-cloud-policy
spec:
  podSelector:
    matchLabels:
      app: hybrid-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.0/8  # On-prem
    - ipBlock:
        cidr: 172.16.0.0/16  # AWS
    - ipBlock:
        cidr: 192.168.0.0/16  # Azure
    ports:
    - protocol: TCP
      port: 443
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/8
    - ipBlock:
        cidr: 172.16.0.0/16
    - ipBlock:
        cidr: 192.168.0.0/16
```

#### 5. Load Balancing Configuration
```yaml
# Global Load Balancer Setup
apiVersion: v1
kind: Service
metadata:
  name: global-app
  annotations:
    global.load.balancer/type: "hybrid"
    global.load.balancer/config: |
      {
        "locations": {
          "on-prem": {
            "weight": 40,
            "priority": 1
          },
          "aws": {
            "weight": 30,
            "priority": 2
          },
          "azure": {
            "weight": 30,
            "priority": 2
          }
        }
      }
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8443
  selector:
    app: hybrid-app
```

### Implementation Steps

1. Network Connectivity Setup
```bash
# Configure VPN/Direct Connect
aws directconnect create-connection \
  --location "DX-Location" \
  --bandwidth "1Gbps" \
  --connection-name "hybrid-connection"

# Setup Azure ExpressRoute
az network express-route create \
  --name "hybrid-expressroute" \
  --resource-group "hybrid-rg" \
  --location "eastus" \
  --bandwidth "1000" \
  --provider "Provider"
```

2. DNS Configuration
```bash
# Configure CoreDNS for hybrid setup
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns-custom
  namespace: kube-system
data:
  hybrid.server: |
    hybrid.example.com {
        forward . 10.0.0.53 172.16.0.53 192.168.0.53
        cache 30
    }
EOF
```

3. Monitoring Setup
```yaml
# Cross-Cloud Monitoring
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: hybrid-monitor
spec:
  endpoints:
  - interval: 30s
    port: metrics
  selector:
    matchLabels:
      app: hybrid-app
```

### Best Practices

1. Network Design
```markdown
- Plan IP address spaces carefully
- Implement redundant connections
- Use consistent CIDR blocks
- Document network topology
- Regular connectivity testing
```

2. Security Implementation
```markdown
- Encrypt all cross-cloud traffic
- Implement strict network policies
- Regular security audits
- Monitor traffic patterns
- Implement access controls
```

3. Performance Optimization
```markdown
- Use regional endpoints
- Implement caching
- Monitor latency
- Optimize routing
- Regular testing
```

### Common Pitfalls

1. Network Issues
```markdown
- IP range conflicts
- DNS resolution problems
- Routing misconfiguration
- Bandwidth limitations
- Latency issues
```

2. Operational Challenges
```markdown
- Complex troubleshooting
- Configuration drift
- Cost management
- Compliance monitoring
- Performance bottlenecks
```

### Monitoring and Alerts

1. Network Metrics
```yaml
# Alert Rules
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: hybrid-network-alerts
spec:
  groups:
  - name: hybrid.rules
    rules:
    - alert: CrossCloudLatencyHigh
      expr: hybrid_network_latency_seconds > 0.5
      for: 5m
      labels:
        severity: warning
```

2. Health Checks
```yaml
# Health Check Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-config
data:
  check-connectivity.sh: |
    #!/bin/bash
    locations=("on-prem" "aws" "azure")
    for loc in "${locations[@]}"; do
      if ! ping -c 1 "${loc}-endpoint" &>/dev/null; then
        echo "Connectivity to ${loc} failed"
        exit 1
      fi
    done
```

