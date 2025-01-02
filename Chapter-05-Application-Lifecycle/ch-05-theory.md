# Chapter 5: Application Lifecycle Management

## 1. Deployment Strategies

### 1.1 Overview of Deployment Types
```ascii
┌──────────────────────────────────────────────────┐
│              Deployment Strategies               │
│                                                 │
│  ┌─────────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Rolling    │  │ Blue/    │  │  Canary   │  │
│  │  Update     │  │ Green    │  │           │  │
│  └─────────────┘  └──────────┘  └───────────┘  │
│                                                 │
└──────────────────────────────────────────────────┘
```

### 1.2 Rolling Update Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v2
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

### 1.3 Deployment Process Flow
```ascii
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Version 1│────►│Rolling   │────►│Version 2 │
│ Pods     │     │Update    │     │Pods      │
└──────────┘     └──────────┘     └──────────┘
     ▲                                 │
     └─────────────────────────────────┘
           Rollback if needed
```

## 2. Configuration Management

### 2.1 ConfigMaps and Secrets
```yaml
# ConfigMap Example
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    environment=production
    log_level=INFO
    feature.flag=true
  cache.conf: |
    max_size=512m
    eviction_policy=lru

# Secret Example
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  db-password: supersecret
  api-key: abc123xyz789
```

### 2.2 Configuration Mounting Options
```ascii
┌─────────────Pod──────────────┐
│                              │
│  ┌──────────Container───┐    │
│  │                      │    │
│  │   ┌─────────────┐   │    │
│  │   │Environment  │   │    │
│  │   │Variables    │   │    │
│  │   └─────────────┘   │    │
│  │                      │    │
│  │   ┌─────────────┐   │    │
│  │   │Volume       │   │    │
│  │   │Mounts      │   │    │
│  │   └─────────────┘   │    │
│  └──────────────────────┘    │
└──────────────────────────────┘
```

## 3. Application Scaling

### 3.1 Horizontal Pod Autoscaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 500Mi
```

### 3.2 Scaling Process
```ascii
┌─────────────────────────────────────────┐
│           HPA Controller                │
│                                         │
│  ┌─────────┐    ┌────────┐   ┌──────┐  │
│  │ Metrics │───►│Decision│──►│Scale │  │
│  │Collector│    │ Making │   │Action│  │
│  └─────────┘    └────────┘   └──────┘  │
└─────────────────────────────────────────┘
```

## 4. Application Health Management

### 4.1 Health Check Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-health
spec:
  containers:
  - name: app
    image: myapp:v1
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 5
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 3
    startupProbe:
      httpGet:
        path: /health/startup
        port: 8080
      failureThreshold: 30
      periodSeconds: 10
```

### 4.2 Health Check Types
```ascii
┌────────────────────────────────────┐
│         Health Check Types         │
│                                   │
│  ┌────────┐  ┌─────────┐  ┌────┐  │
│  │Liveness│  │Readiness│  │Start│  │
│  │Probe   │  │Probe    │  │Probe│  │
│  └────────┘  └─────────┘  └────┘  │
│      │           │          │      │
│  Restarts    Traffic     Initial   │
│  Container   Control     Startup   │
└────────────────────────────────────┘
```

## Best Practices

1. Deployment Strategy
   - Use rolling updates for zero-downtime deployments
   - Set appropriate surge and unavailable pod limits
   - Implement proper readiness probes
   - Plan rollback procedures

2. Configuration Management
   - Use ConfigMaps for non-sensitive configuration
   - Implement Secrets for sensitive data
   - Version control configurations
   - Use environment-specific configs

3. Application Scaling
   - Set appropriate resource requests/limits
   - Configure HPA thresholds carefully
   - Monitor scaling events
   - Implement proper pod disruption budgets

4. Health Management
   - Implement all three probe types
   - Set appropriate timeouts and thresholds
   - Use meaningful health check endpoints
   - Monitor probe failures

## Common Pitfalls

1. Deployment Issues
   - Insufficient resource requests
   - Missing readiness probes
   - Improper rollback strategy
   - Image pull failures

2. Configuration Problems
   - Hardcoded configurations
   - Insecure secret management
   - Missing environment variables
   - Configuration drift

3. Scaling Challenges
   - Inappropriate scaling thresholds
   - Resource constraint issues
   - Missing metrics
   - Scaling lag

4. Health Check Failures
   - Incorrect probe configuration
   - Resource-intensive health checks
   - Missing failure handling
   - Improper timeout values

## Real-world Considerations

1. Production Readiness
   - High availability setup
   - Disaster recovery plan
   - Monitoring and alerting
   - Performance optimization

2. Security
   - Secret rotation
   - Access control
   - Network security
   - Vulnerability scanning

3. Maintenance
   - Update strategies
   - Backup procedures
   - Scaling policies
   - Resource management

