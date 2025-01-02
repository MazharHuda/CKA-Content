# Chapter 9: Kubernetes Monitoring

## 1. Monitoring Fundamentals

### 1.1 Monitoring Architecture
```ascii
┌─────────────Kubernetes Monitoring Stack──────────────┐
│                                                     │
│  ┌─Metrics─┐    ┌─Collection─┐    ┌─Visualization─┐ │
│  │         │    │            │    │               │ │
│  │• Node   │───►│• Prometheus│───►│• Grafana      │ │
│  │• Pod    │    │• Metrics   │    │• Dashboards   │ │
│  │• Service│    │  Server    │    │• Alerts       │ │
│  └─────────┘    └────────────┘    └───────────────┘ │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 1.2 Key Metrics Categories
1. Node Metrics
   - CPU usage
   - Memory utilization
   - Disk I/O
   - Network traffic

2. Pod Metrics
   - Container CPU/Memory
   - Network statistics
   - File system usage
   - Application metrics

3. Cluster Metrics
   - Control plane health
   - API server latency
   - etcd performance
   - Scheduler decisions

## 2. Metrics Server

### 2.1 Installation and Configuration
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: metrics-server
  namespace: kube-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: metrics-server
  template:
    spec:
      containers:
      - name: metrics-server
        image: k8s.gcr.io/metrics-server/metrics-server:v0.6.1
        args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
```

### 2.2 Resource Metrics Pipeline
```ascii
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Kubelet  │────►│ Metrics   │────►│ API      │
│ /metrics │     │ Server    │     │ Server   │
└──────────┘     └───────────┘     └──────────┘
```

## 3. Prometheus Monitoring

### 3.1 Architecture Components
```yaml
# Prometheus Configuration
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  serviceAccountName: prometheus
  serviceMonitorSelector:
    matchLabels:
      team: frontend
  resources:
    requests:
      memory: 400Mi
  enableAdminAPI: false
```

### 3.2 Service Monitoring
```yaml
# ServiceMonitor Example
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

## 4. Logging Architecture

### 4.1 Container Logging
```ascii
┌─────────────Pod───────────────┐
│                              │
│  ┌──────────┐   ┌─────────┐  │
│  │App       │   │Logging  │  │
│  │Container │   │Sidecar │  │
│  │          │   │        │  │
│  └──────────┘   └─────────┘  │
│        │            │        │
│        └────┬───────┘        │
│             │                │
│      ┌──────▼─────┐         │
│      │Log Volume  │         │
│      └────────────┘         │
└──────────────────────────────┘
```

### 4.2 Logging Solutions
```yaml
# Fluentd DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1.14
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: containers
          mountPath: /var/lib/docker/containers
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: containers
        hostPath:
          path: /var/lib/docker/containers
```

## 5. Alert Management

### 5.1 Alert Rules
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: kubernetes-alerts
spec:
  groups:
  - name: kubernetes
    rules:
    - alert: HighCPUUsage
      expr: container_cpu_usage_seconds_total > 90
      for: 5m
      labels:
        severity: warning
      annotations:
        description: "Container CPU usage is above 90%"
```

### 5.2 Alert Routing
```yaml
# Alertmanager Configuration
apiVersion: monitoring.coreos.com/v1
kind: Alertmanager
metadata:
  name: main
spec:
  replicas: 3
  configSecret: alertmanager-config
```

## 6. Performance Monitoring

### 6.1 Node Performance
```yaml
# Node Exporter Configuration
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    spec:
      containers:
      - name: node-exporter
        image: prom/node-exporter
        ports:
        - containerPort: 9100
```

### 6.2 Application Performance
```yaml
# Custom Metrics API
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  name: v1beta1.custom.metrics.k8s.io
spec:
  service:
    name: custom-metrics-apiserver
    namespace: monitoring
  group: custom.metrics.k8s.io
  version: v1beta1
  insecureSkipTLSVerify: true
  groupPriorityMinimum: 100
  versionPriority: 100
```

## 7. Visualization and Dashboards

### 7.1 Grafana Setup
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  selector:
    matchLabels:
      app: grafana
  template:
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:8.3.0
        ports:
        - containerPort: 3000
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
```

### 7.2 Dashboard Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
data:
  kubernetes-pods.json: |
    {
      "dashboard": {
        "panels": [
          {
            "title": "Pod CPU Usage",
            "type": "graph"
          }
        ]
      }
    }
```

## Best Practices

### 1. Monitoring Strategy
```markdown
- Define clear monitoring objectives
- Implement proper retention policies
- Set up alerting thresholds
- Regular monitoring review
- Automated response procedures
```

### 2. Resource Management
```markdown
- Monitor resource utilization
- Set up resource quotas
- Implement autoscaling
- Track capacity trends
- Plan for growth
```

### 3. Performance Optimization
```markdown
- Monitor key metrics
- Set performance baselines
- Track SLOs/SLIs
- Regular performance testing
- Optimize based on metrics
```

## Common Pitfalls

### 1. Monitoring Configuration
```markdown
- Missing critical metrics
- Improper alert thresholds
- Insufficient data retention
- Poor visualization
- Lack of automation
```

### 2. Operational Issues
```markdown
- Alert fatigue
- Metric data gaps
- Resource exhaustion
- Performance bottlenecks
- Monitoring overhead
```

[Continue with more sections...]
