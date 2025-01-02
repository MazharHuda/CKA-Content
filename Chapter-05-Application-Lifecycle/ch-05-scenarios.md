# Chapter 5: Application Lifecycle Management - Real-world Scenarios

## Scenario 1: E-commerce Platform Migration

### Context
A large e-commerce company needs to migrate their monolithic application to a microservices architecture while ensuring zero downtime and maintaining session persistence.

### Requirements
- Zero downtime migration
- Session persistence
- Gradual traffic shifting
- Performance monitoring
- Rollback capability

### Solution

#### 1. Strangler Fig Pattern Implementation
```yaml
# New Microservice Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service-new
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
      version: v2
  template:
    metadata:
      labels:
        app: product-service
        version: v2
    spec:
      containers:
      - name: product-service
        image: product-service:v2
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
---
# Traffic Routing Configuration
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: product-service
spec:
  hosts:
  - product.example.com
  http:
  - match:
    - uri:
        prefix: "/api/v2/products"
    route:
    - destination:
        host: product-service-new
  - route:
    - destination:
        host: product-service-legacy
```

#### 2. Session Management
```yaml
# Redis Session Store
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-session
spec:
  serviceName: redis-session
  replicas: 3
  template:
    spec:
      containers:
      - name: redis
        image: redis:6.2
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: redis-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

## Scenario 2: Global SaaS Application Deployment

### Context
A SaaS provider needs to deploy their application globally with region-specific configurations and compliance requirements.

### Requirements
- Multi-region deployment
- Region-specific configurations
- Data residency compliance
- Automated deployment pipeline
- Performance optimization

### Solution

#### 1. Regional Configuration Management
```yaml
# Region-specific ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-eu
  namespace: production-eu
data:
  app.properties: |
    region=eu-west-1
    data.center=ireland
    compliance.mode=gdpr
    feature.flags={"privacy.shield": true}
---
# Regional Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-eu
spec:
  replicas: 5
  template:
    spec:
      containers:
      - name: app
        image: saas-app:v1.2
        envFrom:
        - configMapRef:
            name: app-config-eu
        volumeMounts:
        - name: eu-certs
          mountPath: /etc/certs
      volumes:
      - name: eu-certs
        secret:
          secretName: eu-tls-certs
```

#### 2. Global Load Balancing
```yaml
# Global DNS Configuration
apiVersion: externaldns.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: global-app
spec:
  endpoints:
  - dnsName: app.example.com
    targets:
    - eu-west-1.elb.amazonaws.com
    - us-east-1.elb.amazonaws.com
    recordType: CNAME
    recordTTL: 300
```

## Scenario 3: CI/CD Pipeline with Progressive Delivery

### Context
A development team needs to implement a robust CI/CD pipeline with progressive delivery features for their microservices.

### Requirements
- Automated testing
- Progressive rollouts
- Metric-based promotion
- Automated rollbacks
- Integration testing

### Solution

#### 1. Progressive Delivery Configuration
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: app-canary
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  service:
    port: 80
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
    webhooks:
      - name: integration-tests
        type: pre-rollout
        url: http://test-runner.test/integration
      - name: load-tests
        type: during-rollout
        url: http://test-runner.test/load
```

#### 2. Monitoring and Alerting
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: deployment-alerts
spec:
  groups:
  - name: deployment
    rules:
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) 
        / 
        sum(rate(http_requests_total[5m])) > 0.01
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate detected during deployment
```

## Best Practices and Lessons Learned

1. Deployment Strategy
   - Use feature flags for risk mitigation
   - Implement proper monitoring before migration
   - Plan rollback procedures
   - Test in staging environment
   - Monitor user impact

2. Configuration Management
   - Version control all configurations
   - Use secrets management
   - Implement audit logging
   - Regular configuration reviews
   - Environment-specific configs

3. Monitoring and Metrics
   - Define SLOs/SLIs
   - Implement proper alerting
   - Monitor business metrics
   - Track user experience
   - Performance baselines

4. Security Considerations
   - Regular security scans
   - Compliance monitoring
   - Access control reviews
   - Secret rotation
   - Network policies

## Common Pitfalls

1. Migration Issues
   - Insufficient testing
   - Poor rollback planning
   - Missing monitoring
   - Database schema conflicts
   - Network dependencies

2. Configuration Problems
   - Environment mismatches
   - Secret exposure
   - Missing configurations
   - Invalid values
   - Version conflicts

3. Performance Issues
   - Resource constraints
   - Network latency
   - Cache misses
   - Database bottlenecks
   - Memory leaks

## Scenario 4: Disaster Recovery Implementation

### Context
A financial services company needs to implement a comprehensive disaster recovery strategy for their Kubernetes-based trading platform.

### Requirements
- RPO < 5 minutes
- RTO < 15 minutes
- Cross-region failover
- Data consistency
- Automated recovery procedures

### Solution

#### 1. Backup Configuration
```yaml
# Velero Backup Schedule
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  template:
    includedNamespaces:
    - trading-platform
    - user-data
    includedResources:
    - deployments
    - statefulsets
    - configmaps
    - secrets
    - persistentvolumeclaims
    storageLocation: aws-backup
    volumeSnapshotLocations:
    - aws-snapshot
    hooks:
      preHooks:
      - exec:
          command:
          - /bin/sh
          - -c
          - "/backup/pre-backup.sh"
          container: trading-app
          onError: Fail
