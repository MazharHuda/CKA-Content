# Chapter 9: Monitoring - Real-world Scenarios

## Scenario 1: Implementing Production Monitoring Stack

### Context
A large e-commerce company needs to set up comprehensive monitoring for their Kubernetes cluster running critical applications.

### Requirements
- Real-time metrics collection
- Automated alerting
- Performance monitoring
- Log aggregation
- Visualization dashboards

### Solution

#### 1. Prometheus Stack Deployment
```yaml
# Prometheus Configuration
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
  namespace: monitoring
spec:
  serviceAccountName: prometheus
  serviceMonitorSelector:
    matchLabels:
      team: devops
  resources:
    requests:
      memory: "2Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "1000m"
  retention: 15d
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 100Gi
```

#### 2. Alert Configuration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: critical-alerts
  namespace: monitoring
spec:
  groups:
  - name: node.rules
    rules:
    - alert: HighNodeCPU
      expr: instance:node_cpu_utilisation:rate5m > 0.8
      for: 10m
      labels:
        severity: critical
        team: infrastructure
      annotations:
        summary: "High CPU usage on {{ $labels.instance }}"
        description: "CPU usage is above 80% for more than 10 minutes"
```

### Implementation Steps

1. Deploy Monitoring Stack:
```bash
# Install Prometheus Operator
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.enabled=true \
  --set alertmanager.enabled=true
```

2. Configure Service Monitoring:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: ecommerce
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

## Scenario 2: Multi-Cluster Monitoring

### Context
A company needs to implement centralized monitoring for multiple Kubernetes clusters across different regions.

### Requirements
- Centralized metrics collection
- Cross-cluster visibility
- Regional performance comparison
- Unified alerting
- Data retention policies

### Solution

#### 1. Thanos Configuration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  thanos:
    baseImage: quay.io/thanos/thanos
    version: v0.24.0
    objectStorageConfig:
      key: thanos.yaml
      name: thanos-objstore-config
  externalLabels:
    cluster: us-east-1
    replica: 0
```

#### 2. Global View Setup
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thanos-query
spec:
  template:
    spec:
      containers:
      - name: thanos-query
        image: quay.io/thanos/thanos:v0.24.0
        args:
        - query
        - --store=dnssrv+_grpc._tcp.thanos-store-0.monitoring.svc.cluster.local
        - --store=dnssrv+_grpc._tcp.thanos-store-1.monitoring.svc.cluster.local
```

## Scenario 3: Application Performance Monitoring

### Context
A development team needs to implement detailed application monitoring with custom metrics.

### Requirements
- Custom metrics collection
- Performance tracking
- Error rate monitoring
- Latency measurements
- Resource utilization

### Solution

#### 1. Custom Metrics Configuration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-metrics
spec:
  endpoints:
  - port: http-metrics
    path: /metrics
    interval: 15s
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'http_requests_total'
      action: keep
  selector:
    matchLabels:
      app: web-service
```

#### 2. HPA with Custom Metrics
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 1k
```

## Scenario 4: Log Management at Scale

### Context
An organization needs to implement centralized logging for their Kubernetes environment.

### Requirements
- Centralized log collection
- Log parsing and indexing
- Search capabilities
- Log retention policies
- Access control

### Solution

#### 1. Fluentd DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: logging
spec:
  template:
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1.14
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch-logging"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
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

#### 2. Elasticsearch Configuration
```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: logging
spec:
  version: 7.15.0
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        resources:
          requests:
            storage: 100Gi
```

### Best Practices

1. Monitoring Strategy
```markdown
- Define clear monitoring objectives
- Implement proper retention policies
- Set up alerting thresholds
- Regular monitoring review
- Automated response procedures
```

2. Resource Management
```markdown
- Monitor resource utilization
- Set up resource quotas
- Implement autoscaling
- Track capacity trends
- Plan for growth
```

3. Performance Optimization
```markdown
- Monitor key metrics
- Set performance baselines
- Track SLOs/SLIs
- Regular performance testing
- Optimize based on metrics
```

### Common Pitfalls

1. Monitoring Configuration
```markdown
- Missing critical metrics
- Improper alert thresholds
- Insufficient data retention
- Poor visualization
- Lack of automation
```

2. Operational Issues
```markdown
- Alert fatigue
- Metric data gaps
- Resource exhaustion
- Performance bottlenecks
- Monitoring overhead
```

## Scenario 5: High-Performance Metrics Collection

### Context
A financial services company needs to implement high-performance metrics collection for their trading platform with minimal latency impact.

### Requirements
- Low-latency metrics collection
- High-frequency sampling
- Efficient storage
- Query optimization
- Resource efficiency

### Solution

#### 1. High-Performance Prometheus Configuration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: trading-prometheus
spec:
  replicas: 2
  shards: 2
  resources:
    requests:
      memory: "8Gi"
      cpu: "4"
    limits:
      memory: "16Gi"
      cpu: "8"
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 500Gi
  ruleSelector:
    matchLabels:
      role: trading-alerts
  query:
    maxSamples: 100000000
    maxConcurrency: 16
    lookbackDelta: 1m
```

