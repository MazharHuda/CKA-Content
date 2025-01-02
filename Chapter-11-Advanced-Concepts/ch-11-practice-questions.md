# Chapter 11: Advanced Concepts - Practice Questions

## Section 1: Custom Resource Definitions (CRDs)

### Question 1
Given this CRD definition:
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: backups.stable.example.com
spec:
  group: stable.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                frequency:
                  type: string
                destination:
                  type: string
              required: ["frequency"]
```
What happens if you create a custom resource without specifying the destination field?

a) Creation fails due to validation
b) Resource is created successfully
c) Default value is applied
d) Resource is created in pending state

**Answer:** b
**Explanation:** In this CRD:
1. Only frequency field is marked as required
2. destination field is optional
3. Schema validation allows missing optional fields
4. Resource will be created without destination

### Question 2
When implementing a custom controller, what's the primary purpose of the reconciliation loop?

a) Monitor API server health
b) Ensure desired state matches actual state
c) Validate custom resources
d) Manage resource quotas

**Answer:** b
**Explanation:** The reconciliation loop:
1. Continuously monitors resource state
2. Compares actual vs desired state
3. Takes actions to align states
4. Handles error conditions

## Section 2: Advanced Scheduling

### Question 3
Examine this pod topology spread constraint:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
```
What happens if there are no nodes with the zone label?

a) Pod is scheduled to any node
b) Pod remains in pending state
c) Pod is scheduled with warning
d) Pod scheduling fails

**Answer:** b
**Explanation:** When using topology spread constraints:
1. topologyKey must exist on nodes
2. If key is missing, constraint cannot be satisfied
3. whenUnsatisfiable: DoNotSchedule prevents scheduling
4. Pod remains pending until nodes are labeled

### Question 4
Your pod is using node affinity but not getting scheduled. Given:
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu-type
            operator: In
            values:
            - nvidia-tesla-p100
```
What should you check first?

a) Node labels
b) Pod resource requests
c) Node capacity
d) Scheduler configuration

**Answer:** a
**Explanation:** For node affinity issues:
1. Verify node labels match requirements
2. Check if any nodes have required labels
3. Use kubectl get nodes --show-labels
4. Review node selector terms

## Section 3: Advanced Networking

### Question 5
Given this network policy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: complex-policy
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
    - podSelector:
        matchLabels:
          role: frontend
```
Which statement is true about the policy?

a) Allows traffic from production namespace AND frontend pods
b) Allows traffic from production namespace OR frontend pods
c) Allows traffic only from frontend pods in production namespace
d) Allows all traffic from production namespace

**Answer:** b
**Explanation:** In network policies:
1. Multiple from entries in same rule are OR conditions
2. Multiple conditions within same from entry are AND conditions
3. Policy allows traffic from any pod in production namespace
4. Also allows traffic from any frontend pod in any namespace

### Question 6
You're implementing service mesh features. What's the primary purpose of a sidecar container in this context?

a) Log collection
b) Traffic management
c) Resource monitoring
d) Data backup

**Answer:** b
**Explanation:** Service mesh sidecars:
1. Handle traffic routing and management
2. Implement security policies
3. Provide observability
4. Enable service-to-service communication features

## Section 4: Advanced Security

### Question 7
Examine this pod security context:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  containers:
  - name: sec-container
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
```
What's the effect of dropping ALL capabilities?

a) Container runs in privileged mode
b) Container loses all Linux capabilities
c) Container keeps default capabilities
d) Container fails to start

**Answer:** b
**Explanation:** Dropping ALL capabilities:
1. Removes all Linux kernel capabilities
2. Provides maximum security restriction
3. May affect some application functionality
4. Common security best practice

## Section 5: Advanced Workload Management

### Question 29
Given this HorizontalPodAutoscaler configuration:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Pods
    pods:
      metric:
        name: packets-per-second
      target:
        type: AverageValue
        averageValue: 1k
```
What triggers scaling in this configuration?

a) Only CPU utilization
b) Only packets-per-second
c) Either CPU or packets-per-second
d) Both CPU and packets-per-second must exceed targets

**Answer:** c
**Explanation:** HPA will scale when:
1. Either metric exceeds its target
2. CPU utilization goes above 50%
3. Packets-per-second exceeds 1k
4. Uses the highest recommended replica count

### Question 30
Examine this VerticalPodAutoscaler configuration:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: app-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: 100m
        memory: 50Mi
      maxAllowed:
        cpu: 1
        memory: 500Mi
```
What happens if a container needs more than the maxAllowed resources?

a) Container is terminated
b) Resources are capped at maximum
c) VPA is disabled
d) Pod is evicted

**Answer:** b
**Explanation:** With VPA maxAllowed:
1. Resource requests are capped at maximum
2. Container continues to run
3. May impact performance
4. Prevents excessive resource allocation

### Question 31
Your application needs guaranteed QoS. Given:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed-pod
spec:
  containers:
  - name: app
    image: app:v1
    resources:
      requests:
        memory: "128Mi"
        cpu: "500m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```