```

#### 2. Cross-Region Data Replication
```yaml
# Primary Database StatefulSet
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: trading-db-primary
spec:
  replicas: 3
  serviceName: trading-db
  template:
    spec:
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: trading
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-creds
              key: username
        - name: REPLICATION_MODE
          value: "master"
        - name: REPLICATION_USER
          valueFrom:
            secretKeyRef:
              name: replication-creds
              key: username
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
---
# Secondary Database (DR Region)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: trading-db-secondary
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: postgresql
        env:
        - name: REPLICATION_MODE
          value: "slave"
        - name: MASTER_HOST
          value: "trading-db-primary.primary-region"
```

#### 3. Automated Failover Configuration
```yaml
# Global Service Discovery
apiVersion: v1
kind: Service
metadata:
  name: trading-platform-global
  annotations:
    global.traffic.policy: "failover"
    failover.region.primary: "us-east-1"
    failover.region.secondary: "eu-west-1"
spec:
  ports:
  - port: 443
    targetPort: 8443
  selector:
    app: trading-platform
---
# Health Check Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-config
data:
  check-primary.sh: |
    #!/bin/bash
    if ! curl -sf https://trading-platform.primary/health; then
      /usr/local/bin/kubectl patch svc trading-platform-global \
        -p '{"metadata":{"annotations":{"active.region":"eu-west-1"}}}'
    fi
```

#### 4. Recovery Automation
```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: dr-test
spec:
  schedule: "0 0 * * 0"  # Weekly
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: dr-test
            image: dr-test:v1
            env:
            - name: BACKUP_LOCATION
              value: "s3://backups/trading"
            - name: DR_REGION
              value: "eu-west-1"
            command:
            - /scripts/test-recovery.sh
          restartPolicy: OnFailure
```

### Recovery Procedures

#### 1. Automated Recovery Script
```bash
#!/bin/bash
# recovery.sh

# Set variables
PRIMARY_REGION="us-east-1"
DR_REGION="eu-west-1"
NAMESPACE="trading-platform"

# Check primary region health
check_primary_health() {
    kubectl --context=$PRIMARY_REGION get nodes --no-headers | grep -q "Ready"
    return $?
}

# Initiate failover
perform_failover() {
    # 1. Switch DNS
    aws route53 change-resource-record-sets \
        --hosted-zone-id $HOSTED_ZONE \
        --change-batch file://dns-failover.json

    # 2. Promote DR database
    kubectl --context=$DR_REGION \
        exec -it trading-db-secondary-0 -- \
        pg_ctl promote

    # 3. Scale up DR applications
    kubectl --context=$DR_REGION \
        scale deployment trading-platform --replicas=10

    # 4. Update global service
    kubectl --context=$DR_REGION \
        patch svc trading-platform-global \
        -p '{"metadata":{"annotations":{"active.region":"eu-west-1"}}}'
}
```

#### 2. Data Verification
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-verification
spec:
  template:
    spec:
      containers:
      - name: verify
        image: data-verify:v1
        env:
        - name: PRIMARY_DB
          value: "trading-db-primary.primary-region"
        - name: DR_DB
          value: "trading-db-secondary.dr-region"
        command:
        - /scripts/verify-data.sh
      restartPolicy: OnFailure
```

### Best Practices

1. Backup Strategy
   - Regular backup testing
   - Multiple backup locations
   - Encrypted backups
   - Retention policy
   - Backup monitoring

2. Failover Process
   - Automated health checks
   - Regular failover testing
   - Documentation
   - Team training
   - Communication plan

