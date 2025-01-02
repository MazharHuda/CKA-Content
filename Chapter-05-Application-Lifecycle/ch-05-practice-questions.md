# Chapter 5: Application Lifecycle Management - Practice Questions

## Section 1: Deployment Strategies

### Question 1
Given this deployment configuration:
```yaml
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
  template:
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
```
During an update to nginx:1.20, what is the maximum number of pods that could be available at any time?

a) 4 pods
b) 5 pods
c) 3 pods
d) 6 pods

**Answer:** b
**Explanation:** With maxSurge=1, the deployment can temporarily create 1 extra pod during the update. Therefore, the maximum number of pods would be the original replicas (4) + maxSurge (1) = 5 pods.

### Question 2
In a blue-green deployment scenario, what happens to the old (blue) deployment after the switch to the new (green) deployment is complete?

a) It is automatically deleted
b) It remains as a backup for potential rollback
c) It continues receiving traffic
d) It is scaled to zero replicas

**Answer:** b
**Explanation:** In blue-green deployments, the old deployment is typically kept as a backup to enable quick rollbacks if issues are discovered in the new deployment. It's not automatically deleted or scaled down.

## Section 2: Configuration Management

### Question 3
Examine this ConfigMap usage:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: config-test-pod
spec:
  containers:
  - name: test-container
    image: busybox
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```
What happens to the pod if the ConfigMap 'app-config' is updated?

a) The pod automatically restarts
b) The mounted configuration files are automatically updated
c) The pod needs to be manually restarted
d) The configuration remains unchanged until pod restart

**Answer:** b
**Explanation:** When a ConfigMap is mounted as a volume, any updates to the ConfigMap are automatically reflected in the mounted files. However, the application needs to be designed to reload its configuration.

### Question 4
You need to update a secret being used by a deployment. Which approach ensures zero downtime?

a) Update the secret and restart the pods
b) Create a new secret and update the deployment to use it
c) Modify the secret directly in etcd
d) Delete and recreate the pods with the new secret

**Answer:** b
**Explanation:** Creating a new secret and updating the deployment to use it allows for a controlled rollout of the new configuration, ensuring zero downtime as pods are gradually updated.

## Section 3: Application Scaling

### Question 5
Given this HPA configuration:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```
If CPU utilization drops to 20% for 2 minutes, what happens?

a) Pods are immediately scaled down
b) No scaling occurs yet
c) Pods scale down to minimum replicas
d) Pods are deleted after 300 seconds

**Answer:** b
**Explanation:** The stabilizationWindowSeconds of 300 means the HPA will wait for 5 minutes of sustained low utilization before scaling down, so no immediate action is taken after only 2 minutes.

## Section 4: Multi-cluster Management

### Question 6
In a multi-cluster deployment using active-active configuration, which statement is true about service discovery?

a) Services automatically discover endpoints across clusters
b) A global load balancer must be configured
c) Services can only discover local endpoints
d) Service discovery is handled by the CNI plugin

**Answer:** b
**Explanation:** In multi-cluster deployments, a global load balancer must be configured to distribute traffic between clusters as Kubernetes services by default only work within a single cluster.

### Question 7
You're implementing a canary deployment. Given:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service-v1
      weight: 90
    - destination:
        host: my-service-v2
      weight: 10
```
What percentage of traffic will the new version (v2) receive?

a) 90%
b) 10%
c) 50%
d) 100%

**Answer:** b
**Explanation:** The weight: 10 for v2 means that 10% of the traffic will be routed to the new version, while 90% continues to go to the original version.

## Section 5: Advanced Scenarios

### Question 8
You need to implement A/B testing based on user location. Which Istio resource should you use?

a) DestinationRule
b) VirtualService
c) Gateway
d) ServiceEntry

**Answer:** b
**Explanation:** VirtualService provides traffic routing capabilities including the ability to route based on headers, which can be used to implement A/B testing based on user attributes like location.

### Question 9
In a blue-green deployment, what is the primary purpose of keeping both versions running after the switch?

a) Load balancing between versions
b) Quick rollback capability
c) Resource efficiency
d) Testing purposes

**Answer:** b
**Explanation:** Keeping both versions running allows for immediate rollback by simply switching the service selector back to the previous version if issues are discovered in the new version.

### Question 10
You're implementing a rolling update with maxSurge=25% and maxUnavailable=25% on a deployment with 100 replicas. What is the maximum number of pods that could be unavailable during the update?

a) 25 pods
b) 50 pods
c) 75 pods
d) 100 pods

**Answer:** a
**Explanation:** With maxUnavailable=25%, the maximum number of pods that can be unavailable during the update is 25% of the desired replicas (100), which is 25 pods.

## Section 6: Advanced Deployment Scenarios

### Question 11
Given this feature flag configuration:
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
        "percentage": 20,
        "users": ["beta-testers"]
      }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: FEATURE_FLAGS
          valueFrom:
            configMapKeyRef:
              name: feature-flags
              key: features.json
```
What percentage of users will see the new UI?

