# Chapter 9: Monitoring - Practice Labs

## Prerequisites
- Running Kubernetes cluster
- kubectl CLI tool configured
- Helm installed (for Prometheus/Grafana installation)
- Basic understanding of monitoring concepts

## Lab 1: Setting Up Metrics Server

### Objective
Install and configure Metrics Server to collect basic resource metrics.

### Tasks

1. Deploy Metrics Server:
```bash
# Create metrics server deployment
cat <<EOF | kubectl apply -f -
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
    metadata:
      labels:
        k8s-app: metrics-server
    spec:
      serviceAccountName: metrics-server
      containers:
      - name: metrics-server
        image: k8s.gcr.io/metrics-server/metrics-server:v0.6.1
        args:
        - --cert-dir=/tmp
        - --secure-port=4443
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
EOF
```

2. Verify Metrics Server Installation:
```bash
# Check if metrics server is running
kubectl get pods -n kube-system | grep metrics-server

# Test metrics collection
kubectl top nodes
kubectl top pods --all-namespaces
```

## Lab 2: Implementing Prometheus Monitoring

### Objective
Set up Prometheus monitoring stack with basic alerting.

### Tasks

1. Install Prometheus Operator:
```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

2. Configure Service Monitor:
```yaml
# Create ServiceMonitor for an application
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

3. Create Alert Rules:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-alerts
  namespace: monitoring
spec:
  groups:
  - name: app.rules
    rules:
    - alert: HighCPUUsage
      expr: container_cpu_usage_seconds_total > 80
      for: 5m
      labels:
        severity: warning
      annotations:
        description: Container CPU usage is above 80%
```

## Lab 3: Setting Up Grafana Dashboards

### Objective
Configure Grafana dashboards for visualizing cluster metrics.

### Tasks

1. Access Grafana Dashboard:
```bash
# Get Grafana admin password
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward Grafana service
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

2. Create Custom Dashboard:
```json
{
  "dashboard": {
    "id": null,
    "title": "Kubernetes Cluster Monitoring",
    "panels": [
      {
        "title": "CPU Usage",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)"
          }
        ]
      }
    ]
  }
}
```

## Lab 4: Implementing Logging Solutions

### Objective
Set up centralized logging using Elasticsearch, Fluentd, and Kibana (EFK stack).

### Tasks

1. Deploy Elasticsearch:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
  namespace: logging
spec:
  serviceName: elasticsearch
  replicas: 3
  template:
    spec:
      containers:
      - name: elasticsearch
        image: docker.elastic.co/elasticsearch/elasticsearch:7.9.3
        env:
        - name: discovery.type
          value: single-node
        ports:
        - containerPort: 9200
          name: http
        - containerPort: 9300
          name: transport
```

2. Configure Fluentd DaemonSet:
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
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

## Lab 5: Implementing Custom Metrics

### Objective
Set up custom metrics collection and monitoring.

### Tasks

1. Create Custom Metrics API:
```yaml
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

2. Configure Custom Metrics Adapter:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-metrics-adapter
  namespace: monitoring
spec:
  template:
    spec:
      containers:
      - name: custom-metrics-adapter
        image: custom-metrics-adapter:v1.0
        args:
        - --secure-port=6443
        - --tls-cert-file=/etc/adapter/cert.pem
        - --tls-private-key-file=/etc/adapter/key.pem
```

## Verification Tasks

1. Check Metrics Collection:
```bash
# Verify node metrics
kubectl top nodes

# Verify pod metrics
kubectl top pods --all-namespaces

# Check Prometheus targets
kubectl port-forward -n monitoring svc/prometheus-operated 9090:9090
```

2. Test Alerting:
```bash
# Create high load
kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do dd if=/dev/zero of=/dev/null; done"

# Check alerts in Prometheus
kubectl port-forward -n monitoring svc/alertmanager-operated 9093:9093
```

3. Verify Logging:
```bash
# Check Fluentd logs
kubectl logs -n logging -l name=fluentd

# Access Kibana dashboard
kubectl port-forward -n logging svc/kibana 5601:5601
```

## Best Practices

1. Monitoring Setup
```markdown
- Use persistent storage for metrics
- Implement proper retention policies
- Configure appropriate scrape intervals
- Set up alerting thresholds
- Regular backup of dashboards
```

2. Resource Management
```markdown
- Monitor resource usage
- Set up resource quotas
- Configure HPA based on metrics
- Track capacity trends
- Plan for scaling
```

## Cleanup

```bash
# Remove monitoring stack
helm uninstall prometheus -n monitoring
kubectl delete namespace monitoring

# Remove logging stack
kubectl delete namespace logging

# Remove metrics server
kubectl delete -f metrics-server.yaml
```

## Tips for CKA Exam

1. Know how to verify cluster metrics using kubectl top
2. Understand basic Prometheus configuration
3. Be familiar with logging architecture
4. Practice troubleshooting monitoring issues
5. Know how to set up basic monitoring tools