## 5. Advanced Deployment Patterns

### 5.1 Blue-Green Deployment
```ascii
┌─────────────────────────────────────────────────┐
│              Blue-Green Deployment              │
│                                                │
│    ┌─────────┐                ┌─────────┐      │
│    │ Blue    │                │ Green   │      │
│    │(Active) │                │(Staging)│      │
│    └────┬────┘                └────┬────┘      │
│         │                          │           │
│    ┌────▼──────────────────────────▼────┐     │
│    │           Load Balancer           │     │
│    └─────────────────┬────────────────┘     │
│                      │                       │
│                   Traffic                    │
└─────────────────────────────────────────────────┘
```

#### Implementation Example
```yaml
# Blue Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:1.0
---
# Green Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
  labels:
    app: myapp
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:2.0
---
# Service for switching between blue and green
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
    version: blue  # Switch to 'green' for cutover
  ports:
  - port: 80
    targetPort: 8080
```

### 5.2 Canary Deployment
```ascii
┌──────────────────────────────────────────┐
│           Canary Deployment              │
│                                         │
│  ┌────────────────┐   ┌──────────────┐  │
│  │   Production   │   │    Canary    │  │
│  │    (90%)      │   │    (10%)     │  │
│  └───────┬────────┘   └──────┬───────┘  │
│          │                   │          │
│     ┌────▼───────────────────▼────┐     │
│     │      Traffic Splitting      │     │
│     └──────────────┬─────────────┘     │
│                    │                    │
│                 Users                   │
└──────────────────────────────────────────┘
```

#### Implementation Example
```yaml
# Main Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-main
spec:
  replicas: 9  # 90% of traffic
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: app
        image: myapp:1.0
---
# Canary Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-canary
spec:
  replicas: 1  # 10% of traffic
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
      - name: app
        image: myapp:2.0
---
# Service with traffic splitting
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app-vsvc
spec:
  hosts:
  - app.example.com
  http:
  - route:
    - destination:
        host: app-main
        subset: v1
      weight: 90
    - destination:
        host: app-canary
        subset: v2
      weight: 10
```

### 5.3 A/B Testing Deployment
```ascii
┌───────────────────────────────────────────┐
│            A/B Testing Setup              │
│                                          │
│  ┌─────────┐          ┌─────────┐        │
│  │Version A│          │Version B│        │
│  │         │          │         │        │
│  └────┬────┘          └────┬────┘        │
│       │                    │             │
│  ┌────▼────────────────────▼────┐        │
│  │      Traffic Router          │        │
│  │  (Based on User Criteria)    │        │
│  └─────────────┬───────────────┘        │
│                │                         │
│             Users                       │
└───────────────────────────────────────────┘
```

#### Implementation Example
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: app-ab-test
spec:
  hosts:
  - app.example.com
  http:
  - match:
    - headers:
        user-agent:
          regex: ".*Chrome.*"
    route:
    - destination:
        host: version-a
  - route:
    - destination:
        host: version-b
```

### 5.4 Feature Flags Deployment
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  features.json: |
    {
      "newUI": {
        "enabled": true,
        "users": ["beta-testers"],
        "percentage": 25
      },
      "recommendation-engine": {
        "enabled": false,
        "whitelist": ["premium-users"]
      }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-with-features
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0
        volumeMounts:
        - name: features
          mountPath: /etc/config
        env:
        - name: FEATURE_FLAGS_FILE
          value: /etc/config/features.json
      volumes:
      - name: features
        configMap:
          name: feature-flags
```

### Best Practices for Advanced Deployments

1. Blue-Green Deployments
   - Ensure identical infrastructure for both environments
   - Implement proper health checks
   - Plan rollback procedures
   - Test both environments before switching

2. Canary Deployments
   - Start with small traffic percentage
   - Monitor key metrics
   - Define clear success/failure criteria
   - Implement automated rollback triggers

3. A/B Testing
   - Define clear test metrics
   - Implement proper monitoring
   - Use consistent user routing
   - Plan test duration

4. Feature Flags
   - Centralize flag management
   - Implement proper access control
   - Monitor feature usage
   - Clean up unused flags

### Common Pitfalls

1. Resource Management
   - Insufficient capacity planning
   - Resource contention
   - Improper scaling configuration
   - Memory leaks

2. Traffic Management
   - Incorrect routing rules
   - Session handling issues
   - Load balancer misconfiguration
   - Network latency

3. Monitoring and Metrics
   - Insufficient monitoring
   - Missing key metrics
   - Delayed alerting
   - Incomplete logging

## 6. Multi-cluster Deployment Patterns

