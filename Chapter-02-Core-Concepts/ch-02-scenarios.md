# Chapter 2: Core Concepts - Real-world Scenarios

## Scenario 1: Microservices Application Deployment

### Context
A company is migrating their monolithic e-commerce application to microservices on Kubernetes.

### Requirements
- Multiple interconnected services
- High availability
- Service discovery
- Load balancing
- Persistent data storage
- Monitoring capabilities

### Solution

#### 1. Service Architecture
```yaml
# Frontend Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: frontend:v1
        ports:
        - containerPort: 80
        readinessProbe:
          httpGet:
            path: /health
            port: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
# Backend API Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: api:v1
        env:
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: db-host
```

#### 2. Service Discovery Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 8080
    targetPort: 8080
```

### Implementation Steps
1. Deploy infrastructure components
2. Configure networking
3. Set up monitoring
4. Implement scaling policies
5. Configure backups

## Scenario 2: High-Availability Database Cluster

### Context
A financial services company needs to deploy a highly available PostgreSQL database cluster.

### Requirements
- Zero data loss
- Automatic failover
- Regular backups
- Performance monitoring
- Resource isolation

### Solution

#### 1. StatefulSet Configuration
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi
```

#### 2. Backup Configuration
```yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:13
            command: ["/bin/sh", "-c", "pg_dump -h postgres-0.postgres > /backup/db.sql"]
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: backup-pvc
```

## Scenario 3: CI/CD Pipeline Integration

### Context
A development team needs to implement continuous deployment to Kubernetes.

### Requirements
- Automated deployments
- Rolling updates
- Rollback capability
- Environment separation
- Security controls

### Solution

#### 1. Deployment Strategy
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:${VERSION}
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### 2. Environment Separation
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: staging
---
apiVersion: v1
kind: Namespace
metadata:
  name: production
```

## Scenario 4: Multi-tenant Cluster Management

### Context
A SaaS provider needs to host multiple customer applications on the same cluster.

### Requirements
- Resource isolation
- Network segregation
- Access control
- Resource quotas
- Performance monitoring

### Solution

#### 1. Namespace and Resource Quota Setup
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: customer-a
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: customer-quota
  namespace: customer-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
```

#### 2. Network Policy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: customer-a
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          tenant: customer-a
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          tenant: customer-a
```

### Best Practices and Lessons Learned

1. Resource Management
   - Implement resource quotas early
   - Monitor resource usage
   - Set up alerting for resource constraints

2. Security
   - Use RBAC for access control
   - Implement network policies
   - Regular security audits

3. Monitoring
   - Set up comprehensive monitoring
   - Implement logging solution
   - Create dashboards for visibility

4. Backup and Recovery
   - Regular backup schedule
   - Test recovery procedures
   - Document disaster recovery plans

5. Performance Optimization
   - Regular performance reviews
   - Optimize resource requests/limits
   - Implement horizontal pod autoscaling