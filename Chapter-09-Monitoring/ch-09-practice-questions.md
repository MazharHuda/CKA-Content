# Chapter 9: Monitoring - Practice Questions

## Section 1: Metrics Server and Basic Monitoring

### Question 1
After installing Metrics Server, the command `kubectl top nodes` shows "metrics not available". What could be the cause?

a) Metrics Server pod is not running
b) Node exporter is not installed
c) Prometheus is not configured
d) Grafana is missing

**Answer:** a
**Explanation:** The kubectl top command relies on Metrics Server. Common issues include:
1. Metrics Server pod not running or unhealthy
2. Configuration issues with Metrics Server
3. Communication issues between Metrics Server and kubelet
4. Insufficient time for metrics collection

### Question 2
Examine this Metrics Server deployment:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - args:
        - --kubelet-insecure-tls
        - --kubelet-preferred-address-types=InternalIP
```
What is the purpose of --kubelet-insecure-tls?

a) Disable all TLS verification
b) Skip certificate verification for kubelets
c) Use insecure connection to API server
d) Disable HTTPS entirely

**Answer:** b
**Explanation:** The --kubelet-insecure-tls flag:
1. Skips certificate verification when connecting to kubelets
2. Useful in test environments
3. Not recommended for production
4. Helps resolve certificate issues during testing

## Section 2: Prometheus Monitoring

### Question 3
Given this ServiceMonitor configuration:
```yaml
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
    interval: 30s
```
What determines which services are monitored?

a) Service name
b) Service labels
c) Pod labels
d) Namespace labels

**Answer:** b
**Explanation:** ServiceMonitor uses:
1. Label selector to find services to monitor
2. Services must match matchLabels criteria
3. Services must expose metrics endpoint
4. Port name must match specification

### Question 4
Your Prometheus pod is rapidly consuming disk space. What should you check first?

a) Retention period
b) Scrape interval
c) Number of targets
d) Alert rules

**Answer:** a
**Explanation:** For Prometheus storage issues:
1. Check retention period configuration
2. Review storage.tsdb.retention.time setting
3. Monitor disk usage trends
4. Consider data compaction settings

## Section 3: Logging Architecture

### Question 5
Examine this logging configuration:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: app:v1
    args: ["/bin/sh", "-c", "while true; do echo $(date) >> /var/log/app.log; sleep 5; done"]
    volumeMounts:
    - name: log-volume
      mountPath: /var/log
  volumes:
  - name: log-volume
    emptyDir: {}
```
What happens to the logs when the pod is deleted?

a) Logs are automatically archived
b) Logs are permanently lost
c) Logs are saved to node
d) Logs are sent to master

**Answer:** b
**Explanation:** With emptyDir volume:
1. Volume is created when pod is assigned to node
2. Volume exists as long as pod runs on that node
3. When pod is deleted, data is lost
4. Should use persistent storage for log retention

### Question 6
In a cluster with Fluentd DaemonSet, some pods' logs are missing. What should you verify?

a) Pod log path configuration
b) Fluentd pod status on nodes
c) Master node configuration
d) API server logging

**Answer:** b
**Explanation:** For missing logs, check:
1. Fluentd pods running on all nodes
2. Fluentd pod logs for errors
3. Volume mounts for log collection
4. Node access permissions

## Section 4: Alert Management

### Question 7
Given this alert rule:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: node-alerts
spec:
  groups:
  - name: node.rules
    rules:
    - alert: HighNodeCPU
      expr: instance:node_cpu_utilisation:rate5m > 0.8
      for: 10m
```
When will this alert fire?

a) Immediately when CPU exceeds 80%
b) After 10 minutes of high CPU
c) When node CPU reaches 100%
d) After 5 minutes of monitoring

**Answer:** b
**Explanation:** Alert will fire when:
1. CPU utilization exceeds 80%
2. Condition persists for 10 minutes
3. 'for' clause prevents alert flapping
4. Uses 5-minute rate of CPU utilization

### Question 8
Your alerting system is generating too many notifications. What should you implement first?

a) Increase thresholds
b) Add alert grouping
c) Reduce monitoring targets
d) Disable alerts

**Answer:** b
**Explanation:** To reduce alert fatigue:
1. Implement alert grouping
2. Set appropriate thresholds
3. Add alert routing
4. Configure inhibition rules

## Section 5: Performance Monitoring

### Question 9
Using kubectl top, you notice high memory usage in a pod. What command provides more detailed information?

a) kubectl describe pod
b) kubectl logs
c) kubectl get pod -o yaml
d) kubectl exec -- ps aux

**Answer:** d
**Explanation:** To investigate high memory usage:
1. Use kubectl top for overview
2. kubectl exec for detailed process info
3. Check container logs for issues
4. Review pod events

### Question 10
Examine this HPA configuration:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```
What metrics source is required for this HPA to work?

a) Prometheus
b) Metrics Server
c) Custom metrics
d) Node exporter