### 6.1 Multi-cluster Architecture Overview
```ascii
┌─────────────────────────────────────────────────────────┐
│                  Multi-cluster Setup                    │
│                                                        │
│  ┌─────────Cluster A──────┐   ┌─────────Cluster B────┐ │
│  │                        │   │                       │ │
│  │  ┌─────┐    ┌─────┐   │   │   ┌─────┐   ┌─────┐  │ │
│  │  │App A│    │App B│   │   │   │App A│   │App B│  │ │
│  │  └──┬──┘    └──┬──┘   │   │   └──┬──┘   └──┬──┘  │ │
│  │     │         │      │   │      │        │     │ │
│  └─────┼─────────┼──────┘   └──────┼────────┼─────┘ │
│        │         │                  │        │       │
│    ┌───▼─────────▼──────────────────▼────────▼───┐   │
│    │           Global Load Balancer              │   │
│    └───────────────────┬───────────────────────┘   │
│                        │                           │
│                     Traffic                        │
└─────────────────────────────────────────────────────┘
```

### 6.2 Active-Active Configuration
```yaml
# Cluster A Configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: global-app
  annotations:
    cluster-name: cluster-a
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: global-app
    spec:
      containers:
      - name: app
        image: myapp:1.0
        env:
        - name: CLUSTER_NAME
          value: "cluster-a"
---
# Global Service Discovery (using external-dns)
apiVersion: v1
kind: Service
metadata:
  name: global-app
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.global.example.com
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: global-app
```

### 6.3 Active-Passive Setup
```ascii
┌──────────Active Cluster───────┐  ┌──────────Passive Cluster─────┐
│                              │  │                               │
│  ┌─────┐ ┌─────┐ ┌─────┐    │  │  ┌─────┐ ┌─────┐ ┌─────┐    │
│  │Pod 1│ │Pod 2│ │Pod 3│    │  │  │Pod 1│ │Pod 2│ │Pod 3│    │
│  └──┬──┘ └──┬──┘ └──┬──┘    │  │  └──┬──┘ └──┬──┘ └──┬──┘    │
│     │       │       │       │  │     │       │       │       │
│  ┌──▼───────▼───────▼──┐    │  │  ┌──▼───────▼───────▼──┐    │
│  │    Active Service   │    │  │  │   Passive Service   │    │
│  └──────────┬─────────┘    │  │  └──────────┬─────────┘    │
└─────────────┼──────────────┘  └─────────────┼──────────────┘
              │                               │
              │         Failover              │
              └───────────Switch──────────────┘
```

### 6.4 Data Replication Strategy
```yaml
# Database StatefulSet with Cross-cluster Replication
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  replicas: 3
  serviceName: database
  template:
    spec:
      containers:
      - name: database
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
        - name: MYSQL_REPLICATION_MODE
          value: "group"
        - name: MYSQL_CLUSTER_MEMBERS
          value: "database-0.database.cluster-a,database-0.database.cluster-b"
        volumeMounts:
        - name: data
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

### 6.5 Cross-cluster Service Discovery
```yaml
# Service Export Configuration
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ServiceExport
metadata:
  name: global-app
  namespace: default
---
# Service Import Configuration
apiVersion: multicluster.x-k8s.io/v1alpha1
kind: ServiceImport
metadata:
  name: global-app
spec:
  type: ClusterSetIP
  ports:
  - port: 80
    protocol: TCP
```

### 6.6 Multi-cluster Load Balancing
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: global-app
spec:
  host: global-app.default.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
  subsets:
  - name: cluster-a
    labels:
      cluster: cluster-a
  - name: cluster-b
    labels:
      cluster: cluster-b
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: global-app
spec:
  hosts:
  - global-app.default.svc.cluster.local
  http:
  - route:
    - destination:
        host: global-app.default.svc.cluster.local
        subset: cluster-a
      weight: 50
    - destination:
        host: global-app.default.svc.cluster.local
        subset: cluster-b
      weight: 50
```

### Best Practices

1. Cluster Management
   - Use consistent configurations across clusters
   - Implement proper access controls
   - Maintain cluster version parity
   - Regular synchronization checks

2. Data Management
   - Implement proper backup strategies
   - Configure data replication
   - Monitor replication lag
   - Plan for disaster recovery

3. Network Configuration
   - Configure secure cross-cluster communication
   - Implement service mesh for traffic management
   - Monitor network latency
   - Plan for network partitions

4. Monitoring and Observability
   - Centralized logging
   - Cross-cluster metrics
   - Distributed tracing
   - Alerting system

### Common Pitfalls

1. Configuration Management
   - Configuration drift between clusters
   - Inconsistent security policies
   - Resource naming conflicts
   - Version mismatches

2. Network Issues
   - Cross-cluster latency
   - Network partitions
   - DNS resolution problems
   - Load balancing issues

3. Data Consistency
   - Replication delays
   - Data conflicts
   - Backup inconsistencies
   - Recovery complications