#### 2. Recording Rules for Performance
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: trading-recording-rules
spec:
  groups:
  - name: trading.rules
    interval: 10s
    rules:
    - record: trading:order_latency:avg_5m
      expr: |
        rate(order_processing_duration_seconds_sum[5m])
        /
        rate(order_processing_duration_seconds_count[5m])
```

## Scenario 6: Compliance Monitoring

### Context
A healthcare organization needs to implement monitoring that meets HIPAA compliance requirements.

### Requirements
- Audit logging
- Access tracking
- Data encryption
- Compliance reporting
- Alert management

### Solution

#### 1. Audit Configuration
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: compliance-audit
spec:
  rules:
  - level: RequestResponse
    resources:
    - group: ""
      resources: ["secrets", "configmaps", "pods"]
    omitStages:
      - RequestReceived
  - level: Metadata
    resources:
    - group: "apps"
      resources: ["deployments", "statefulsets"]
```

#### 2. Compliance Monitoring Rules
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: compliance-alerts
spec:
  groups:
  - name: compliance.rules
    rules:
    - alert: UnauthorizedAccess
      expr: rate(apiserver_request_total{code=~"4.."}[5m]) > 10
      for: 5m
      labels:
        severity: critical
        compliance: hipaa
      annotations:
        summary: High rate of unauthorized access attempts
```

## Scenario 7: Disaster Recovery Monitoring

### Context
An organization needs to implement comprehensive monitoring for their disaster recovery procedures.

### Requirements
- Cross-site monitoring
- Backup verification
- Recovery time tracking
- Failover monitoring
- SLA compliance

### Solution

#### 1. Cross-Site Monitoring Configuration
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: dr-prometheus
spec:
  replicas: 2
  externalLabels:
    site: dr-site
  remoteWrite:
    - url: http://central-prometheus/api/v1/write
      writeRelabelConfigs:
      - sourceLabels: [__name__]
        regex: 'backup_.*|recovery_.*'
        action: keep
```

#### 2. Recovery Metrics Collection
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: recovery-monitor
spec:
  selector:
    matchLabels:
      app: dr-metrics
  endpoints:
  - port: metrics
    interval: 30s
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'recovery_.*'
      action: keep
```

## Scenario 8: Machine Learning Operations Monitoring

### Context
A data science team needs to monitor their ML model training and inference operations.

### Requirements
- Model performance metrics
- Resource utilization
- Training progress
- Inference latency
- Data pipeline monitoring

### Solution

#### 1. ML Metrics Collection
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ml-monitor
spec:
  selector:
    matchLabels:
      app: ml-platform
  endpoints:
  - port: metrics
    path: /metrics
    interval: 15s
    metricRelabelings:
    - sourceLabels: [__name__]
      regex: 'model_.*|training_.*|inference_.*'
      action: keep
```

#### 2. ML Performance Alerts
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ml-alerts
spec:
  groups:
  - name: ml.rules
    rules:
    - alert: ModelAccuracyDrop
      expr: |
        model_accuracy_score < 0.95 and
        rate(model_prediction_requests_total[1h]) > 100
      for: 15m
      labels:
        severity: warning
      annotations:
        summary: "Model accuracy below threshold"
```

### Best Practices for Advanced Monitoring

1. Performance Optimization
```markdown
- Use efficient metric collection
- Implement proper data retention
- Optimize query performance
- Scale monitoring infrastructure
- Use recording rules for complex queries
```

2. High Availability
```markdown
- Deploy redundant monitoring
- Implement cross-site monitoring
- Configure proper failover
- Regular backup of monitoring data
- Test recovery procedures
```

3. Security and Compliance
```markdown
- Encrypt sensitive metrics
- Implement access controls
- Configure audit logging
- Regular compliance checks
- Monitor security metrics
```

### Common Implementation Challenges

1. Scale Issues
```markdown
- High cardinality metrics
- Resource consumption
- Storage growth
- Query performance
- Alert fatigue
```

2. Operational Complexity
```markdown
- Configuration management
- Cross-team coordination
- Tool integration
- Data retention policies
- Cost management
```

[Continue with more scenarios if needed...]