What makes this pod Guaranteed QoS?

a) Having both requests and limits
b) Requests equal to limits
c) High resource values
d) Memory configuration

**Answer:** b
**Explanation:** For Guaranteed QoS:
1. Every container must have requests and limits
2. Requests must equal limits for both CPU and memory
3. All containers in pod must meet criteria
4. Provides highest level of resource guarantee

### Question 32
Given this PodDisruptionBudget:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: critical-service
```
During node maintenance, what happens if only 2 pods are running?

a) One pod can be evicted
b) No pods can be evicted
c) All pods can be evicted
d) Node drain fails

**Answer:** b
**Explanation:** With minAvailable: 2:
1. Must maintain at least 2 pods
2. Cannot evict if only 2 pods running
3. Protects service availability
4. Node drain will be blocked

### Question 33
Your application needs to run exactly one pod per node. What's the best approach?

a) Use node selectors
b) Use DaemonSet
c) Use anti-affinity rules
d) Use StatefulSet

**Answer:** b
**Explanation:** DaemonSet is ideal because:
1. Automatically runs one pod per node
2. Handles node additions/removals
3. Ensures even distribution
4. Perfect for node-level services

### Question 34
Examine this priority class:
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
preemptionPolicy: Never
```
What happens when a pod using this class is scheduled?

a) Preempts lower priority pods
b) Waits for resources to be available
c) Gets scheduled immediately
d) Fails if resources unavailable

**Answer:** b
**Explanation:** With preemptionPolicy: Never:
1. Pod has high scheduling priority
2. Won't preempt other pods
3. Waits for resources naturally
4. Maintains system stability

## Section 6: Advanced Scheduling Patterns

### Question 35
Given this pod topology spread constraint:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: web
  containers:
  - name: nginx
    image: nginx
```
What happens if the skew constraint cannot be satisfied?

a) Pod remains unscheduled
b) Pod is scheduled with best effort
c) Pod is scheduled to any node
d) Pod scheduling fails

**Answer:** b
**Explanation:** With whenUnsatisfiable: ScheduleAnyway:
1. Scheduler attempts to minimize skew
2. If perfect balance impossible, schedules anyway
3. Best effort distribution is attempted
4. Pod won't remain pending

### Question 36
Examine this node affinity rule:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu-type
            operator: In
            values:
            - nvidia-tesla-p100
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: disk-type
            operator: In
            values:
            - ssd
```
What happens if no nodes have SSD disks?

a) Pod remains unscheduled
b) Pod is scheduled to any node with correct GPU
c) Pod is scheduled to node with HDD
d) Pod scheduling fails

**Answer:** b
**Explanation:** In this configuration:
1. GPU requirement is mandatory (required)
2. SSD is preferred but not required
3. Pod will schedule to any node with correct GPU
4. SSD preference only affects ranking of eligible nodes

### Question 37
Your application needs to ensure pods are spread across failure domains. Given:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 6
  template:
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: web
```
How many pods can be in a single zone if you have 3 zones?

a) 1
b) 2
c) 3
d) 4

**Answer:** c
**Explanation:** With maxSkew: 1:
1. Maximum difference between zones is 1 pod
2. With 6 replicas and 3 zones
3. Ideal distribution is 2 pods per zone
4. Maximum allowed in any zone is 3 pods

### Question 38
You need to ensure certain pods never co-locate on the same node. Which feature should you use?

a) Node selector
b) Node affinity
c) Pod affinity
d) Pod anti-affinity

**Answer:** d
**Explanation:** Pod anti-affinity:
1. Prevents pods from scheduling on same node
2. Based on pod labels
3. Can be required or preferred
4. Essential for high availability

### Question 39
Given this pod anti-affinity rule:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - web
        topologyKey: kubernetes.io/hostname
```
What is the effect of this configuration?

a) Pod must run on same node as web pods
b) Pod cannot run on nodes with web pods
c) Pod must run in same zone as web pods
d) Pod prefers nodes without web pods

**Answer:** b
**Explanation:** This anti-affinity rule:
1. Prevents scheduling where web pods exist
2. Uses hostname as topology key
3. Is a hard requirement (required)
4. Applies during scheduling only

### Question 40
Your cluster has nodes with different capabilities. How should you ensure pods land on appropriate nodes?

a) Use manual scheduling
b) Use taints and tolerations
c) Use node labels and selectors
d) Use pod priority

**Answer:** c
**Explanation:** Node labels and selectors:
1. Allow declarative node selection
2. Can match multiple attributes
3. Easily maintainable
4. Standard Kubernetes feature

[Continue with more questions...]