**Answer:** b
**Explanation:** Resource-based HPA requires:
1. Metrics Server installed and running
2. CPU metrics collection enabled
3. Pod resource requests defined
4. Proper metrics aggregation

### Question 11
Given this custom metrics configuration:
```yaml
apiVersion: custom.metrics.k8s.io/v1beta1
kind: MetricDefinition
metadata:
  name: http_requests_total
spec:
  query: sum(rate(http_requests_total[5m])) by (pod)
```
What type of HPA can use this metric?

a) Resource-based HPA
b) Custom metrics HPA
c) External metrics HPA
d) Object metrics HPA

**Answer:** b
**Explanation:** Custom metrics HPA:
1. Uses metrics defined through custom metrics API
2. Requires custom metrics adapter
3. Allows application-specific scaling
4. Supports more complex scaling scenarios

### Question 12
Your Prometheus storage is growing rapidly. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  retention: 15d
  retentionSize: "10GB"
```
What happens when storage reaches 10GB?

a) Oldest data is automatically deleted
b) New data collection stops
c) Prometheus pod crashes
d) Data is compressed

**Answer:** a
**Explanation:** When retentionSize is reached:
1. Oldest data blocks are removed first
2. Retention is enforced during compaction
3. New data continues to be collected
4. Process is automatic and continuous

### Question 13
Examine this Grafana dashboard configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard
data:
  dashboard.json: |
    {
      "panels": [
        {
          "type": "graph",
          "datasource": "${DS_PROMETHEUS}",
          "targets": [
            {
              "expr": "container_memory_usage_bytes",
              "legendFormat": "{{pod}}"
            }
          ]
        }
      ]
    }
```
Why might some pods not appear in the graph?

a) Missing metrics collection
b) Incorrect datasource variable
c) Wrong metric name
d) Dashboard permissions

**Answer:** a
**Explanation:** Pods might not appear because:
1. Metrics Server not collecting data from pods
2. Pod not exposing metrics endpoint
3. ServiceMonitor not configured correctly
4. Network issues preventing metrics collection

### Question 14
You notice delayed alerts in your monitoring system. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: delayed-alerts
spec:
  groups:
  - name: example
    rules:
    - alert: HighLatency
      expr: http_request_duration_seconds > 1
      for: 5m
      labels:
        severity: warning
```
What could cause alert delays beyond the 5m window?

a) Alert manager configuration
b) Prometheus scrape interval
c) Network latency
d) All of the above

**Answer:** d
**Explanation:** Alert delays can be caused by:
1. Alertmanager grouping and inhibition rules
2. Long Prometheus scrape intervals
3. Network issues between components
4. Resource constraints on monitoring stack

### Question 15
Your cluster's monitoring system shows gaps in metrics. Given:
```bash
$ kubectl get pods -n monitoring
NAME                      READY   STATUS    RESTARTS   AGE
prometheus-0              1/1     Running   0          7d
node-exporter-abc12       1/1     Running   2          7d
node-exporter-def34       0/1     Error    5          7d
```
What should you check first?

a) Node-exporter logs
b) Prometheus configuration
c) Network policies
d) Storage capacity

**Answer:** a
**Explanation:** For metric gaps:
1. Check node-exporter logs for errors
2. Verify node-exporter running on all nodes
3. Check network connectivity
4. Review Prometheus target status

### Question 16
Given this logging configuration:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    image: app:v1
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
```
What happens when log files exceed 4Gi?

a) Logs are automatically rotated
b) Pod is evicted
c) New logs are dropped
d) Container restarts

**Answer:** b
**Explanation:** When ephemeral storage limit is exceeded:
1. Pod is evicted from the node
2. Event is generated
3. Pod may be rescheduled
4. Data may be lost

### Question 17
Examine this monitoring stack error:
```bash
Error: timeout while waiting for response from Prometheus
```
What should you check in this order?

a) Network, Prometheus status, queries
b) Queries, network, Prometheus status
c) Prometheus status, queries, network
d) Queries, Prometheus status, network

**Answer:** a
**Explanation:** Troubleshooting steps:
1. Verify network connectivity first
2. Check Prometheus pod status and logs
3. Review query complexity and timeouts
4. Check resource utilization

### Question 18
Your custom metrics adapter is not providing metrics. Given:
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
What should you verify first?

a) API service registration
b) Metrics adapter pods
c) RBAC permissions
d) TLS certificates

**Answer:** b
**Explanation:** Troubleshooting steps:
1. Check metrics adapter pod status and logs
2. Verify API service registration
3. Check RBAC permissions
4. Validate TLS configuration

### Question 19
Given this monitoring alert:
```yaml
- alert: PodCrashLooping
  expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 5 > 0
  for: 15m
  labels:
    severity: warning
```
Why use the rate function with multiplication?

a) Improve alert accuracy
b) Convert to restarts per hour
c) Reduce false positives
d) Calculate total restarts

**Answer:** b
**Explanation:** The calculation:
1. rate calculates per-second rate
2. Multiply by 60 to get per-minute
3. Multiply by 5 to get per-5-minutes
4. Makes threshold more intuitive