a) 100% of users
b) 20% of all users
c) 20% of beta-testers only
d) 0% of users

**Answer:** c
**Explanation:** The configuration shows that the new UI is enabled for 20% of users who are in the beta-testers group only. Regular users won't see the feature regardless of the percentage.

### Question 12
In a shadow deployment pattern:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - route:
    - destination:
        host: my-service-v1
    mirror:
      host: my-service-v2
    mirror_percent: 50
```
What happens to the responses from the mirrored traffic?

a) They are sent back to users
b) They are discarded
c) They are logged for comparison
d) They are cached for future use

**Answer:** b
**Explanation:** In shadow deployments (also called mirror or dark launch), the mirrored traffic responses are discarded. The purpose is to test the new version's behavior without affecting users.

### Question 13
You're implementing a deployment with session affinity:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  ports:
  - port: 80
  selector:
    app: web
```
What happens if a pod handling a client's sessions fails?

a) The client loses their session data
b) The session is automatically transferred to another pod
c) The client is redirected to the same pod when it restarts
d) The client is assigned to a new pod with a new session

**Answer:** a
**Explanation:** With ClientIP session affinity, if a pod fails, the client will be routed to a different pod, but session data is not automatically transferred. Session persistence across pods requires external session storage.

### Question 14
Examine this progressive delivery configuration:
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
```
How long will it take to reach 50% traffic to the new version if all metrics pass?

a) 5 minutes
b) 2.5 minutes
c) 10 minutes
d) 5 hours

**Answer:** a
**Explanation:** With stepWeight: 5 and maxWeight: 50, it will take 10 steps (50/5) to reach 50% traffic. Each step takes 30s (interval), so total time = 10 steps × 30s = 5 minutes.

### Question 15
In a deployment using the Strangler Fig pattern:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: legacy-migration
spec:
  hosts:
  - legacy.example.com
  http:
  - match:
    - uri:
        prefix: "/api/v2/"
    route:
    - destination:
        host: new-service
  - route:
    - destination:
        host: legacy-service
```
What happens to requests to `/api/v1/users`?

a) They are rejected
b) They are routed to new-service
c) They are routed to legacy-service
d) They return a 404 error

**Answer:** c
**Explanation:** In the Strangler Fig pattern, only specifically matched paths (here `/api/v2/`) are routed to the new service. All other paths default to the legacy service, allowing gradual migration.

### Question 16
Given this deployment with readiness gates:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      readinessGates:
      - conditionType: "custom.io/feature-complete"
      containers:
      - name: app
        image: myapp:v2
```
What happens if the custom condition is never satisfied?

a) The pod starts normally
b) The pod remains in NotReady state
c) The deployment fails
d) The pod is rescheduled

**Answer:** b
**Explanation:** When using readiness gates, a pod will not be marked as Ready until all readiness gates conditions are satisfied, even if all containers are ready. The pod will remain in NotReady state.

### Question 17
You're implementing a deployment with custom metrics:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  metrics:
  - type: Pods
    pods:
      metric:
        name: queue_length
      target:
        type: AverageValue
        averageValue: 10
```
What happens if the metrics server can't collect the custom metric?

a) The HPA uses the last known value
b) The HPA stops scaling
c) The HPA scales to minimum replicas
d) The HPA scales to maximum replicas

**Answer:** b
**Explanation:** When custom metrics are unavailable, the HPA controller will not make scaling decisions based on that metric. It will continue to enforce min/max replicas but won't actively scale based on the missing metric.