3. Data Management
   - Consistent backups
   - Replication monitoring
   - Data validation
   - Corruption detection
   - Recovery testing

4. Recovery Testing
   - Regular DR drills
   - Performance testing
   - Data integrity checks
   - Team readiness
   - Process documentation

### Common Pitfalls

1. Backup Issues
   - Incomplete backups
   - Backup corruption
   - Long backup times
   - Storage costs
   - Recovery time objectives

2. Replication Problems
   - Replication lag
   - Network issues
   - Data inconsistency
   - Resource constraints
   - Configuration drift

3. Recovery Challenges
   - Complex dependencies
   - Missing documentation
   - Incomplete testing
   - Team coordination
   - Communication issues

## Scenario 5: High Availability Implementation

### Context
A healthcare platform needs to implement a highly available infrastructure for their critical patient management system with zero downtime requirements.

### Requirements
- 99.999% uptime
- Zero-downtime maintenance
- Geographic redundancy
- Load balancing
- Automatic failover

### Solution

#### 1. Multi-Zone Deployment Configuration
```yaml
# Pod Anti-affinity Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: patient-system
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: patient-system
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - patient-system
            topologyKey: topology.kubernetes.io/zone
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role
                operator: In
                values:
                - high-availability
      containers:
      - name: patient-app
        image: patient-system:v1
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /live
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
```

#### 2. Database High Availability
```yaml
# StatefulSet for Database Cluster
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: patient-db
spec:
  serviceName: patient-db
  replicas: 3
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: patient-db
            topologyKey: topology.kubernetes.io/zone
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: patient_records
        - name: PATRONI_REPLICATION_USERNAME
          valueFrom:
            secretKeyRef:
              name: db-creds
              key: replication-username
        - name: PATRONI_KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: PATRONI_KUBERNETES_POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: PATRONI_KUBERNETES_PORTS
          value: '[{"name": "postgresql", "port": 5432}]'
        volumeMounts:
        - name: patient-db-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: patient-db-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi
```

#### 3. Load Balancing and Service Mesh
```yaml
# Service Mesh Configuration
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: patient-system
spec:
  host: patient-system
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 1024
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 10
---
# Circuit Breaker Configuration
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: patient-system
spec:
  hosts:
  - patient-system
  http:
  - route:
    - destination:
        host: patient-system
    timeout: 10s
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: connect-failure,refused-stream,unavailable
```

#### 4. Health Monitoring and Auto-Recovery
```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: patient-system-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: patient-system
  minReplicas: 6
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
---
# Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: patient-system-pdb
spec:
  minAvailable: "80%"
  selector:
    matchLabels:
      app: patient-system
```

### Best Practices

1. Infrastructure Design
   - Multi-zone deployment
   - Node anti-affinity rules
   - Resource quotas
   - Network redundancy
   - Load balancing

2. Application Design
   - Stateless applications
   - Circuit breakers
   - Retry mechanisms
   - Health checks
   - Graceful degradation

3. Data Management
   - Synchronous replication
   - Backup strategies
   - Data consistency
   - Cache management
   - Connection pooling

4. Monitoring and Recovery
   - Proactive monitoring
   - Automated scaling
   - Self-healing
   - Alert management
   - Performance metrics

### Common Pitfalls

1. Design Issues
   - Single points of failure
   - Resource contention
   - Network bottlenecks
   - Improper scaling
   - Missing redundancy

2. Operational Challenges
   - Configuration drift
   - Maintenance windows
   - Update strategies
   - Capacity planning
   - Performance degradation

3. Recovery Problems
   - Split-brain scenarios
   - Data inconsistency
   - Failed failovers
   - Resource exhaustion
   - Cascading failures

### Implementation Steps

1. Infrastructure Setup
```bash
# Label nodes for high availability
kubectl label nodes <node-name> node-role=high-availability

# Verify zone distribution
kubectl get nodes --show-labels | grep topology.kubernetes.io/zone

# Monitor pod distribution
kubectl get pods -o wide --show-labels
```

2. Database Setup
```bash
# Initialize database cluster
kubectl apply -f patient-db-statefulset.yaml

# Verify replication status
kubectl exec -it patient-db-0 -- patronictl list

# Test failover
kubectl exec -it patient-db-0 -- patronictl failover
```

3. Service Mesh Configuration
```bash
# Install Istio
istioctl install --set profile=high-availability

# Enable injection
kubectl label namespace patient-system istio-injection=enabled

# Verify mesh status
istioctl analyze
```