### Question 20
Your monitoring system's time series database is showing poor performance. What should you implement?

a) Increase retention period
b) Add more storage
c) Implement recording rules
d) Reduce scrape interval

**Answer:** c
**Explanation:** Recording rules:
1. Pre-calculate expensive queries
2. Reduce query-time load
3. Improve dashboard performance
4. Better handle high cardinality

## Section 6: Advanced Alerting Configurations

### Question 21
Examine this AlertManager configuration:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: AlertmanagerConfig
metadata:
  name: alert-routing
spec:
  route:
    groupBy: ['alertname', 'cluster']
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 4h
```
What is the purpose of groupWait?

a) Time to wait before sending first alert
b) Time between alert group updates
c) Time before repeating alerts
d) Alert timeout period

**Answer:** a
**Explanation:** groupWait defines:
1. Initial delay before sending first notification
2. Allows time for similar alerts to group
3. Helps reduce alert noise
4. Default is usually 30 seconds

### Question 22
Given this alert rule:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: node-alerts
spec:
  groups:
  - name: node.rules
    rules:
    - alert: NodeMemoryFull
      expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Node {{ $labels.instance }} memory usage is {{ $value }}%"
```
What's the purpose of the `$labels` reference?

a) Access node metadata
b) Format alert message
c) Filter alert targets
d) Set alert priority

**Answer:** a
**Explanation:** $labels provides:
1. Access to target labels
2. Dynamic alert message creation
3. Instance identification
4. Additional context in alerts

## Section 7: Multi-cluster Monitoring

### Question 23
In a multi-cluster setup, you notice duplicate metrics. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  externalLabels:
    cluster: prod-1
  remoteWrite:
    - url: http://thanos-receive:19291
```
What's the purpose of externalLabels?

a) Route alerts
b) Identify metric source
c) Filter metrics
d) Set metric priority

**Answer:** b
**Explanation:** externalLabels:
1. Adds cluster identifier to metrics
2. Prevents metric conflicts
3. Enables cluster-specific querying
4. Essential for multi-cluster setups

### Question 24
Your Thanos setup shows stale data. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ThanosRuler
metadata:
  name: thanos-ruler
spec:
  queryEndpoints:
    - dnssrv+_http._tcp.thanos-query.monitoring.svc.cluster.local
  evaluationInterval: 30s
```
What should you check first?

a) Query endpoints
b) Storage configuration
c) Network connectivity
d) Retention settings

**Answer:** a
**Explanation:** For stale data issues:
1. Verify query endpoint connectivity
2. Check service discovery
3. Validate DNS resolution
4. Monitor endpoint health

## Section 8: Custom Metrics Implementation

### Question 25
Examine this custom metrics adapter configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: adapter-config
data:
  config.yaml: |
    rules:
    - seriesQuery: 'http_requests_total{kubernetes_namespace!=""}'
      resources:
        overrides:
          kubernetes_namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^(.*)_total"
        as: "${1}_per_second"
      metricsQuery: 'rate(<<.Series>>{<<.LabelMatchers>>}[2m])'
```
What transformation is being applied to the metrics?

a) Aggregation
b) Rate calculation
c) Normalization
d) Filtering

**Answer:** b
**Explanation:** The configuration:
1. Takes total request metrics
2. Calculates rate over 2 minutes
3. Renames metrics to indicate rate
4. Makes metrics suitable for HPA

### Question 26
Your custom metrics are not being collected. Given:
```yaml
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
    path: /custom-metrics
    interval: 15s
```
What should you verify first?

a) Service labels
b) Metrics endpoint
c) Port configuration
d) Prometheus configuration

**Answer:** b
**Explanation:** Troubleshooting steps:
1. Verify metrics endpoint accessibility
2. Check endpoint returns valid metrics
3. Validate service labels
4. Review Prometheus scrape logs

## Section 9: Performance Optimization

### Question 27
Your Prometheus queries are slow. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: recording-rules
spec:
  groups:
  - name: cpu
    interval: 5m
    rules:
    - record: instance:node_cpu:avg_rate5m
      expr: avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)
```
What's the purpose of this configuration?

a) Alert generation
b) Query optimization
c) Metric aggregation
d) Data sampling

**Answer:** b
**Explanation:** Recording rules:
1. Pre-calculate expensive queries
2. Reduce query-time load
3. Improve dashboard performance
4. Store computed values

### Question 28
Your monitoring stack is consuming excessive resources. Given:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: prometheus
spec:
  retention: 15d
  resources:
    requests:
      memory: "2Gi"
    limits:
      memory: "4Gi"
```
What should you consider first?

a) Reduce retention period
b) Increase resources
c) Add sharding
d) Compress data

**Answer:** a
**Explanation:** To reduce resource usage:
1. Adjust retention period based on needs
2. Review data resolution requirements
3. Consider data downsampling
4. Optimize storage usage

[Continue with more questions if needed...]
